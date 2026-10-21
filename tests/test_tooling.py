import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj
validator=module("validator","scripts/validate.py")
installer=module("installer","scripts/install.py")
bench=module("bench","scripts/benchmark.py")

class ToolingTests(unittest.TestCase):
    def test_static_validation(self):
        result=validator.check()
        self.assertTrue(result["ok"],result["errors"])
        self.assertEqual(result["skills"],28)
    def test_install_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as d:
            installer.install(d,apply=False)
            self.assertEqual(list(Path(d).iterdir()),[])
    def test_install_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/"AGENTS.md";target.write_text("original")
            installer.install(d,apply=True)
            self.assertEqual(target.read_text(),"original")
            self.assertTrue((Path(d)/".codex/config.toml").exists())
    def test_benchmark_synthetic(self):
        bench.summarize(ROOT/"benchmarks/example.jsonl")

if __name__=="__main__":unittest.main()
