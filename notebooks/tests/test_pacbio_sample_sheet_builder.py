import unittest
from notebooks.tests.notebook_test_helpers import TestNotebook


class TestPacbioSampleSheetBuilderNotebook(TestNotebook):
    NOTEBOOK = "pacbio_sample_sheet_builder.ipynb"

    def test_pacbio_v11_no_twist_metag(self):
        run_params = {
            # Part 1 Step 0 inputs
            'processing_doc_fp': (
                f'{self.test_data_dir}/processing_docs/'
                f'pacbio_metag_processing_doc.csv'),
            'qiita_id_key': "Qiita_ID",
            'sample_name_col_key': "sample_name",
            'sample_type_key': "sample_type",
            'plate_col_key': "Extraction_Plate",
            'project_name_col_key': "Project_Name",
            'well_col_key': "Library_Well_ID",
            'twist_adaptor_id_col_key': None,
            'barcode_col_key': "Barcode",
            'run_id_key': "Sequencing Run",
            'run_title_key': "Sequencing_Run_Name"
        }

        output_params = {
            # Part 1 Step 8 output
            'out_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/test_output/pacbio_v11_metag_sample_sheet.csv'),
                self._FILE_PATH_KEY: True
            }
        }

        self._run_notebook_test(run_params, output_params)

    def test_pacbio_v11_unpooled_absquant(self):
        run_params = {
            # Part 1 Step 0 inputs
            'processing_doc_fp': (
                f'{self.test_data_dir}/processing_docs/'
                f'pacbio_twist_unpooled_absquant_processing_doc.csv'),
            'qiita_id_key': "Qiita_ID",
            'sample_name_col_key': "sample_name",
            'sample_type_key': "sample_type",
            'plate_col_key': "Extraction_Plate",
            'project_name_col_key': "Project_Name",
            'well_col_key': "Library_Well_ID",
            'twist_adaptor_id_col_key': "Amplification_Twist_UDI",
            'barcode_col_key': "Barcode",
            'run_id_key': "Sequencing Run",
            'run_title_key': "Sequencing Run Name"
        }

        output_params = {
            # Part 1 Step 8 output
            'out_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/test_output/'
                     'pacbio_v11_absquant_unpooled_sample_sheet.csv'),
                self._FILE_PATH_KEY: True
            }
        }

        self._run_notebook_test(run_params, output_params)

    def test_pacbio_v11_pooled_absquant(self):
        """Verify notebook produces expected output files."""

        run_params = {
            # Part 1 Step 0 inputs
            'processing_doc_fp': (
                f'{self.test_data_dir}/processing_docs/'
                'pacbio_twist_pooled_absquant_processing_doc.csv'),
            'qiita_id_key': "Qiita_ID",
            'sample_name_col_key': "sample_name",
            'sample_type_key': "sample_type",
            'plate_col_key': "Extraction_Plate",
            'project_name_col_key': "Project_Name",
            'well_col_key': "Library_Well_ID",
            'twist_adaptor_id_col_key': "Amplification_Twist_UDI",
            'barcode_col_key': "Barcode",
            'run_id_key': "Sequencing Run",
            'run_title_key': "Sequencing Run Name"
        }

        output_params = {
            # Part 1 Step 8 output
            'out_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/test_output/'
                     'pacbio_v11_absquant_pooled_sample_sheet.csv'),
                self._FILE_PATH_KEY: True
            },
        }

        self._run_notebook_test(run_params, output_params)


if __name__ == "__main__":
    unittest.main()
