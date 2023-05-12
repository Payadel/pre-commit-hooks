import unittest
from unittest.mock import patch

from on_rails import ValidationError, assert_result_with_type

from pre_commit_hooks.document_oriented.main import main, process


class TestProcess(unittest.TestCase):
    def test_no_files_changed(self):
        result = process([], ['*.py'], ['*.md'])
        self.assertTrue(result.success)

    def test_source_and_docs_changed(self):
        result = process(['foo.py', 'bar.md'], ['*.py'], ['*.md'])
        self.assertTrue(result.success)

    def test_only_source_changed(self):
        result = process(['foo.py', 'bar.py'], ['*.py'], ['*.md'])

        self.assertFalse(result.success)
        self.assertEqual(result.detail.message,
                         '2 source files have been changed. It is necessary to update at least one document file.\n'
                         'changed files:\n[\'foo.py\', \'bar.py\']')


class TestMain(unittest.TestCase):
    @patch('sys.exit')
    def test_no_any_doc_pattern_provided(self, mock_exit):
        main([])
        mock_exit.assert_called_once_with(1)

    @patch('sys.exit')
    def test_no_any_src_pattern_provided(self, mock_exit):
        main(['-d', '*.md', '--doc', 'docs/*'
              ])
        mock_exit.assert_called_once_with(1)

    @patch('sys.exit')
    def test_no_any_src_changed(self, mock_exit):
        main(['-d', '*.md', '--doc', 'docs/*',
                                     '-s', 'fake/*'])
        mock_exit.assert_called_once_with(0)


if __name__ == '__main__':
    unittest.main()
