import unittest
import papermill as pm
import tempfile
from pathlib import Path
import os

NOTEBOOK = "tellseq_D_variable_volume_pooling.ipynb"
PICKLIST_FNAME = "Tellseq_iSeqnormpool_set_col19to24.txt"


class TestTellseqD(unittest.TestCase):
    def setUp(self):
        self.notebooks_dir = os.path.dirname(os.path.dirname(__file__))
        self.test_output_dir = os.path.join(self.notebooks_dir, 'test_output')

    def test_iseqnorm_picklist(self):
        """Verify notebook produces expected output for iSeqnormed picklist."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            run_params = {
                'test_dict': {
                    'plate_df_set_fp': f"{self.test_output_dir}/QC/"
                                       f"Tellseq_plate_df_C_set_col19to24.txt",
                    'read_counts_fps': [
                        f"{self.notebooks_dir}/test_data/Demux/"
                        f"Tellseq_fastqc_sequence_counts.tsv"],
                    'dynamic_range': 5,
                    'iseqnormed_picklist_fbase':
                        f"{tmp_path}/Tellseq_iSeqnormpool"
                }
            }

            pm.execute_notebook(
                input_path=f"{self.notebooks_dir}/{NOTEBOOK}",
                output_path=f"{tmp_path}/test_iseqnorm_picklist.ipynb",
                parameters=run_params,
                log_output=True,
            )

            out_iseqnormed_picklist_fp = f"{tmp_path}/{PICKLIST_FNAME}"
            self.assertTrue(os.path.exists(out_iseqnormed_picklist_fp),
                            msg="Notebook did not produce desired file.")

            exp_iseqnormed_fp = \
                f"{self.test_output_dir}/Pooling/{PICKLIST_FNAME}"
            with open(out_iseqnormed_picklist_fp, 'r') as out:
                with open(exp_iseqnormed_fp, 'r') as test:
                    out_lines = out.readlines()
                    test_lines = test.readlines()
                    for out_line, test_line in zip(out_lines,
                                                   test_lines):
                        self.assertEqual(out_line, test_line,
                                         msg=("Lines of output" +
                                              "and test don't match"))


if __name__ == "__main__":
    unittest.main()
