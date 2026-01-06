import unittest
from notebooks.tests.notebook_test_helpers import TestNotebook


class TestTellseqANotebook(TestNotebook):
    NOTEBOOK = "tellseq_A_compression_and_barcoding.ipynb"

    def test_main_path(self):
        """Verify notebook produces expected outputs."""

        run_params = {
            'expt_name': 'RKLtest',
            'arbitrary_compression_fp': None,
            'studies_info': [
                {
                    'Project Name': 'TestProjA_10002',
                    'Project Abbreviation': 'TestProjA',
                    'sample_accession_fp': (f"{self.test_data_dir}/Plate_Maps/"
                                            "Tellseq_TestProjA - 10002 - "
                                            "Sample Accession.csv"),
                    'qiita_metadata_fp': (f"{self.test_data_dir}/Plate_Maps/"
                                          "10002_20241004-110731.txt"),
                    'experiment_design_description': 'plasma sequencing',
                    'HumanFiltering': 'True',
                    'Email': 'r@gmail.com'
                }
            ],
            'compression_layout': [
                {
                    'Plate Position': 1,
                    'Plate map file': (f"{self.test_data_dir}/Plate_Maps/"
                                       "Tellseq_Test_Plate_1.tsv"),
                    'Project Name': 'TestProjA_10002',
                    'Project Plate': 'Plate_1',
                    'Plate elution volume': 70
                },
                {
                    'Plate Position': 2,
                    'Plate map file': (f"{self.test_data_dir}/Plate_Maps/"
                                       "Tellseq_Test_Plate_2.tsv"),
                    'Project Name': 'TestProjA_10002',
                    'Project Plate': 'Plate_2',
                    'Plate elution volume': 70
                },
                {
                    'Plate Position': 3,
                    'Plate map file': (f"{self.test_data_dir}/Plate_Maps/"
                                       "Tellseq_Test_Plate_3.tsv"),
                    'Project Name': 'TestProjA_10002',
                    'Project Plate': 'Plate_3',
                    'Plate elution volume': 70
                },
                {
                    'Plate Position': 4,
                    'Plate map file': (f"{self.test_data_dir}/Plate_Maps/"
                                       "Tellseq_Test_Plate_4.tsv"),
                    'Project Name': 'TestProjA_10002',
                    'Project Plate': 'Plate_4',
                    'Plate elution volume': 70
                },
            ],
            'blanks_dir': f"{self.test_data_dir}/BLANKS_for_tellseq",
            'katharoseq_dir': None,
            'dilutions_infos': {
                "10to1dilution": (f"{self.test_data_dir}/Quant/MiniPico/"
                                  "Tellseq_gDNA_diluted_10_to_1_Quant.txt"),
                "2to1dilution": (f"{self.test_data_dir}/Quant/MiniPico/"
                                 "Tellseq_gDNA_diluted_2_to_1_Quant.txt"),
                "undiluted": (f"{self.test_data_dir}/Quant/MiniPico/"
                              "Tellseq_gDNA_Original_Quant.txt")
            },
            'min_conc_threshold': 1.5,
            'replicate_dict': None,
            'ng': 7.5,
            'total_vol': 5000,
            'min_vol': 25,
            'resolution': 2.5,
            'syndna_pool_number': None,
            'undiluted_gdna_conc_fp': (f"{self.test_data_dir}/Quant/MiniPico/"
                                       "Tellseq_gDNA_Original_Quant.txt"),
            'barcodes_plate_name': ('TellSeq_Barcode_Plate_1_LN2409001_'
                                    'EXP052026'),
            'barcodes_fp': (f"{self.test_data_dir}/Tellseq/"
                            "TELL-Seq_Barcodes_PP_Primer_Plate - "
                            "PP_Primer_Position.csv"),
            'barcode_vol': 4000,
        }

        output_params = {
            # 'syndna_picklist_fp': {
            #     self._OUT_PARAM_VARIABLE_KEY:
            #         '{path}/Input_Norm/Tellseq_matrix_syndna_absquant.txt',
            #     self._FILE_PATH_KEY: True,
            # },
            'norm_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/Input_Norm/Tellseq_inputnorm.txt',
                self._FILE_PATH_KEY: True,
            },
            'barcode_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/Indices/Tellseq_barcode_matrix.txt',
                self._FILE_PATH_KEY: True,
            },
            'file_name_base': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/Tellseq',
                self._FILE_PATH_KEY: False,
            },
            'plate_df_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/Tellseq_plate_df_A.txt',
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
            },
            'expt_info_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/Tellseq_expt_info.yml',
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
                self._ZERO_DATES_FUNC_KEY:
                    self._replace_local_test_paths
            },
        }

        self._run_notebook_test(run_params, output_params)

    def test_absquant_path(self):
        """Verify notebook produces expected outputs for absquant."""

        run_params = {
            'expt_name': 'RKLtest',
            'arbitrary_compression_fp': None,
            'studies_info': [
                {
                    'Project Name': 'TestProjA_10002',
                    'Project Abbreviation': 'TestProjA',
                    'sample_accession_fp': (f"{self.test_data_dir}/Plate_Maps/"
                                            "Tellseq_TestProjA - 10002 - "
                                            "Sample Accession.csv"),
                    'qiita_metadata_fp': (f"{self.test_data_dir}/Plate_Maps/"
                                          "10002_20241004-110731.txt"),
                    'experiment_design_description': 'plasma sequencing',
                    'HumanFiltering': 'True',
                    'Email': 'r@gmail.com'
                }
            ],
            'compression_layout': [
                {
                    'Plate Position': 1,
                    'Plate map file': (f"{self.test_data_dir}/Plate_Maps/"
                                       "Tellseq_Test_Plate_1.tsv"),
                    'Project Name': 'TestProjA_10002',
                    'Project Plate': 'Plate_1',
                    'Plate elution volume': 70
                },
                {
                    'Plate Position': 2,
                    'Plate map file': (f"{self.test_data_dir}/Plate_Maps/"
                                       "Tellseq_Test_Plate_2.tsv"),
                    'Project Name': 'TestProjA_10002',
                    'Project Plate': 'Plate_2',
                    'Plate elution volume': 70
                },
                {
                    'Plate Position': 3,
                    'Plate map file': (f"{self.test_data_dir}/Plate_Maps/"
                                       "Tellseq_Test_Plate_3.tsv"),
                    'Project Name': 'TestProjA_10002',
                    'Project Plate': 'Plate_3',
                    'Plate elution volume': 70
                },
                {
                    'Plate Position': 4,
                    'Plate map file': (f"{self.test_data_dir}/Plate_Maps/"
                                       "Tellseq_Test_Plate_4.tsv"),
                    'Project Name': 'TestProjA_10002',
                    'Project Plate': 'Plate_4',
                    'Plate elution volume': 70
                },
            ],
            'blanks_dir': f"{self.test_data_dir}/BLANKS_for_tellseq",
            'katharoseq_dir': None,
            'dilutions_infos': {
                "10to1dilution": (f"{self.test_data_dir}/Quant/MiniPico/"
                                  "Tellseq_gDNA_diluted_10_to_1_Quant.txt"),
                "2to1dilution": (f"{self.test_data_dir}/Quant/MiniPico/"
                                 "Tellseq_gDNA_diluted_2_to_1_Quant.txt"),
                "undiluted": (f"{self.test_data_dir}/Quant/MiniPico/"
                              "Tellseq_gDNA_Original_Quant.txt")
            },
            'min_conc_threshold': 1.5,
            'replicate_dict': None,
            'ng': 7.5,
            'total_vol': 5000,
            'min_vol': 25,
            'resolution': 2.5,
            'syndna_pool_number': 1,
            'undiluted_gdna_conc_fp': (f"{self.test_data_dir}/Quant/MiniPico/"
                                       "Tellseq_gDNA_Original_Quant.txt"),
            'barcodes_plate_name': ('TellSeq_Barcode_Plate_1_LN2409001_'
                                    'EXP052026'),
            'barcodes_fp': (f"{self.test_data_dir}/Tellseq/"
                            "TELL-Seq_Barcodes_PP_Primer_Plate - "
                            "PP_Primer_Position.csv"),
            'barcode_vol': 4000,
        }

        output_params = {
            'syndna_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/Input_Norm/Tellseq_matrix_syndna_absquant.txt',
                self._FILE_PATH_KEY: True,
            },
            'norm_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/Input_Norm/Tellseq_absquant_inputnorm.txt',
                self._FILE_PATH_KEY: True,
            },
            'barcode_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/Indices/Tellseq_absquant_barcode_matrix.txt',
                self._FILE_PATH_KEY: True,
            },
            'file_name_base': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/Tellseq_absquant',
                self._FILE_PATH_KEY: False,
            },
            'plate_df_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/Tellseq_absquant_plate_df_A.txt',
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
            },
            'expt_info_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/Tellseq_absquant_expt_info.yml',
                self._FILE_PATH_KEY: True,
                self._AUTOCONSTRUCTED_KEY: True,
                self._ZERO_DATES_FUNC_KEY:
                    self._replace_local_test_paths
            },
        }

        self._run_notebook_test(run_params, output_params)

if __name__ == "__main__":
    unittest.main()
