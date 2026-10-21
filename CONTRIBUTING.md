# Contributing

Add skills with concise, precise `name` and `description` YAML frontmatter. Avoid descriptions such as "use for every coding task." Keep one primary workflow and put long examples into references.

Run `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v`. When changing routing, add a fixture to `tests/test_routing.py`. For model/cost claims provide reproducible task prompts, model IDs, token measurements, acceptance checks, and at least three repetitions. Do not claim synthetic examples as benchmarks.
