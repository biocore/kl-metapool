import unittest
from notebooks.tests.notebook_test_helpers import TestNotebook


class TestTellseqBNotebook(TestNotebook):
    NOTEBOOK = "tellseq_B_concentration_estimation.ipynb"

    def test_main_path(self):
        """Verify notebook produces expected outputs."""

        run_params = {
            'full_plate_fp': (f"{self.test_output_dir}/QC/"
                              "Tellseq_plate_df_A.txt"),
            'lib_concs_fp': (f"{self.test_data_dir}/Quant/MiniPico/"
                             "Tellseq_clean_lib_quant.txt"),
        }

        output_params = {
            'plate_df_fbase': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/Tellseq',
                self._FILE_PATH_KEY: False,
            },
            'plate_df_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/Tellseq_plate_df_B.txt',
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
            },
        }

        self._run_notebook_test(run_params, output_params)

    def test_absquant_path(self):
        """Verify notebook produces expected outputs for absquant."""

        run_params = {
            'full_plate_fp': (f"{self.test_output_dir}/QC/"
                              "Tellseq_absquant_plate_df_A.txt"),
            'lib_concs_fp': (f"{self.test_data_dir}/Quant/MiniPico/"
                             "Tellseq_clean_lib_quant.txt"),
        }

        output_params = {
            'plate_df_fbase': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/Tellseq_absquant',
                self._FILE_PATH_KEY: False,
            },
            'plate_df_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/Tellseq_absquant_plate_df_B.txt',
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
            },
        }

        self._run_notebook_test(run_params, output_params)


if __name__ == "__main__":
    unittest.main()
