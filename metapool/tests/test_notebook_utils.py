import unittest
import warnings
from metapool.notebook_utils import (
    get_studies_attr_list,
    pick_expected_separator
)


class TestGetStudiesAttrList(unittest.TestCase):
    """Tests for get_studies_attr_list function."""

    def test_extracts_single_attribute(self):
        """Test extracting a single attribute from studies list."""
        studies = [
            {'Project Name': 'ProjectA', 'Email': 'a@test.com'},
            {'Project Name': 'ProjectB', 'Email': 'b@test.com'},
        ]
        result = get_studies_attr_list(studies, 'Project Name')
        self.assertEqual(result, ['ProjectA', 'ProjectB'])

    def test_extracts_file_paths(self):
        """Test extracting file path attributes."""
        studies = [
            {'sample_accession_fp': '/path/to/file1.tsv'},
            {'sample_accession_fp': '/path/to/file2.tsv'},
            {'sample_accession_fp': '/path/to/file3.tsv'},
        ]
        result = get_studies_attr_list(studies, 'sample_accession_fp')
        self.assertEqual(result, [
            '/path/to/file1.tsv',
            '/path/to/file2.tsv',
            '/path/to/file3.tsv'
        ])

    def test_single_study(self):
        """Test with single study in list."""
        studies = [{'Email': 'test@example.com'}]
        result = get_studies_attr_list(studies, 'Email')
        self.assertEqual(result, ['test@example.com'])

    def test_empty_list(self):
        """Test with empty studies list."""
        result = get_studies_attr_list([], 'Project Name')
        self.assertEqual(result, [])


class TestPickExpectedSeparator(unittest.TestCase):
    """Tests for pick_expected_separator function."""

    def test_all_tsv_files(self):
        """Test separator detection with all .tsv files."""
        fps = ['file1.tsv', 'file2.tsv', 'file3.tsv']
        sep, visible_sep = pick_expected_separator(fps)
        self.assertEqual(sep, '\t')
        self.assertEqual(visible_sep, 'tab')

    def test_all_txt_files(self):
        """Test separator detection with all .txt files."""
        fps = ['file1.txt', 'file2.txt']
        sep, visible_sep = pick_expected_separator(fps)
        self.assertEqual(sep, '\t')
        self.assertEqual(visible_sep, 'tab')

    def test_all_csv_files(self):
        """Test separator detection with all .csv files."""
        fps = ['file1.csv', 'file2.csv', 'file3.csv']
        sep, visible_sep = pick_expected_separator(fps)
        self.assertEqual(sep, ',')
        self.assertEqual(visible_sep, 'comma')

    def test_mixed_tsv_txt(self):
        """Test separator detection with mixed .tsv and .txt files."""
        fps = ['file1.tsv', 'file2.txt', 'file3.tsv']
        sep, visible_sep = pick_expected_separator(fps)
        self.assertEqual(sep, '\t')
        self.assertEqual(visible_sep, 'tab')

    def test_mixed_extensions_warns(self):
        """Test that mixed csv and tsv files triggers warning."""
        fps = ['file1.csv', 'file2.tsv']
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            sep, visible_sep = pick_expected_separator(fps)
            # Should default to tab and warn
            self.assertEqual(sep, '\t')
            self.assertEqual(visible_sep, 'tab')
            self.assertEqual(len(w), 1)
            self.assertIn('Could not determine separator', str(w[0].message))

    def test_single_csv_file(self):
        """Test with single csv file."""
        fps = ['data.csv']
        sep, visible_sep = pick_expected_separator(fps)
        self.assertEqual(sep, ',')
        self.assertEqual(visible_sep, 'comma')

    def test_single_tsv_file(self):
        """Test with single tsv file."""
        fps = ['data.tsv']
        sep, visible_sep = pick_expected_separator(fps)
        self.assertEqual(sep, '\t')
        self.assertEqual(visible_sep, 'tab')

    def test_empty_list_warns(self):
        """Test that empty file list triggers warning and defaults to tab."""
        fps = []
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            sep, visible_sep = pick_expected_separator(fps)
            # Should default to tab and warn
            self.assertEqual(sep, '\t')
            self.assertEqual(visible_sep, 'tab')
            self.assertEqual(len(w), 1)
            self.assertIn('Could not determine separator', str(w[0].message))


if __name__ == '__main__':
    unittest.main()
