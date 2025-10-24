import unittest
from notebooks.tests.notebook_test_helpers import TestNotebook


class TestAmpliconNotebook(TestNotebook):
    NOTEBOOK = "amplicon_pre_prep_file_generator.ipynb"

    def test_amplicon_main_path(self):
        """Verify notebook produces expected output files."""

        run_params = {
            'seq_type': '16S',
            'sample_accession_fp': f"{self.test_data_dir}/Plate_Maps/2022_summer_Celeste_Adaptation_16_17_18_21_sa_file.tsv",
            'metadata_fp': f"{self.test_data_dir}/Plate_Maps/12986_20230314-090655.txt",
            'compression_layout': [
                {
                    # top left plate
                    'Plate Position': '1',
                    'Primer Plate #': '1',
                    # VisionMate output
                    'Plate map file': f'{self.test_data_dir}/Plate_Maps/2022_summer_Celeste_Adaptation_16_plate_map.tsv',

                    # 'sample_plate': 'Celeste_Adaptation_12986_Plate_16', # PROJECTNAME_QIITA_ID_Plate_#
                    'Sample Plate': 'Plate_16',  # Plate_#
                    'Project Name': 'Celeste_Adaptation_12986',  # PROJECTNAME_QIITAID
                    'center_project_name': 'Celeste Adapt',  # what the wetlab calls the project
                    'Project Abbreviation': 'ADAPT',  # what the wetlab calls the project
                    # brief but specific project description
                    'experiment_design_description': '16S sequencing of antibiotic time series',
                    'Plate elution volume': '70',

                    'Plating': 'SF',  # initials
                    'Extraction Kit Lot': '166032128',
                    'Extraction Robot': 'Carmen_HOWE_KF3',
                    'TM1000 8 Tool': '109379Z',
                    'Primer Date': '2021-08-17',  # yyyy-mm-dd
                    'MasterMix Lot': '978215',
                    'Water Lot': 'RNBJ0628',
                    'TM10 8 Tool': '865HS8',
                    'Processing Robot': 'Echo550',
                    'TM300 8 Tool': 'not applicable',
                    'TM50 8 Tool': 'not applicable',
                    'instrument_model': 'Illumina MiSeq',
                    'run_date': '2023-03-02',  # date of MiSeq run
                    'Original Name': ''  # leave empty
                },
                {
                    # top right plate
                    'Plate Position': '2',
                    'Primer Plate #': '2',
                    'Plate map file': f'{self.test_data_dir}/Plate_Maps/2022_summer_Celeste_Adaptation_17_plate_map.tsv',

                    # 'sample_plate': 'Celeste_Adaptation_12986_Plate_17', # PROJECTNAME_QIITA_ID_Plate_#
                    'Sample Plate': 'Plate_17',  # Plate_#
                    'Project Name': 'Celeste_Adaptation_12986',
                    'center_project_name': 'Celeste Adapt',  # what the wetlab calls the project
                    'Project Abbreviation': 'ADAPT',
                    'experiment_design_description': '16S sequencing of antibiotic time series',
                    'Plate elution volume': '70',

                    'Plating': 'SF',
                    'Extraction Kit Lot': '166032128',
                    'Extraction Robot': 'Carmen_HOWE_KF3',
                    'TM1000 8 Tool': '109379Z',
                    'Primer Date': '2021-08-17',
                    'MasterMix Lot': '978215',
                    'Water Lot': 'RNBJ0628',
                    'TM10 8 Tool': '865HS8',
                    'Processing Robot': 'Echo550',
                    'TM300 8 Tool': 'not applicable',
                    'TM50 8 Tool': 'not applicable',
                    'instrument_model': 'Illumina MiSeq',
                    'run_date': '2023-03-02',
                    'Original Name': ''
                },
                {
                    # bottom left plate
                    'Plate Position': '3',
                    'Primer Plate #': '3',
                    'Plate map file': f'{self.test_data_dir}/Plate_Maps/2022_summer_Celeste_Adaptation_18_plate_map.tsv',
                    'Plate elution volume': '70',

                    # 'sample_plate': 'Celeste_Adaptation_12986_Plate_18', # PROJECTNAME_QIITA_ID_Plate_#
                    'Sample Plate': 'Plate_18',  # Plate_#
                    'Project Name': 'Celeste_Adaptation_12986',
                    'center_project_name': 'Celeste Adapt',  # what the wetlab calls the project
                    'Project Abbreviation': 'ADAPT',
                    'experiment_design_description': '16S sequencing of antibiotic time series',

                    'Plating': 'SF',
                    'Extraction Kit Lot': '166032128',
                    'Extraction Robot': 'Carmen_HOWE_KF3',
                    'TM1000 8 Tool': '109379Z',
                    'Primer Date': '2021-08-17',
                    'MasterMix Lot': '978215',
                    'Water Lot': 'RNBJ0628',
                    'TM10 8 Tool': '865HS8',
                    'Processing Robot': 'Echo550',
                    'TM300 8 Tool': 'not applicable',
                    'TM50 8 Tool': 'not applicable',
                    'instrument_model': 'Illumina MiSeq',
                    'run_date': '2023-03-02',
                    'Original Name': ''
                },
                {
                    # bottom right plate
                    'Plate Position': '4',
                    'Primer Plate #': '4',
                    'Plate map file': f'{self.test_data_dir}/Plate_Maps/2022_summer_Celeste_Adaptation_21_plate_map.tsv',
                    'Plate elution volume': '70',

                    # 'sample_plate': 'Celeste_Adaptation_12986_Plate_21', # PROJECTNAME_QIITA_ID_Plate_#
                    'Sample Plate': 'Plate_21',  # PROJECTNAME_QIITA_ID_Plate_#
                    'Project Name': 'Celeste_Adaptation_12986',
                    'center_project_name': 'Celeste Adapt',  # what the wetlab calls the project
                    'Project Abbreviation': 'ADAPT',
                    'experiment_design_description': '16S sequencing of antibiotic time series',

                    'Plating': 'SF',
                    'Extraction Kit Lot': '166032128',
                    'Extraction Robot': 'Carmen_HOWE_KF3',
                    'TM1000 8 Tool': '109379Z',
                    'Primer Date': '2021-08-17',
                    'MasterMix Lot': '978215',
                    'Water Lot': 'RNBJ0628',
                    'TM10 8 Tool': '865HS8',
                    'Processing Robot': 'Echo550',
                    'TM300 8 Tool': 'not applicable',
                    'TM50 8 Tool': 'not applicable',
                    'instrument_model': 'Illumina MiSeq',
                    'run_date': '2023-03-02',
                    'Original Name': ''
                },
            ],
            'well_col': 'Well',
            'blanks_dir': f'{self.test_data_dir}/BLANKS',
            'katharoseq_dir': None,
            'files': [f'{self.test_data_dir}/amplicon/20230201_IL515fBC_806r_ABTX_11052_174_178_182_185_MF_notebook_updated.txt'],
            'keep_these': ['ABTX_Plate_174', 'ABTX_Plate_178'],
        }

        output_params = {
            'output_filename': {
                self._OUT_PARAM_VARIABLE_KEY: '{path}/amplicon/20230302_IL515fBC_806_Celeste_Adaptation_12986_Plate_16_17_18_21.txt',
                self._FILE_PATH_KEY: True,
            },
            'merged_output_filename': {
                self._OUT_PARAM_VARIABLE_KEY: '{path}/amplicon/20230203_IL515fBC_806_ABTX_11052_Plates_174_178_182_185_ADAPT_12986_Plate_16_17_18_21_merged.txt',
                self._FILE_PATH_KEY: True,
            }
        }

        self._run_notebook_test(run_params, output_params)



if __name__ == "__main__":
    unittest.main()
