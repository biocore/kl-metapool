import unittest
from notebooks.tests.notebook_test_helpers import TestNotebook


class TestTellseqCNotebook(TestNotebook):
    NOTEBOOK = "tellseq_C_equal_volume_pooling.ipynb"

    def test_main_path(self):
        """Verify notebook produces expected outputs."""

        run_params = {
            'full_plate_fp': (f"{self.test_output_dir}/QC/"
                              "Tellseq_plate_df_B.txt"),
            'expt_config_fp': (f"{self.test_output_dir}/QC/"
                               "Tellseq_expt_info.yml"),
            'current_set_id': 'col19to24',
            'evp_total_vol': 190,
            'iseq_sequencer': 'iSeq',
            'novaseq_sequencer': 'NovaSeqXPlus',
        }

        output_params = {
            'evp_picklist_fbase': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/Indices/Tellseq_evp',
                self._FILE_PATH_KEY: False,
            },
            'evp_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/Indices/Tellseq_evp_set_col19to24.txt',
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
            },
            'machine_samplesheet_fbase': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/SampleSheets/Tellseq_samplesheet_instrument_iseq',
                self._FILE_PATH_KEY: False,
            },
            'machine_samplesheet_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/'
                     'Tellseq_samplesheet_instrument_iseq_set_col19to24.csv'),
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date,
            },
            'spp_samplesheet_fbase': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/SampleSheets/Tellseq_samplesheet_spp',
                self._FILE_PATH_KEY: False,
            },
            'iseq_spp_samplesheet_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/'
                     'Tellseq_samplesheet_spp_iseq_set_col19to24.csv'),
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date,
            },
            'novaseq_spp_samplesheet_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/'
                     'Tellseq_samplesheet_spp_novaseqxplus_set_col19to24.csv'),
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date,
            },
            'plate_set_base_dir': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/',
                self._FILE_PATH_KEY: False,

            },
            'plate_set_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/Tellseq_plate_df_C_set_col19to24.txt',
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
            },
        }

        self._run_notebook_test(run_params, output_params)

    def test_absquant_path(self):
        """Verify notebook produces expected outputs for absquant."""

        run_params = {
            'full_plate_fp': (f"{self.test_output_dir}/QC/"
                              "Tellseq_absquant_plate_df_B.txt"),
            'expt_config_fp': (f"{self.test_output_dir}/QC/"
                               "Tellseq_absquant_expt_info.yml"),
            'current_set_id': 'col19to24',
            'evp_total_vol': 190,
            'iseq_sequencer': 'iSeq',
            'novaseq_sequencer': 'NovaSeqXPlus',
        }

        output_params = {
            'evp_picklist_fbase': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/Indices/Tellseq_evp',
                self._FILE_PATH_KEY: False,
            },
            'evp_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/Indices/Tellseq_evp_set_col19to24.txt',
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
            },
            'machine_samplesheet_fbase': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/SampleSheets/'
                    'Tellseq_absquant_samplesheet_instrument_iseq',
                self._FILE_PATH_KEY: False,
            },
            'machine_samplesheet_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/'
                     'Tellseq_absquant_samplesheet_instrument_iseq'
                     '_set_col19to24.csv'),
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date,
            },
            'spp_samplesheet_fbase': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/SampleSheets/Tellseq_absquant_samplesheet_spp',
                self._FILE_PATH_KEY: False,
            },
            'iseq_spp_samplesheet_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/'
                     'Tellseq_absquant_samplesheet_spp'
                     '_iseq_set_col19to24.csv'),
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date,
            },
            'novaseq_spp_samplesheet_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/'
                     'Tellseq_absquant_samplesheet_spp_novaseqxplus'
                     '_set_col19to24.csv'),
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date,
            },
            'plate_set_base_dir': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/',
                self._FILE_PATH_KEY: False,

            },
            'plate_set_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/Tellseq_absquant_plate_df_C_set_col19to24.txt',
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
            },
        }

        self._run_notebook_test(run_params, output_params)

if __name__ == "__main__":
    unittest.main()
