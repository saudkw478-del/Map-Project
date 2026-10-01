"""LLM Gateway: one choke point for every model call.

- tiers: ordered provider lists ("bulk" cheap/free, "important" stronger)
- pinning: an agent sticks to one provider so its voice stays consistent; others are fallbacks only
- budgets: per-provider and global daily request caps (free tiers are limited and change often)
- fallback: rate-limit/error/invalid output => next provider; all fail => None (caller uses code-only L1)
- cache: identical requests are served locally
"""
import hashlib
import json
import os
import time
import tomllib
import urllib.error
import urllib.request
from dataclasses import dataclass, field


class ProviderError(Exception):
    def __init__(self, msg: str, rate_limited: bool = False):
        super().__init__(msg)
        self.rate_limited = rate_limited


@dataclass
class LLMRequest:
    task_type: str
    prompt: str
    system: str = ""
    max_tokens: int = 300
    tier: str = "bulk"
    pin_key: str | None = None       # e.g. "agent:12" -> stable provider choice
    json_mode: bool = False
    temperature: float = 0.7


@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str
    in_tokens: int = 0
    out_tokens: int = 0
    cached: bool = False


class FakeProvider:
    """Deterministic offline provider for development and tests. Costs nothing."""

    def __init__(self, name: str = "fake"):
        self.name, self.model = name, "fake-1"

    def complete(self, req: LLMRequest) -> LLMResponse:
        h = int(hashlib.sha256((req.task_type + req.prompt).encode()).hexdigest()[:8], 16)
        if req.json_mode or req.task_type == "decision":
            text = json.dumps({"action": "idle", "reason": f"fake-{h % 1000}"})
        else:
            text = f"[fake:{req.task_type}:{h % 10000}]"
        return LLMResponse(text, self.name, self.model, len(req.prompt) // 4, len(text) // 4)


class OpenAICompatProvider:
    """Any OpenAI-compatible /chat/completions endpoint (Groq, Gemini-compat, OpenRouter, local Ollama/vLLM...)."""

    def __init__(self, name: str, base_url: str, model: str, api_key_env: str | None, timeout: float = 60.0):
        self.name, self.base_url, self.model, self.timeout = name, base_url.rstrip("/"), model, timeout
        self.api_key = os.environ.get(api_key_env, "") if api_key_env else ""

    def complete(self, req: LLMRequest) -> LLMResponse:
        body = {
            "model": self.model,
            "messages": ([{"role": "system", "content": req.system}] if req.system else []) + [{"role": "user", "content": req.prompt}],
            "max_tokens": req.max_tokens,
            "temperature": req.temperature,
        }
        if req.json_mode:
            body["response_format"] = {"type": "json_object"}
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        http = urllib.request.Request(f"{self.base_url}/chat/completions", json.dumps(body).encode(), headers)
        try:
            with urllib.request.urlopen(http, timeout=self.timeout) as r:
                data = json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise ProviderError(f"{self.name} HTTP {e.code}", rate_limited=e.code == 429) from e
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            raise ProviderError(f"{self.name}: {e}") from e
        try:
            text = data["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError) as e:
            raise ProviderError(f"{self.name}: malformed response") from e
        u = data.get("usage", {})
        return LLMResponse(text, self.name, self.model, u.get("prompt_tokens", 0), u.get("completion_tokens", 0))


@dataclass
class Budget:
    global_daily: int = 10**9
    per_provider_daily: dict = field(default_factory=dict)
    _day: int = -1
    _global_used: int = 0
    _used: dict = field(default_factory=dict)

    def _roll(self, now: float) -> None:
        day = int(now // 86400)
        if day != self._day:
            self._day, self._global_used, self._used = day, 0, {}

    def allows(self, provider: str, now: float) -> bool:
        self._roll(now)
        return self._global_used < self.global_daily and self._used.get(provider, 0) < self.per_provider_daily.get(provider, 10**9)

    def charge(self, provider: str, now: float) -> None:
        self._roll(now)
        self._global_used += 1
        self._used[provider] = self._used.get(provider, 0) + 1


class LLMGateway:
    def __init__(self, tiers: dict[str, list], budget: Budget | None = None, now_fn=time.time, cooldown_s: float = 60.0):
        self.tiers, self.budget, self.now, self.cooldown_s = tiers, budget or Budget(), now_fn, cooldown_s
        self.cache: dict[str, LLMResponse] = {}
        self.cooldown_until: dict[str, float] = {}
        self.stats = {"calls": 0, "cache_hits": 0, "fallbacks": 0, "failures": 0, "in_tokens": 0, "out_tokens": 0}

    def _key(self, req: LLMRequest) -> str:
        return hashlib.sha256(json.dumps([req.task_type, req.system, req.prompt, req.tier, req.json_mode, req.max_tokens]).encode()).hexdigest()

    def _order(self, req: LLMRequest) -> list:
        providers = self.tiers.get(req.tier) or self.tiers.get("bulk", [])
        if not providers:
            return []
        start = int(hashlib.sha256((req.pin_key or "").encode()).hexdigest()[:8], 16) % len(providers) if req.pin_key else 0
        return providers[start:] + providers[:start]

    def complete(self, req: LLMRequest, validate=None) -> LLMResponse | None:
        key = self._key(req)
        if key in self.cache:
            self.stats["cache_hits"] += 1
            return LLMResponse(**{**self.cache[key].__dict__, "cached": True})
        now = self.now()
        for i, p in enumerate(self._order(req)):
            if self.cooldown_until.get(p.name, 0) > now or not self.budget.allows(p.name, now):
                continue
            try:
                self.budget.charge(p.name, now)
                resp = p.complete(req)
            except ProviderError as e:
                if e.rate_limited:
                    self.cooldown_until[p.name] = now + self.cooldown_s
                self.stats["fallbacks"] += 1
                continue
            if validate is not None and not validate(resp.text):
                self.stats["fallbacks"] += 1
                continue
            self.stats["calls"] += 1
            self.stats["in_tokens"] += resp.in_tokens
            self.stats["out_tokens"] += resp.out_tokens
            self.cache[key] = resp
            return resp
        self.stats["failures"] += 1
        return None


def load_gateway(path: str, env: dict | None = None, now_fn=time.time) -> LLMGateway:
    """Build a gateway from a TOML file. Providers whose API key env var is missing are skipped.
    A 'fake' provider is appended to every tier when `allow_fake = true`, so dev never hard-fails."""
    env = os.environ if env is None else env
    with open(path, "rb") as f:
        cfg = tomllib.load(f)
    providers = {}
    for name, c in cfg.get("providers", {}).items():
        if c.get("api_key_env") and not env.get(c["api_key_env"]):
            continue
        providers[name] = OpenAICompatProvider(name, c["base_url"], c["model"], c.get("api_key_env"))
    tiers = {t: [providers[n] for n in names if n in providers] for t, names in cfg.get("tiers", {}).items()}
    if cfg.get("allow_fake", True):
        for t in tiers:
            tiers[t].append(FakeProvider())
    b = cfg.get("budget", {})
    return LLMGateway(tiers, Budget(b.get("global_daily", 10**9), dict(b.get("per_provider_daily", {}))), now_fn)
