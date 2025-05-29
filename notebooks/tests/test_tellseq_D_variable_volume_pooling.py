# test_input_unittest.py
import unittest
import papermill as pm
import json
import tempfile
from pathlib import Path
import os

NOTEBOOK = "../tellseq_D_variable_volume_pooling.ipynb"
TEST_DICT = 'test_dict'


class TestTellseqD(unittest.TestCase):
    def test_is_eq_normed_output(self):
        """
        Executes the notebook with two different parameter sets and checks:
          1) the resulting CSV matches expected DataFrame
          2) the JSON of changed variables can be loaded
        """
        expected_fn = "test_is_eq_normed_output"
        plate_df_set_fp = ('../test_output/QC/' +
                           'Tellseq_plate_df_C_set_col19to24.txt')
        read_counts_fps = [('../test_data/Demux/' +
                            'Tellseq_fastqc_sequence_counts.tsv')]
        dynamic_range = 5

        # for params, expected_fn in PARAM_SETS:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            tmp_nb_dir = tmp_path / "nb"
            tmp_outputs_dir = tmp_path / "csv"
            tmp_nb_dir.mkdir()
            tmp_outputs_dir.mkdir()

            # paths for outputs
            dict_output = tmp_outputs_dir / f"dict{expected_fn}.txt"

            iseqnormed_picklist_fbase = (
                tmp_outputs_dir / "Tellseq_iSeqnormpool")

            run_params = {
                TEST_DICT: {
                    'plate_df_set_fp': plate_df_set_fp,
                    'read_counts_fps': read_counts_fps,
                    'dynamic_range': dynamic_range,
                    'iseqnormed_picklist_fbase': str(iseqnormed_picklist_fbase)
                },
                "test_notebook_output_csv": str(dict_output),
            }

            out_nb = tmp_nb_dir / f"{expected_fn}.ipynb"
            pm.execute_notebook(
                input_path=NOTEBOOK,
                output_path=str(out_nb),
                parameters=run_params,
                log_output=True,
            )

            # Test 1. Check the file writing as output of the method
            with open(dict_output, 'r') as f:
                changed_variables = json.load(f)
                output_iseqnormed_picklist_fp = (
                    changed_variables['iseqnormed_picklist_fp'])
                test_iseqnormed_fp = (
                    '../test_output/' +
                    'Pooling/' +
                    'Tellseq_iSeqnormpool_set_col19to24.txt'
                )
                self.assertTrue(os.path.exists(output_iseqnormed_picklist_fp),
                                msg="Notebook did not produce desired file.")
                with open(output_iseqnormed_picklist_fp, 'r') as out:
                    with open(test_iseqnormed_fp, 'r') as test:
                        out_lines = out.readlines()
                        test_lines = test.readlines()
                        for out_line, test_line in zip(out_lines,
                                                       test_lines):
                            self.assertEqual(out_line, test_line,
                                             msg=("Lines of output" +
                                                  "and test don't match"))


if __name__ == "__main__":
    unittest.main()
