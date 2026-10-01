import json

from civ.llm.gateway import Budget, FakeProvider, LLMGateway, LLMRequest, ProviderError, load_gateway


class Flaky:
    def __init__(self, name, error=None, text="ok"):
        self.name, self.model, self.error, self.text, self.calls = name, "m", error, text, 0

    def complete(self, req):
        self.calls += 1
        if self.error:
            raise self.error
        from civ.llm.gateway import LLMResponse
        return LLMResponse(self.text, self.name, "m", 10, 5)


def req(**kw):
    return LLMRequest(task_type="chat", prompt="hello", **kw)


def test_fake_provider_is_deterministic():
    f = FakeProvider()
    assert f.complete(req()).text == f.complete(req()).text


def test_fallback_on_rate_limit_and_cooldown():
    a = Flaky("a", ProviderError("429", rate_limited=True))
    b = Flaky("b", text="from-b")
    clock = [1000.0]
    g = LLMGateway({"bulk": [a, b]}, now_fn=lambda: clock[0], cooldown_s=60)
    assert g.complete(req()).text == "from-b"
    g.cache.clear()
    assert g.complete(req()).text == "from-b"
    assert a.calls == 1            # in cooldown, not retried
    clock[0] += 120
    g.cache.clear()
    g.complete(req())
    assert a.calls == 2            # cooldown expired


def test_all_fail_returns_none_for_code_fallback():
    g = LLMGateway({"bulk": [Flaky("a", ProviderError("boom"))]})
    assert g.complete(req()) is None and g.stats["failures"] == 1


def test_validation_failure_moves_to_next_provider():
    g = LLMGateway({"bulk": [Flaky("a", text="not json"), Flaky("b", text='{"x":1}')]})
    r = g.complete(req(), validate=lambda t: t.startswith("{") and bool(json.loads(t)))
    assert r.provider == "b"


def test_daily_budget_is_enforced_and_rolls_over():
    a = Flaky("a")
    clock = [0.0]
    g = LLMGateway({"bulk": [a]}, Budget(per_provider_daily={"a": 2}), now_fn=lambda: clock[0])
    for i in range(5):
        g.complete(LLMRequest(task_type="t", prompt=str(i)))
    assert a.calls == 2
    clock[0] += 86400
    g.complete(LLMRequest(task_type="t", prompt="new"))
    assert a.calls == 3


def test_pinning_gives_agent_a_stable_provider():
    a, b = Flaky("a", text="A"), Flaky("b", text="B")
    g = LLMGateway({"bulk": [a, b]})
    first = {k: g.complete(LLMRequest(task_type="t", prompt=f"p{i}", pin_key=k)).provider for i, k in enumerate(["agent:1", "agent:2"])}
    again = {k: g.complete(LLMRequest(task_type="t", prompt=f"q{i}", pin_key=k)).provider for i, k in enumerate(["agent:1", "agent:2"])}
    assert first == again


def test_cache_avoids_second_call():
    a = Flaky("a")
    g = LLMGateway({"bulk": [a]})
    g.complete(req()); r = g.complete(req())
    assert a.calls == 1 and r.cached


def test_load_gateway_skips_providers_without_keys(tmp_path):
    p = tmp_path / "llm.toml"
    p.write_text('allow_fake=true\n[providers.groq]\nbase_url="http://x"\nmodel="m"\napi_key_env="GROQ_API_KEY"\n[tiers]\nbulk=["groq"]\n')
    g = load_gateway(str(p), env={})
    assert [x.name for x in g.tiers["bulk"]] == ["fake"]
    g2 = load_gateway(str(p), env={"GROQ_API_KEY": "k"})
    assert [x.name for x in g2.tiers["bulk"]] == ["groq", "fake"]
