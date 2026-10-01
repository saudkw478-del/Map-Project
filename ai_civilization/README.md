# AI Living Civilization

Observer-only simulation of an AI-driven society. Design: [`docs/DESIGN.md`](docs/DESIGN.md).

## Status
- **Phase 0 (done):** deterministic discrete-event engine, lazy needs, utility-AI routines, work/money ledger,
  proximity meetings, append-only SQLite event log, replay digest. **No LLM used.**
- **LLM Gateway (done, offline-tested only):** tiers, per-agent provider pinning, daily budgets, fallback, cache,
  OpenAI-compatible providers (Groq / Gemini / OpenRouter / local). Not yet tested against live APIs.

## Run
```bash
cd backend
pip install pytest          # only dev dependency; the engine itself has none
python -m pytest -q
python -m civ.cli.run_world --days 30 --seed 1 --timeline 1 --day 3
```
Same `--seed` => identical event digest (see `tests/test_core.py`).

## LLM providers (free tiers)
```bash
cp config/llm.toml.example config/llm.toml
export GROQ_API_KEY=...   GEMINI_API_KEY=...   # never commit keys
```
Free-tier limits change often; check each provider's current limits.
