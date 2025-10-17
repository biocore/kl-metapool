import unittest
import papermill as pm
import tempfile
from pathlib import Path
import os


class TestNotebook(unittest.TestCase):
    NOTEBOOK = "amplicon_pre_prep_file_generator.ipynb"

    def setUp(self):
        self.notebooks_dir = os.path.dirname(os.path.dirname(__file__))
        self.test_data_dir = os.path.join(self.notebooks_dir, 'test_data')
        self.test_output_dir = os.path.join(self.notebooks_dir, 'test_output')

    def _help_test_files_exact_text_match(self, file_1, file_2):
        with open(file_1, 'r', encoding='utf-8') as f1, \
                open(file_2, 'r', encoding='utf-8') as f2:
            text1 = f1.read()
            text2 = f2.read()
        self.assertMultiLineEqual(text1, text2)

    def _run_notebook_test(self, run_params, output_params):
        """Verify notebook produces expected output files."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            for curr_param in output_params:
                run_params[curr_param] = \
                    output_params[curr_param].format(path=tmp_path)

            pm.execute_notebook(
                input_path=f"{self.notebooks_dir}/{self.NOTEBOOK}",
                output_path=f"{tmp_path}/{self.NOTEBOOK}",
                parameters=run_params,
                log_output=True,
            )

            for curr_output_param in output_params:
                if not curr_output_param.endswith("fp"):
                    continue
                output_filename = output_params[curr_output_param]
                curr_generated_fp = output_filename.format(path=tmp_path)
                self.assertTrue(
                    os.path.exists(curr_generated_fp),
                    # note, intentionally not using full generated output fp,
                    # which will have a long temp directory folder name in it
                    msg=f"Notebook did not produce file at {output_filename}")

                curr_expected_fp = output_filename.format(
                    path=os.path.join(self.test_output_dir, "amplicon"))
                self.maxDiff = None
                # confirm that the written file matches the original
                self._help_test_files_exact_text_match(
                    curr_generated_fp, curr_expected_fp)
