"""Static deployment contract. Run: python3 -m unittest discover -s tools -p 'test_deployment.py'."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DeploymentTests(unittest.TestCase):
    def test_publish_only_generated_outputs(self):
        config = json.loads((ROOT / 'vercel.json').read_text())
        self.assertIsNone(config['framework'])
        self.assertEqual(config['installCommand'], '')
        self.assertEqual(config['buildCommand'], '')
        self.assertEqual(config['outputDirectory'], 'learning-library/out')
        output = ROOT / config['outputDirectory']
        expected = {'roadmap-app.html', 'Recruiter-TA-Library.pdf',
                    'Recruiter-TA-Library.docx', 'Recruiter-TA-Library.html',
                    'Recruiter-TA-Library.md'}
        self.assertEqual({p.name for p in output.iterdir()}, expected)
        self.assertTrue(all((output / name).is_file() for name in expected))

    def test_homepage_routes_to_tracker_without_catching_downloads(self):
        config = json.loads((ROOT / 'vercel.json').read_text())
        self.assertEqual(config['rewrites'], [
            {'source': '/', 'destination': '/roadmap-app.html'}])
        self.assertNotIn('redirects', config)
        tracker = ROOT / config['outputDirectory'] / 'roadmap-app.html'
        self.assertIn('id="pals-payload"', tracker.read_text())


if __name__ == '__main__':
    unittest.main()
