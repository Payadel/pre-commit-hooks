import unittest

from on_rails import ValidationError, assert_result, assert_result_with_type

from pre_commit_hooks.document_oriented.args import get_args, validate_args


class TestParser(unittest.TestCase):
    def test_valid_args(self):
        args = ['-d', '*.docx', '--doc', '*.md',
                '-s', '*.py', '--source', 'src/*'
                ]

        result = get_args(args)

        self.assertTrue(result.success)
        self.assertEqual(result.value.docs, ['*.docx', '*.md'])
        self.assertEqual(result.value.sources, ['*.py', 'src/*'])

class TestValidateArgs(unittest.TestCase):
    def test_valid_args(self):
        doc_patterns = ['*.docx', '*.md']
        src_patterns = ['*.py', 'src/*']

        result = validate_args(doc_patterns, src_patterns)

        self.assertTrue(result.success)

    def test_invalid_args(self):
        doc_patterns = []
        src_patterns = ['*.py', 'src/*']
        result = validate_args(doc_patterns, src_patterns)
        assert_result_with_type(self, result, False, expected_detail_type=ValidationError)

        doc_patterns = ['*.docx', '*.md']
        src_patterns = []
        result = validate_args(doc_patterns, src_patterns)
        assert_result_with_type(self, result, False, expected_detail_type=ValidationError)

if __name__ == '__main__':
    unittest.main()
