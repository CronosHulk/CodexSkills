import importlib.util
from pathlib import Path
import tempfile
import unittest
P=Path(__file__).resolve().parents[1]/'.agents/skills/graphify/scripts/graph.py'
spec=importlib.util.spec_from_file_location('graph_impl',P)
graph=importlib.util.module_from_spec(spec);spec.loader.exec_module(graph)
class GraphTests(unittest.TestCase):
    def test_incremental_and_query(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'alpha.py').write_text('def payment_auth(): pass\n')
            (root/'beta.py').write_text('import alpha\n')
            g,n=graph.sync(root)
            self.assertEqual(n,2)
            self.assertEqual(len(g['edges']),1)
            self.assertEqual(graph.query(g,'payment')[0]['file'],'alpha.py')
            self.assertEqual(graph.sync(root)[1],0)
            (root/'alpha.py').write_text('def payment_auth(): return True\n')
            self.assertEqual(graph.sync(root)[1],1)
if __name__=='__main__':unittest.main()
