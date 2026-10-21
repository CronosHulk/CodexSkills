# Reproducible token benchmarks

Record real Codex runs in JSON Lines. For each task run the same acceptance tests and repeat at least three times per configuration. Use a fresh checkout at the same commit, same prompt, same environment and record actual model IDs.

Fields: `task_id`, `mode` (`baseline` or `optimized`), `model`, `input_tokens`, `output_tokens`, `success`; optionally `cached_input_tokens`, `duration_seconds`, `cost_usd`, `notes`.

Run `python3 scripts/benchmark.py benchmarks/example.jsonl`.

**Important:** total tokens are not equivalent to dollars. Dollar comparison requires actual model usage, cache rates and the applicable price table. The example below is synthetic and must not be presented as a real result.
