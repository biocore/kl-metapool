import unittest
from notebooks.tests.notebook_test_helpers import TestNotebook


class TestPacbioSampleSheetBuilderNotebook(TestNotebook):
    NOTEBOOK = "pacbio_sample_sheet_builder.ipynb"
    _ZERO_DATES_FUNC_KEY = "zero_dates_func"  # func to replace for dates

    def test_pacbio_v11_no_twist_metag(self):
        run_params = {
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
            'run_title_key': "Sequencing_Run_Name",
            'experimental_design_desc':
                "fecal samples for metagenomic sequencing"
        }

        output_params = {
            'out_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/pacbio_v11_metag_sample_sheet.csv'),
                self._FILE_PATH_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date
            }
        }

        self._run_notebook_test(run_params, output_params)

    def test_pacbio_v11_unpooled_absquant(self):
        run_params = {
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
            'run_title_key': "Sequencing Run Name",
            'experimental_design_desc':
                "fecal samples for metagenomic sequencing"
        }

        output_params = {
            'out_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/'
                     'pacbio_v11_absquant_unpooled_sample_sheet.csv'),
                self._FILE_PATH_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date
            }
        }

        self._run_notebook_test(run_params, output_params)

    def test_pacbio_v11_pooled_absquant(self):
        run_params = {
            'processing_doc_fp': (
                f'{self.test_data_dir}/processing_docs/'
                'pacbio_twist_pooled_absquant_processing_doc.csv'),
            'qiita_id_key': "Qiita_ID",
            'sample_name_col_key': "Sample_ID",
            'sample_type_key': "sample_type",
            'plate_col_key': "Extraction_Plate",
            'project_name_col_key': "Project_Name",
            'well_col_key': "Library_Well_ID",
            'twist_adaptor_id_col_key': "Twist_UDI_Barcode",
            'barcode_col_key': "Barcode",
            'run_id_key': "Sequencing Run",
            'run_title_key': "Sequencing Run Name",
            'experimental_design_desc':
                "soil samples for metagenomic sequencing"
        }

        output_params = {
            'out_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/'
                     'pacbio_v11_absquant_pooled_sample_sheet.csv'),
                self._FILE_PATH_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date
            }
        }

        self._run_notebook_test(run_params, output_params)


if __name__ == "__main__":
    unittest.main()
