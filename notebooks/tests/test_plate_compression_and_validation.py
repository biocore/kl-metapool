import unittest
from notebooks.tests.notebook_test_helpers import TestNotebook


class TestPlateCompressionAndValidationNotebook(TestNotebook):
    NOTEBOOK = "plate_compression_and_validation.ipynb"

    def _make_standard_params(self):
        """Create standard test parameters for plate compression."""
        run_params = {
            'expt_name': 'RKL4982',

            'studies_info': [
                {
                    'Project Name': 'Celeste_Adaptation_12986',
                    'Project Abbreviation': 'ADAPT',
                    'sample_accession_fp':
                        f'{self.test_data_dir}/Plate_Maps/sa_file_1.tsv',
                    'qiita_metadata_fp': (f'{self.test_data_dir}/Plate_Maps/'
                                          f'12986_20230314-090655.txt'),
                    'experiment_design_description': 'isolate sequencing',
                    'HumanFiltering': 'False',
                    'Email': 'r@gmail.com'
                },
                {
                    'Project Name': 'TestProjB_10001',
                    'Project Abbreviation': 'TestProjB',
                    'sample_accession_fp':
                        f'{self.test_data_dir}/Plate_Maps/sa_file_2.tsv',
                    'qiita_metadata_fp': (f'{self.test_data_dir}/Plate_Maps/'
                                          f'10001_20240503-090339.txt'),
                    'experiment_design_description': 'whole genome sequencing',
                    'HumanFiltering': 'True',
                    'Email': 'l@ucsd.edu'
                },
                {
                    'Project Name': 'Celeste_Marmoset_14577',
                    'Project Abbreviation': 'MARMO',
                    'sample_accession_fp':
                        f'{self.test_data_dir}/Plate_Maps/sa_file_3.tsv',
                    'qiita_metadata_fp': (f'{self.test_data_dir}/Plate_Maps/'
                                          f'14577_20230711-082202.txt'),
                    'experiment_design_description': 'whole genome sequencing',
                    'HumanFiltering': 'False',
                    'Email': 'c@ucsd.edu'
                }
            ],

            'compression_layout': [
                {
                    'Plate Position': 1,
                    'Plate map file':
                        (f'{self.test_data_dir}/Plate_Maps/2022_summer_'
                         'Celeste_Adaptation_16_plate_map.tsv'),
                    'Project Name': 'Celeste_Adaptation_12986',
                    'Project Plate': 'Plate_16',
                    'Plate elution volume': 110
                },
                {
                    'Plate Position': 2,
                    'Plate map file':
                        (f'{self.test_data_dir}/Plate_Maps/2022_summer_'
                         'Celeste_Adaptation_17_plate_map.tsv'),
                    'Project Name': 'Celeste_Adaptation_12986',
                    'Project Plate': 'Plate_17',
                    'Plate elution volume': 110
                },
                {
                    'Plate Position': 3,
                    'Plate map file':
                        (f'{self.test_data_dir}/Plate_Maps/'
                         '2022_summer_Celeste_Adaptation_18_plate_map.tsv'),
                    'Project Name': 'Celeste_Adaptation_12986',
                    'Project Plate': 'Plate_18',
                    'Plate elution volume': 110
                },
                {
                    'Plate Position': 4,
                    'Plate map file':
                        (f'{self.test_data_dir}/Plate_Maps/'
                         'TestProjB_1000_plate_map.tsv'),
                    'Project Name': 'TestProjB_10001',
                    'Project Plate': 'Plate_1000',
                    'Plate elution volume': 110
                }
            ],

            'blanks_dir': f'{self.test_data_dir}/BLANKS',
            'katharoseq_dir': None,
        }

        output_params = {
            # file_name_base is passed to notebook; not a file output itself
            'file_name_base': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/ShotgunMetag',
                self._FILE_PATH_KEY: False,
            },
            # plate_df_fp is auto-constructed from file_name_base in notebook
            'plate_df_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/ShotgunMetag_plate_df_compvalid.txt',
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True
            },
            # expt_info_fp is auto-constructed from file_name_base in notebook
            'expt_info_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/ShotgunMetag_expt_info.yml',
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_local_test_paths
            }
        }

        return run_params, output_params

    def test_plate_compression_standard(self):
        """Verify notebook produces expected plate_df and expt_info files."""
        run_params, output_params = self._make_standard_params()
        self._run_notebook_test(run_params, output_params)


if __name__ == "__main__":
    unittest.main()
