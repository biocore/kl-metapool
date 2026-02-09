import nbformat
import os
import papermill as pm
from pathlib import Path
import re
import tempfile
import unittest

SAVE_DIR = "~/Desktop"


class TestNotebook(unittest.TestCase):
    NOTEBOOK = "amplicon_pre_prep_file_generator.ipynb"
    _OUT_PARAM_VARIABLE_KEY = "param_variable"
    _FILE_PATH_KEY = "is_filepath"  # key for file path parameters
    _AUTOCONSTRUCTED_KEY = "is_autoconstructed"  # if param not set explicitly
    _AUTOCONSTRUCTED_FPS_KEY = "__TestNotebook_autoconstructed_fps"
    _ZERO_DATES_FUNC_KEY = "zero_dates_func"  # func to replace for dates

    # TODO: turn off before committing
    _SAVE_UNMATCHED_OUTPUTS = False  # whether to save unmatched outputs

    _TEST_DATA_DIR_NAME = "test_data"
    _TEST_OUTPUT_DIR_NAME = "test_output"

    def setUp(self):
        self.notebooks_dir = os.path.dirname(os.path.dirname(__file__))
        self.test_data_dir = os.path.join(
            self.notebooks_dir, self._TEST_DATA_DIR_NAME)
        self.test_output_dir = os.path.join(
            self.notebooks_dir, self._TEST_OUTPUT_DIR_NAME)

    def _help_test_files_exact_text_match(self, file_1, file_2, filename=None,
                                          zero_dates_func=None):
        """Helper function to compare two text files for exact match."""

        filename = f"{filename} " if filename else ""
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

    def _replace_local_test_paths(self, text):
        """Helper function to replace local directory paths in text."""

        for test_dir in [self._TEST_DATA_DIR_NAME, self._TEST_OUTPUT_DIR_NAME]:
            path_pattern = rf'(?<=:\s)(?:\.?/)?(?:[^/\s]+/)*{test_dir}/'
            replacement = f'/LOCAL/PATH/TO/{test_dir}/'
            text = re.sub(path_pattern, replacement, text)
        return text

    def _make_referenced_dir(self, input_path, tmp_path):
        # extract directory path by removing filename
        dir_path = os.path.dirname(input_path)
        # remove a leading '/' if present
        if dir_path.startswith('/'):
            dir_path = dir_path[1:]

        # create any necessary directories in the temp path
        full_dir_path = tmp_path / dir_path
        os.makedirs(full_dir_path, exist_ok=True)
        return full_dir_path

    def _run_notebook_test(self, run_params, out_param_details=None,
                           expected_strings=None, unexpected_strings=None):
        """Execute notebook and verify outputs (files and/or content).

        This unified method can test file outputs, notebook content strings,
        or both. At least one of out_param_details, expected_strings, or
        unexpected_strings should be provided.

        Parameters
        ----------
        run_params : dict
            Dictionary of parameter names to values to pass to papermill.
        out_param_details : dict, optional
            Dict mapping output parameter name to a details dict containing
            at least `_OUT_PARAM_VARIABLE_KEY` and optionally `_FILE_PATH_KEY`
            and `_ZERO_DATES_FUNC_KEY`. Used to validate output files.
        expected_strings : list of str, optional
            Strings that must appear in the notebook's cell outputs.
            Test fails if any expected string is not found.
        unexpected_strings : list of str, optional
            Strings that must NOT appear in the notebook's cell outputs.
            Test fails if any unexpected string is found.

        Raises
        ------
        AssertionError
            If output files don't match expected, or if expected strings
            are not found, or if unexpected strings are found.
        """

        out_param_details = out_param_details or {}
        expected_strings = expected_strings or []
        unexpected_strings = unexpected_strings or []

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            output_notebook_path = f"{tmp_path}/{self.NOTEBOOK}"

            autogenerated_input_fps = \
                run_params.get(self._AUTOCONSTRUCTED_FPS_KEY, [])
            run_params.pop(self._AUTOCONSTRUCTED_FPS_KEY, None)

            # Copy any autoconstructed input files to the temp dir
            # since that is where the code will automatically look for them
            for curr_autogenerated_input_name in autogenerated_input_fps:
                original_fp = run_params[curr_autogenerated_input_name]

                # remove self.test_data_dir or self.test_output_dir
                # and recreate directory structure in temp dir
                partial_path = original_fp.replace(
                    f"{self.test_data_dir}", "")
                partial_path = partial_path.replace(
                    f"{self.test_output_dir}", "")
                full_dir_path = self._make_referenced_dir(
                    partial_path, tmp_path)

                # copy autoconstructed input file paths to the temp dir
                filename = os.path.basename(partial_path)
                temp_fp = full_dir_path / filename
                with open(original_fp, 'r', encoding='utf-8') as src_f, \
                        open(temp_fp, 'w', encoding='utf-8') as dst_f:
                    dst_f.write(src_f.read())

                # update run_params to point to temp file path
                run_params[curr_autogenerated_input_name] = str(temp_fp)
            # next curr_run_param_name

            # Populate run_params with formatted output paths and ensure
            # directories exist for any file path outputs.
            for curr_out_param_name, curr_details in out_param_details.items():
                curr_param_variable = \
                    curr_details[self._OUT_PARAM_VARIABLE_KEY]

                if curr_details.get(self._FILE_PATH_KEY, False):
                    # remove directory path by removing {path}/
                    partial_path = curr_param_variable.replace("{path}/", "")
                    self._make_referenced_dir(partial_path, tmp_path)
                # end if

                # autoconstructed output variables are not explicitly set as
                # parameters; the code being tested should generate them itself
                if not curr_details.get(self._AUTOCONSTRUCTED_KEY, False):
                    run_params[curr_out_param_name] = \
                        curr_param_variable.format(path=tmp_path)
            # next curr_out_param_details

            pm.execute_notebook(
                input_path=f"{self.notebooks_dir}/{self.NOTEBOOK}",
                output_path=output_notebook_path,
                parameters=run_params,
                log_output=True,
            )

            # Validate output files if out_param_details provided
            for curr_run_param_name, curr_details in out_param_details.items():
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
                    curr_expected_fp, curr_generated_fp, curr_run_param_name,
                    zero_dates_func=curr_param_zero_dates)

            # Validate content strings if expected/unexpected strings provided
            if expected_strings or unexpected_strings:
                # Read the executed notebook and extract all cell outputs
                with open(output_notebook_path, 'r', encoding='utf-8') as f:
                    nb = nbformat.read(f, as_version=4)

                # Collect all text outputs from all cells
                all_outputs = []
                for cell in nb.cells:
                    if cell.cell_type == 'code' and 'outputs' in cell:
                        for output in cell['outputs']:
                            if output.get('output_type') == 'stream':
                                all_outputs.append(output.get('text', ''))
                            elif output.get('output_type') == 'execute_result':
                                data = output.get('data', {})
                                if 'text/plain' in data:
                                    all_outputs.append(data['text/plain'])
                            elif output.get('output_type') == 'error':
                                all_outputs.append(
                                    '\n'.join(output.get('traceback', [])))

                combined_output = '\n'.join(all_outputs)

                # Check for expected strings
                for expected in expected_strings:
                    msg = (f"Expected string '{expected}' not found in "
                           f"notebook output. Full output:\n{combined_output}")
                    self.assertIn(expected, combined_output, msg=msg)

                # Check for unexpected strings
                for unexpected in unexpected_strings:
                    msg = (f"Unexpected string '{unexpected}' found in "
                           f"notebook output. Full output:\n{combined_output}")
                    self.assertNotIn(unexpected, combined_output, msg=msg)
