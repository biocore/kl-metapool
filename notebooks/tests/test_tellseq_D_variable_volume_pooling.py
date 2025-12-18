import unittest
from notebooks.tests.notebook_test_helpers import TestNotebook


class TestTellseqDNotebook(TestNotebook):
    NOTEBOOK = "tellseq_D_variable_volume_pooling.ipynb"

    def test_main_path(self):
        """Verify notebook produces expected output for iSeqnormed picklist."""

        run_params = {
            'plate_df_set_fp': (f"{self.test_output_dir}/QC/"
                                f"Tellseq_plate_df_C_set_col19to24.txt"),
            'read_counts_fps': [
                (f"{self.test_data_dir}/Demux/"
                 "Tellseq_fastqc_sequence_counts.tsv")],
            'reads_column': 'Raw Reads',
            'dynamic_range': 5,
        }

        output_params = {
            'iseqnormed_picklist_fbase': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/Pooling/Tellseq_iSeqnormpool'),
                self._FILE_PATH_KEY: False,
            },
            'iseqnormed_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/Pooling/Tellseq_iSeqnormpool_set_col19to24.txt'),
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
            },
        }

        self._run_notebook_test(run_params, output_params)


if __name__ == "__main__":
    unittest.main()
