import unittest
import papermill as pm
import tempfile
from pathlib import Path
import os
import re

SAVE_DIR = "~/Desktop"


class TestNotebook(unittest.TestCase):
    NOTEBOOK = "amplicon_pre_prep_file_generator.ipynb"
    _OUT_PARAM_VARIABLE_KEY = "param_variable"
    _FILE_PATH_KEY = "is_filepath"  # key for file path parameters
    _ZERO_DATES_FUNC_KEY = "zero_dates_func"  # func to replace for dates

    # TODO: turn off before committing
    _SAVE_UNMATCHED_OUTPUTS = True  # whether to save unmatched outputs

    def setUp(self):
        self.notebooks_dir = os.path.dirname(os.path.dirname(__file__))
        self.test_data_dir = os.path.join(self.notebooks_dir, 'test_data')
        self.test_output_dir = os.path.join(self.notebooks_dir, 'test_output')

    def _help_test_files_exact_text_match(self, file_1, file_2, filename=None,
                                          zero_dates_func=None):
        """Helper function to compare two text files for exact match."""

        filename = filename if not filename else f"{filename} "
        msg = f"{filename}files do not match exactly."
        self.maxDiff = None
        with open(file_1, 'r', encoding='utf-8') as f1, \
                open(file_2, 'r', encoding='utf-8') as f2:
            text1 = f1.read()
            text2 = f2.read()
            if zero_dates_func:
                text1 = zero_dates_func(text1)
                text2 = zero_dates_func(text2)
            try:
                self.assertMultiLineEqual(text1, text2, msg=msg)
            except AssertionError as e:
                if self._SAVE_UNMATCHED_OUTPUTS:
                    # save the unmatched output files for inspection
                    file_info = [(file_1, text1), (file_2, text2)]
                    for curr_index in range(len(file_info)):
                        curr_file, curr_text = file_info[curr_index]
                        base_name = os.path.basename(curr_file)
                        save_fp = os.path.join(
                            SAVE_DIR, f"UNMATCHED_{curr_index+1}_{base_name}")
                        with open(save_fp, 'w', encoding='utf-8') as sf:
                            sf.write(curr_text)

                raise e

    def _replace_illumina_date(self, text):
        """Helper function to replace illumina date strings in text."""

        date_pattern = r',\nDate,\d{4}-\d{2}-\d{2},'
        replacement = r',\nDate,0000-00-00,'
        return re.sub(date_pattern, replacement, text)

    def _run_notebook_test(self, run_params, out_param_details):
        """Verify notebook produces expected output files.

        Expects out_param_details to be a dict mapping output parameter name
        to a details dict containing at least `_OUT_PARAM_VARIABLE_KEY` and
        optionally `_FILE_PATH_KEY` and `_ZERO_DATES_FUNC_KEY`.
        """

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Populate run_params with formatted output paths and ensure
            # directories exist for any file path outputs.
            for curr_param_name, curr_details in out_param_details.items():
                curr_param_variable = \
                    curr_details[self._OUT_PARAM_VARIABLE_KEY]
                run_params[curr_param_name] = \
                    curr_param_variable.format(path=tmp_path)

                if curr_details.get(self._FILE_PATH_KEY, False):
                    # extract directory path by removing {path}/ and filename
                    dir_path = os.path.dirname(
                        curr_param_variable.replace("{path}/", ""))
                    # create any necessary directories in the temp path
                    full_dir_path = tmp_path / dir_path
                    os.makedirs(full_dir_path, exist_ok=True)
                # end if
            # next curr_param_details

            pm.execute_notebook(
                input_path=f"{self.notebooks_dir}/{self.NOTEBOOK}",
                output_path=f"{tmp_path}/{self.NOTEBOOK}",
                parameters=run_params,
                log_output=True,
            )

            # Validate that expected files were produced and contents match
            for curr_param_name, curr_details in out_param_details.items():
                if not curr_details.get(self._FILE_PATH_KEY, False):
                    continue
                curr_param_variable = \
                    curr_details[self._OUT_PARAM_VARIABLE_KEY]
                curr_param_zero_dates = \
                    curr_details.get(self._ZERO_DATES_FUNC_KEY, None)
                curr_generated_fp = curr_param_variable.format(path=tmp_path)
                self.assertTrue(
                    os.path.exists(curr_generated_fp),
                    # note, intentionally not using full generated output fp,
                    # which will have a long temp directory folder name in it
                    msg=(f"Notebook did not produce file at "
                         f"{curr_param_variable}"))

                curr_expected_fp = curr_param_variable.format(
                    path=self.test_output_dir)
                self.maxDiff = None

                # confirm that the written file matches the original
                self._help_test_files_exact_text_match(
                    curr_expected_fp, curr_generated_fp, curr_param_name,
                    zero_dates_func=curr_param_zero_dates)
