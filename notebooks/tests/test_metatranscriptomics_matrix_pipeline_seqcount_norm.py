import unittest
from notebooks.tests.notebook_test_helpers import TestNotebook


class TestMetatranscriptomicsMatrixPipelineSeqcountNormNotebook(TestNotebook):
    NOTEBOOK = "metatranscriptomics_matrix_pipeline_seqcount_norm.ipynb"

    def _make_params(self):
        run_params = {
            # Step 1 inputs - sample accession files
            'sample_accession_fps': [
                (f'{self.test_data_dir}/Plate_Maps/2024_NPH_007 '
                 'Sample Processing spreadsheet_SAS KL_w_mmc.csv'),
                (f'{self.test_data_dir}/Plate_Maps/2024_NPH_008 '
                 'Sample Processing spreadsheet_SAS KL_w_mmc.csv'),
                (f'{self.test_data_dir}/Plate_Maps/2024_NPH_009 '
                 'Sample Processing spreadsheet_SAS KL_w_mmc.csv'),
                (f'{self.test_data_dir}/Plate_Maps/2024_NPH_010 '
                 'Sample Processing spreadsheet_SAS KL_w_mmc.csv')
            ],

            # Step 2 input - Qiita metadata
            'metadata_fp': (f'{self.test_data_dir}/Plate_Maps/'
                            '15288_20240807-120030.txt'),

            # Step 3 inputs - compression layout
            'compression_layout': [
                {
                    'Plate Position': 1,
                    'Plate map file': (f'{self.test_data_dir}/Plate_Maps/'
                                       '2024_NPH_Plate_7.tsv'),
                    'Project Name': 'NPH_15288',
                    'Project Plate': 'Plate_7',
                    'Project Abbreviation': 'NPH',
                    'Plate elution volume': 70
                },
                {
                    'Plate Position': 2,
                    'Plate map file': (f'{self.test_data_dir}/Plate_Maps/'
                                       '2024_NPH_Plate_8.tsv'),
                    'Project Name': 'NPH_15288',
                    'Project Plate': 'Plate_8',
                    'Project Abbreviation': 'NPH',
                    'Plate elution volume': 70
                },
                {
                    'Plate Position': 3,
                    'Plate map file': (f'{self.test_data_dir}/Plate_Maps/'
                                       '2024_NPH_Plate_9.tsv'),
                    'Project Name': 'NPH_15288',
                    'Project Plate': 'Plate_9',
                    'Project Abbreviation': 'NPH',
                    'Plate elution volume': 70
                },
                {
                    'Plate Position': 4,
                    'Plate map file': (f'{self.test_data_dir}/Plate_Maps/'
                                       '2024_NPH_Plate_10.tsv'),
                    'Project Name': 'NPH_15288',
                    'Project Plate': 'Plate_10',
                    'Project Abbreviation': 'NPH',
                    'Plate elution volume': 70
                }
            ],

            # Step 3 controls inputs
            'blanks_dir': f'{self.test_data_dir}/BLANKS',
            'katharoseq_dir': None,

            # Step 4 inputs - DNA/RNA quantification
            'sample_dna_concs_fp':
            (f'{self.test_data_dir}/Quant/MiniPico/'
             '2024_NPH_Plates_7-10_initial_gDNA_quant.txt'),
            'sample_rna_concs_fp':
            (f'{self.test_data_dir}/Quant/MiniPico/'
             '2024_NPH_Plates_7-10_initial_RNA_quant.txt'),

            # Step 4 threshold input
            'threshold': 40,

            # Post DNAse QC inputs
            'dnase_dna_concs_fp': (f'{self.test_data_dir}/Quant/MiniPico/'
                                   '2024_NPH_Plates_7-10_Post_DNase_DNA_'
                                   'Quant.txt'),
            'dnase_rna_concs_fp': (f'{self.test_data_dir}/Quant/MiniPico/'
                                   '2024_NPH_Plates_7-10_Post_DNase_RNA_'
                                   'Quant.txt'),

            # cDNA quantification input
            'cdna_concs_fp': (f'{self.test_data_dir}/Quant/MiniPico/'
                              '2024_NPH_Plates_7-10_initial_cDNA_quant.txt'),

            # Confirm no replicates
            'well_col': 'Library Well',

            # Normalization parameters (verify defaults)
            'ng': 50,
            'total_vol': 3500,
            'min_vol': 25,
            'resolution': 2.5,

            # Barcoding inputs
            'index_combo_fp': (f'{self.test_output_dir}/iTru/'
                               'new_iTru_combos_Dec2017.csv'),
            'plate_counter': 245,

            # Library quantification input
            'lib_concs_fp': (f'{self.test_data_dir}/Quant/MiniPico/'
                             '2024_NPH_Plates_7-10_clean_library_quant.txt'),

            # Sample sheet inputs
            'sequencer': 'iSeq',
            'lanes': [1],
            'metadata_dict': {
                'Bioinformatics': [
                    {
                        'Sample_Project': 'NPH_15288',
                        'QiitaID': '15288',
                        'BarcodesAreRC': 'True',
                        'ForwardAdapter': 'GATCGGAAGAGCACACGTCTGAACTCCAGTCAC',
                        'ReverseAdapter': 'GATCGGAAGAGCGTCGTGTAGGGAAAGGAGTGT',
                        'HumanFiltering': 'True',
                        'library_construction_protocol':
                            'Knight Lab Kapa HyperPlus',
                        'experiment_design_description':
                            'stool metatranscriptomics',
                    },
                ],
                'Contact': [
                    {
                        'Sample_Project': 'NPH_15288',
                        'Email': 'tboyer@health.ucsd.edu'
                    },
                ],
                'Assay': 'Metatranscriptomic',
                'SheetType': 'standard_metat',
                'SheetVersion': '10'
            },

            # Read distribution inputs
            'READ_COUNTS_SAMPLE_KEY': 'Category',
            'read_counts_fp': (
                f'{self.test_data_dir}/Demux/'
                '2024_NPH_7-10_fastqc_sequence_counts_plot_matrix.tsv'),
            'reads_column': 'Raw Reads',
        }

        output_params = {
            # Step 5 output - normalization picklist
            'norm_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/Input_Norm/'
                     'YYYY_MM_DD_NPH_7-10_matrix_inputnorm_metaT.txt'),
                self._FILE_PATH_KEY: True
            },

            # Step 2 Step 5 output - index picklist
            'index_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/Indices/'
                     'YYYY_MM_DD_NPH_7-10_matrix_indices_245_metaT.txt'),
                self._FILE_PATH_KEY: True
            },

            # Step 6 output - pooling picklist
            'evp_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/Pooling/YYYY_MM_DD_NPH_7-10_matrix_evp.csv'),
                self._FILE_PATH_KEY: True
            },

            # Plate dataframe output
            'plate_df_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/YYYY_MM_DD_NPH_7_10_matrix_df.txt',
                self._FILE_PATH_KEY: True
            },

            # Sample sheet output
            'sample_sheet_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/'
                     'YYYY_MM_DD_NPH_7-10_matrix_samplesheet_245.csv'),
                self._FILE_PATH_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date
            },

            # iSeq normalized pooling picklist output
            'picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/Pooling/'
                     'YYYY_MM_DD_NPH_7_10_matrix_iSeqnormpool.csv'),
                self._FILE_PATH_KEY: True
            }
        }

        return run_params, output_params

    def test_metatranscriptomics_matrix_pipeline(self):
        """Verify metatranscriptomics notebook makes expected output files."""

        run_params, output_params = self._make_params()
        self._run_notebook_test(run_params, output_params)


if __name__ == "__main__":
    unittest.main()
