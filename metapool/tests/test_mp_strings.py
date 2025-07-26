from unittest import TestCase

from metapool.mp_strings import _split_plate_name, \
    get_main_project_from_plate_name, get_plate_num_from_plate_name, \
    parse_project_name, get_short_name_and_id, \
    get_qiita_id_from_project_name, \
    QIITA_ID_KEY, PROJECT_SHORT_NAME_KEY, PROJECT_FULL_NAME_KEY


class TestMpStrings(TestCase):
    def test__split_plate_name_w_Plate(self):
        plate_name = "Celeste_Adaptation_12986_Plate_16"
        obs = _split_plate_name(plate_name)
        self.assertEqual(obs, ("Celeste_Adaptation_12986", "16"))

    def test__split_plate_name_wo_Plate(self):
        plate_name = "Celeste_Adaptation_12986_16"
        obs = _split_plate_name(plate_name)
        self.assertEqual(obs, ("Celeste_Adaptation_12986", "16"))

    def test__split_plate_name_malformed(self):
        plate_name = "CelesteAdaptation12986Plate16"
        err_msg = "Plate name 'CelesteAdaptation12986Plate16' is malformed."
        with self.assertRaisesRegex(ValueError, err_msg):
            _split_plate_name(plate_name)

    def test_get_main_project_from_plate_name_w_Plate(self):
        plate_name = "Celeste_Adaptation_12986_Plate_16"
        obs = get_main_project_from_plate_name(plate_name)
        self.assertEqual(obs, "Celeste_Adaptation_12986")

    def test_get_main_project_from_plate_name_wo_Plate(self):
        plate_name = "Celeste_Adaptation_12986_16"
        obs = get_main_project_from_plate_name(plate_name)
        self.assertEqual(obs, "Celeste_Adaptation_12986")

    def test_get_plate_num_from_plate_name_w_Plate(self):
        plate_name = "Celeste_Adaptation_12986_Plate_16"
        obs = get_plate_num_from_plate_name(plate_name)
        self.assertEqual(obs, "16")

    def test_get_plate_num_from_plate_name_wo_Plate(self):
        plate_name = "Celeste_Adaptation_12986_16"
        obs = get_plate_num_from_plate_name(plate_name)
        self.assertEqual(obs, "16")

    def test_parse_project_name(self):
        exp = {
            QIITA_ID_KEY: '1',
            PROJECT_SHORT_NAME_KEY: "project_green",
            PROJECT_FULL_NAME_KEY: "project_green_1"
        }
        obs = parse_project_name("project_green_1")
        self.assertDictEqual(exp, obs)

    def test_parse_project_name_err_no_project_name(self):
        expected_err = "project_name cannot be None or empty string"
        with self.assertRaisesRegex(ValueError, expected_err):
            parse_project_name(None)

        with self.assertRaisesRegex(ValueError, expected_err):
            parse_project_name("")

    def test_parse_project_name_err_no_qiita_id(self):
        with self.assertRaisesRegex(
                ValueError, "'project' does not contain a Qiita-ID."):
            parse_project_name("project")

        with self.assertRaisesRegex(
                ValueError, "'project_blue' does not contain a Qiita-ID."):
            parse_project_name("project_blue")

    def test_get_short_name_and_id(self):
        exp = ("A_ProjectF", "1161")
        obs = get_short_name_and_id("A_ProjectF_1161")
        self.assertEqual(obs, exp)

    def test_get_short_name_and_id_no_qiita_id(self):
        obs = get_short_name_and_id("A_ProjectF")
        self.assertEqual(obs, ("A_ProjectF", None))

    def test_get_qiita_id_from_project_name(self):
        obs = get_qiita_id_from_project_name("A_ProjectF_1161")
        self.assertEqual(obs, "1161")

    def test_get_qiita_id_from_project_name_err_no_qiita_id(self):
        with self.assertRaisesRegex(
                ValueError, "'A_ProjectF' does not contain a Qiita-ID."):
            get_qiita_id_from_project_name("A_ProjectF")

    def test_get_qiita_id_from_project_name_err_no_project_name(self):
        with self.assertRaisesRegex(
                ValueError, "project_name cannot be None or empty string"):
            get_qiita_id_from_project_name("")

        with self.assertRaisesRegex(
                ValueError, "project_name cannot be None or empty string"):
            get_qiita_id_from_project_name(None)
