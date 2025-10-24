import unittest
from notebooks.tests.notebook_test_helpers import TestNotebook

class TestMatrixTubePipelineSeqcountNormNotebook(TestNotebook):
    NOTEBOOK = "matrix_tube_pipeline_seqcount_norm.ipynb"

    def _make_params(self):
        run_params = {
            # Part 1 Step 0 inputs
            'expt_name': 'RKL4982',
            'plate_counter': 144,

            # Part 1 Step 0 studies_info
            'studies_info': [
                {
                    'Project Name': 'Celeste_Adaptation_12986',
                    'Project Abbreviation': 'ADAPT',
                    'sample_accession_fp': f'{self.test_data_dir}/Plate_Maps/sa_file_1.tsv',
                    'qiita_metadata_fp': f'{self.test_data_dir}/Plate_Maps/12986_20230314-090655.txt',
                    'experiment_design_description': 'isolate sequencing',
                    'HumanFiltering': 'False',
                    'Email': 'r@gmail.com'
                },
                {
                    'Project Name': 'TestProjB_10001',
                    'Project Abbreviation': 'TestProjB',
                    'sample_accession_fp': f'{self.test_data_dir}/Plate_Maps/sa_file_2.tsv',
                    'qiita_metadata_fp': f'{self.test_data_dir}/Plate_Maps/10001_20240503-090339.txt',
                    'experiment_design_description': 'whole genome sequencing',
                    'HumanFiltering': 'True',
                    'Email': 'l@ucsd.edu'
                },
                {
                    'Project Name': 'Celeste_Marmoset_14577',
                    'Project Abbreviation': 'MARMO',
                    'sample_accession_fp': f'{self.test_data_dir}/Plate_Maps/sa_file_3.tsv',
                    'qiita_metadata_fp': f'{self.test_data_dir}/Plate_Maps/14577_20230711-082202.txt',
                    'experiment_design_description': 'whole genome sequencing',
                    'HumanFiltering': 'False',
                    'Email': 'c@ucsd.edu'
                }
            ],

            # Part 1 Step 0 compression_layout
            'compression_layout': [
                {
                    'Plate Position': 1,
                    'Plate map file': f'{self.test_data_dir}/Plate_Maps/2022_summer_Celeste_Adaptation_16_plate_map.tsv',
                    'Project Name': 'Celeste_Adaptation_12986',
                    'Project Plate': 'Plate_16',
                    'Plate elution volume': 110
                },
                {
                    'Plate Position': 2,
                    'Plate map file': f'{self.test_data_dir}/Plate_Maps/2022_summer_Celeste_Adaptation_17_plate_map.tsv',
                    'Project Name': 'Celeste_Adaptation_12986',
                    'Project Plate': 'Plate_17',
                    'Plate elution volume': 110
                },
                {
                    'Plate Position': 3,
                    'Plate map file': f'{self.test_data_dir}/Plate_Maps/2022_summer_Celeste_Adaptation_18_plate_map.tsv',
                    'Project Name': 'Celeste_Adaptation_12986',
                    'Project Plate': 'Plate_18',
                    'Plate elution volume': 110
                },
                {
                    'Plate Position': 4,
                    'Plate map file': f'{self.test_data_dir}/Plate_Maps/TestProjB_1000_plate_map.tsv',
                    'Project Name': 'TestProjB_10001',
                    'Project Plate': 'Plate_1000',
                    'Plate elution volume': 110
                }
            ],

            # Part 1 Step 3 inputs
            'blanks_dir': f'{self.test_data_dir}/BLANKS',
            'katharoseq_dir': None,

            # Part 1 Step 5 inputs
            'sample_concs_fp': f'{self.test_data_dir}/Quant/MiniPico/2022_07_Celeste_Adaptation_16_17_18_21_gDNA_quant.txt',

            # Part 1 Step 5 (replicates section) inputs
            'replicate_dict': None,
            'well_col': 'Library Well',

            # Part 1 Step 6 inputs (verify defaults)
            'ng': 5,
            'total_vol': 3500,
            'min_vol': 25,
            'resolution': 2.5,

            # Part 1 Step 7 inputs (optional syndna)
            'syndna_pool_number': None,
            'undiluted_gdna_conc_fp': f'{self.test_data_dir}/Quant/MiniPico/2022_07_Celeste_Adaptation_16_17_18_21_gDNA_quant.txt',

            # Part 2 Step 2 inputs
            # NB: this is stored in the outputs dir historically but isn't an
            # output of the notebook -_-
            'index_combo_fp': f'{self.test_output_dir}/iTru/new_iTru_combos_Dec2017.csv',

            # Part 3 Step 1 inputs
            'lib_concs_fp': f'{self.test_data_dir}/Quant/MiniPico/2022_07_Celeste_Adaptation_16_17_18_21_CleanLib_quant.txt',

            # Part 3 Step 3 inputs
            'evp_total_vol': 190,

            # Part 3 Step 7 inputs
            'iseq_lanes': [1],
            'novaseq_sequencer': 'NovaSeqXPlus',
            'novaseq_lanes': [1],

            # Part 4 Step 1 inputs
            'read_counts_fps': [
                f'{self.test_data_dir}/Demux/YYYY_MM_DD_Celeste_Adaptation_raw_counts.tsv',
                f'{self.test_data_dir}/Demux/YYYY_MM_DD_Celeste_Marmoset_raw_counts.tsv',
                f'{self.test_data_dir}/Demux/YYYY_MM_DD_TestProjB_raw_counts.tsv'
            ],
            'READ_COUNTS_SAMPLE_KEY': 'Category',

            # Part 4 Step 2 inputs
            'dynamic_range': 5
        }

        output_params = {
            # Part 1 Step 8 output
            'norm_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/Input_Norm/YYYY_MM_DD_Celeste_Adaptation_16-21_inputnorm.txt',
                self._FILE_PATH_KEY: True
            },
            # Part 2 Step 3 output
            'index_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/Indices/YYYY_MM_DD_Celeste_Adaptation_16-21_indices_matrix.txt',
                self._FILE_PATH_KEY: True
            },

            # Part 3 Step 5 output
            'evp_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/Pooling/YYYY_MM_DD_Celeste_Adaptation_evp.csv',
                self._FILE_PATH_KEY: True
            },

            # Part 3 Step 6 output
            'plate_df_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/QC/YYYY_MM_DD_Celeste_Adaptation_matrix_df.txt',
                self._FILE_PATH_KEY: True
            },

            # Part 3 Step 7 outputs
            'iseq_sample_sheet_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/SampleSheets/YYYY_MM_DD_Celeste_Adaptation_12986_16_17_18_21_matrix_samplesheet_iseq.csv',
                self._FILE_PATH_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date
            },
            'novaseq_sample_sheet_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/SampleSheets/YYYY_MM_DD_Celeste_Adaptation_12986_16_17_18_21_matrix_samplesheet_novaseq.csv',
                self._FILE_PATH_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date
            },

            # Part 4 Step 4 output
            'iseqnormed_picklist_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    '{path}/Pooling/YYYY_MM_DD_Celeste_Adaptation_16_17_18_21_iSeqnormpool.csv',
                self._FILE_PATH_KEY: True
            }
        }
        return run_params, output_params

    def test_matrix_tube_pipeline_standard_metag(self):
        """Verify notebook produces expected output files."""

        run_params, output_params = self._make_params()
        self._run_notebook_test(run_params, output_params)

    def test_matrix_tube_pipeline_absquant_metag(self):
        """Verify notebook produces expected output files."""

        run_params, output_params = self._make_params()

        run_params['syndna_pool_number'] = 1

        # add optional syndna output
        # Part 1 Step 7 output (optional syndna)
        output_params['syndna_picklist_fp'] = {
            self._OUT_PARAM_VARIABLE_KEY:
                '{path}/Input_Norm/YYYY_MM_DD_Celeste_Adaptation_16-21_matrix_syndna_absquant.txt',
            self._FILE_PATH_KEY: True
        }

        # update other outputs that change with absquant
        # Part 3 Step 6 output
        output_params['plate_df_fp'] = {
            self._OUT_PARAM_VARIABLE_KEY:
                '{path}/QC/YYYY_MM_DD_Celeste_Adaptation_matrix_df_absquant.txt',
            self._FILE_PATH_KEY: True
        }
        # Part 3 Step 7 outputs
        output_params['iseq_sample_sheet_fp'] = {
            self._OUT_PARAM_VARIABLE_KEY:
                '{path}/SampleSheets/YYYY_MM_DD_Celeste_Adaptation_12986_16_17_18_21_matrix_samplesheet_iseq_absquant.csv',
            self._FILE_PATH_KEY: True,
            self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date
        }
        output_params['novaseq_sample_sheet_fp'] = {
            self._OUT_PARAM_VARIABLE_KEY:
                '{path}/SampleSheets/YYYY_MM_DD_Celeste_Adaptation_12986_16_17_18_21_matrix_samplesheet_novaseq_absquant.csv',
            self._FILE_PATH_KEY: True,
            self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date
        }

        self._run_notebook_test(run_params, output_params)

if __name__ == "__main__":
    unittest.main()
