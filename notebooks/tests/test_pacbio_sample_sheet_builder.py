import unittest
from notebooks.tests.notebook_test_helpers import TestNotebook


class TestPacbioSampleSheetBuilderNotebook(TestNotebook):
    NOTEBOOK = "pacbio_sample_sheet_builder.ipynb"
    _ZERO_DATES_FUNC_KEY = "zero_dates_func"  # func to replace for dates

    def test_pacbio_v11_metag_case1_wo_amp_wo_absquant(self):
        run_params = {
            'processing_doc_fp': (
                f'{self.test_data_dir}/processing_docs/'
                f'pacbio_v11_metag_case1_without_amp_without_'
                f'absquant_processing_doc.csv'),
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
                "fecal samples for metagenomic sequencing",
            'contact_email': "g@example.com",
        }

        output_params = {
            'out_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/pacbio_v11_metag_sample_sheet_'
                     'case1_without_amp_without_absquant.csv'),
                self._FILE_PATH_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date
            }
        }

        self._run_notebook_test(run_params, output_params)

    def test_pacbio_v12_absquant_sample_sheet_case2_wo_amp_w_absquant(self):
        run_params = {
            'processing_doc_fp': (
                f'{self.test_data_dir}/processing_docs/'
                'pacbio_v12_absquant_case2_without_amp_'
                'with_absquant_processing_doc.csv'),
            'qiita_id_key': "Qiita_ID",
            'sample_name_col_key': "sample_name",
            'sample_type_key': "sample_type",
            'plate_col_key': "Extraction_Plate",
            'project_name_col_key': "Project_Name",
            'well_col_key': "Library_Well_ID",
            'twist_adaptor_id_col_key': None,
            'barcode_col_key': "Barcode",
            'run_id_key': "Sequencing Run",
            'run_title_key': "Sequencing Run Name",
            'experimental_design_desc':
                "fecal samples for metagenomic sequencing",
            'contact_email': "g@example.com",
            'sample_extract_metric': "calc_mass_sample_aliquot_input_g",
        }

        output_params = {
            'out_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/'
                     'pacbio_v12_absquant_sample_sheet_case2_without_amp_'
                     'with_absquant.csv'),
                self._FILE_PATH_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date
            }
        }

        self._run_notebook_test(run_params, output_params)

    def test_pacbio_v11_metag_sample_sheet_case3_w_amp_wo_absquant(self):
        run_params = {
            'processing_doc_fp': (
                f'{self.test_data_dir}/processing_docs/'
                f'pacbio_v11_metag_case3_with_amp_without_'
                f'absquant_processing_doc.csv'),
            'qiita_id_key': "Qiita_ID",
            'sample_name_col_key': "sample_name",
            'sample_type_key': "sample_type",
            'plate_col_key': "Extraction_Plate",
            'project_name_col_key': "Project_Name",
            'well_col_key': "Library_Well_ID",
            'twist_adaptor_id_col_key': 'Twist_UDI_Barcode',
            'barcode_col_key': "Barcode",
            'run_id_key': "Sequencing Run",
            'run_title_key': "Sequencing_Run_Name",
            'experimental_design_desc':
                "fecal samples for metagenomic sequencing",
            'contact_email': "g@example.com"
        }

        output_params = {
            'out_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/pacbio_v11_metag_sample_sheet_'
                     'case3_with_amp_without_absquant.csv'),
                self._FILE_PATH_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date
            }
        }

        self._run_notebook_test(run_params, output_params)

    def test_pacbio_v12_absquant_case4_w_amp_w_absquant_syndna_before(self):
        run_params = {
            'processing_doc_fp': (
                f'{self.test_data_dir}/processing_docs/'
                f'pacbio_v12_absquant_case4_with_amp_with_absquant_syndna_'
                f'before_processing_doc.csv'),
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
                "soil samples for metagenomic sequencing",
            'contact_email': "g@example.com",
            'sample_extract_metric': "sample_volume_ul",
        }

        output_params = {
            'out_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/'
                     'pacbio_v12_absquant_sample_sheet_case4_with_amp_'
                     'with_absquant_syndna_before.csv'),
                self._FILE_PATH_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date
            }
        }

        self._run_notebook_test(run_params, output_params)

    def test_pacbio_v12_absquant_case5_with_amp_with_absquant_syndna_after(self):  # noqa: E501
        run_params = {
            'processing_doc_fp': (
                f'{self.test_data_dir}/processing_docs/'
                f'pacbio_v12_absquant_case5_with_amp_with_absquant_syndna_'
                f'after_processing_doc.csv'),
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
                "fecal samples for metagenomic sequencing",
            'contact_email': "g@example.com",
            'sample_extract_metric': "sample_surface_area_cm2",
        }

        output_params = {
            'out_fp': {
                self._OUT_PARAM_VARIABLE_KEY:
                    ('{path}/SampleSheets/'
                     'pacbio_v12_absquant_sample_sheet_case5_with_amp_'
                     'with_absquant_syndna_after.csv'),
                self._FILE_PATH_KEY: True,
                self._ZERO_DATES_FUNC_KEY: self._replace_illumina_date
            }
        }

        self._run_notebook_test(run_params, output_params)


if __name__ == "__main__":
    unittest.main()
