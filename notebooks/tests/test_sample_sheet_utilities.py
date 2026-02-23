import unittest
from notebooks.tests.notebook_test_helpers import TestNotebook

# String constants for expected notebook output messages
SUCCESS_MSG = 'Success!'
ERROR_MSG = 'Error loading sample sheet'
SHEETTYPE_MSG = 'SheetType'


class TestSampleSheetUtilitiesNotebook(TestNotebook):
    NOTEBOOK = "sample_sheet_utilities.ipynb"

    def test_valid_sample_sheet(self):
        """Test that a valid sample sheet produces a Success message."""
        run_params = {
            'starting_dir': f'{self.test_output_dir}/SampleSheets',
            'sample_sheet_fp': (
                f'{self.test_output_dir}/SampleSheets/'
                f'YYYY_MM_DD_Celeste_Adaptation_12986_16_17_18_21'
                f'_matrix_samplesheet_novaseq_absquant.csv')
        }

        self._run_notebook_test(
            run_params, {},
            expected_strings=[SUCCESS_MSG],
            unexpected_strings=[ERROR_MSG]
        )

    def test_invalid_sample_sheet_missing_sheettype(self):
        """Test that an invalid sample sheet produces an Error message."""
        run_params = {
            'starting_dir': f'{self.test_output_dir}/SampleSheets',
            'sample_sheet_fp': (
                f'{self.test_output_dir}/SampleSheets/'
                f'invalid_sample_sheet_missing_sheettype.csv')
        }

        self._run_notebook_test(
            run_params, {},
            expected_strings=[ERROR_MSG, SHEETTYPE_MSG],
            unexpected_strings=[SUCCESS_MSG]
        )


if __name__ == "__main__":
    unittest.main()
