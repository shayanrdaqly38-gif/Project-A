import tempfile
import unittest
from pathlib import Path
from docsignal import scan


class ScannerTests(unittest.TestCase):
    def audit(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'guide.md').write_text('# نصب\n# نصب\n', encoding='utf8')
            (root/'readme.md').write_text(text, encoding='utf8')
            return scan(root)

    def test_typo(self):
        issue, = self.audit('\n[x](guied.md)')['issues']
        self.assertEqual((issue['line'], issue['suggestion']), (2, 'guide.md'))

    def test_unicode_duplicate(self):
        self.assertEqual(self.audit('[x](guide.md#نصب-1)')['issues'], [])

    def test_missing_heading(self):
        self.assertEqual(self.audit('[x](guide.md#نصبی)')['issues'][0]['kind'], 'missing-heading')

    def test_skip_examples_and_remote(self):
        self.assertEqual(self.audit('````md\n```\n[x](a)\n````\n`[x](a)` [web](https://example.org)')['references'], 0)

    def test_boundary(self):
        self.assertEqual(self.audit('[x](../outside)')['issues'][0]['kind'], 'outside-root')
