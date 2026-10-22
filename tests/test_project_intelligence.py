import importlib.util, tempfile, unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('project_intelligence',Path(__file__).resolve().parents[1]/'scripts/project_intelligence.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class ProjectIntelligenceTests(unittest.TestCase):
 def test_memory_persistence_dedup_and_scope(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   a=mod.remember(root,'decision','Keep public API stable',['src/a.py'],'verified-code')
   b=mod.remember(root,'decision','Keep public API stable',['src/a.py'],'verified-code')
   self.assertEqual(a['id'],b['id'])
   self.assertEqual(len(mod.recall(root,'public',['src/a.py'])),1)
   self.assertEqual(len(mod.recall(root,'public',['src/b.py'])),0)
   with self.assertRaises(ValueError):mod.remember(root,'decision','oops',['../outside'],'verified-code')
 def test_reverse_import_impact(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'lib.py').write_text('def f(): pass\n');(root/'app.py').write_text('import lib\n');(root/'test_app.py').write_text('import app\n')
   g,_=mod.graph.sync(root)
   r=mod.impact(g,['lib.py'])
   self.assertIn('app.py',r['affected']);self.assertIn('test_app.py',r['affected'])
   t=mod.test_candidates(root,g,r)
   self.assertEqual(t['suggested_tests'][0]['file'],'test_app.py')
 def test_no_test_candidates_for_unrelated_change(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'a.py').write_text('x=1\n');(root/'test_b.py').write_text('def test_b(): pass\n')
   g,_=mod.graph.sync(root);r=mod.impact(g,['a.py'])
   self.assertEqual(mod.test_candidates(root,g,r)['suggested_tests'],[])
if __name__=='__main__':unittest.main()
