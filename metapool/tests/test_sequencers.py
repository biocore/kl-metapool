from metapool.sequencers import _deep_freeze, _get_machine_code, \
    get_model_and_center, get_sequencers_w_key_value, get_sequencer_type, \
    get_i5_index_sequencers, is_i5_revcomp_sequencer, \
    get_model_by_instrument_id, PROFILE_NAME_KEY
from types import MappingProxyType
from unittest import TestCase, main


class TestSequencers(TestCase):
    def test__get_machine_code(self):
        obs = _get_machine_code('K00180')
        self.assertEqual(obs, 'K')

        obs = _get_machine_code('D00611')
        self.assertEqual(obs, 'D')

        obs = _get_machine_code('MN01225')
        self.assertEqual(obs, 'MN')

    def test__get_machine_code_err(self):
        err = ("Cannot find a machine code; the instrument model "
               "'8675309' is malformed.")
        with self.assertRaisesRegex(ValueError, err):
            _get_machine_code('8675309')

    def test_get_model_by_instrument_id(self):
        """Test getting model by machine prefix."""
        obs = get_model_by_instrument_id('MN00178')
        self.assertEqual(obs, 'Illumina MiniSeq')

    def test_get_model_by_instrument_id_w_alternate_key(self):
        """Test getting alternate model name by machine prefix."""
        obs = get_model_by_instrument_id(
            'MN00178', model_key=PROFILE_NAME_KEY)
        self.assertEqual(obs, 'MiniSeq')

    def test_get_model_by_instrument_id_err_none(self):
        """Test error when no model found for machine prefix."""
        err = "Cannot find a machine code"
        with self.assertRaisesRegex(ValueError, err):
            get_model_by_instrument_id('MQ')

    def test_get_model_by_instrument_id_err_multiple(self):
        external_mapping = _deep_freeze({
            "MiniSeq": {
                'machine_prefix': 'MN',
                'model_name': 'Illumina MiniSeq',
            },
            "NovaSeqX": {
                'machine_prefix': 'LH',
                'model_name': 'Illumina NovaSeq X',
            },
            "NovaSeqXPlus": {
                'machine_prefix': 'LH',
                'model_name': 'Illumina NovaSeq X Plus',
            }
        })

        err = ("Found 2 sequencer types with machine_prefix 'LH': "
               "NovaSeqX, NovaSeqXPlus.")
        with self.assertRaisesRegex(ValueError, err):
            get_model_by_instrument_id(
                'LH1118920', sequencer_types=external_mapping)

    def test_get_model_and_center_by_model_prefix(self):
        obs = get_model_and_center('D32611_0365_G00DHB5YXX')
        self.assertEqual(obs, ('Illumina HiSeq 2500', 'UCSDMI'))

        obs = get_model_and_center('A86753_0365_G00DHB5YXX')
        self.assertEqual(obs, ('Illumina NovaSeq 6000', 'UCSDMI'))

    def test_get_model_and_center_by_instrument_id(self):
        obs = get_model_and_center('A00953_0032_AHWMGJDDXX')
        self.assertEqual(obs, ('Illumina NovaSeq 6000', 'IGM'))

        obs = get_model_and_center('A00169_8131_AHKXYNDHXX')
        self.assertEqual(obs, ('Illumina NovaSeq 6000', 'LJI'))

        obs = get_model_and_center('M05314_0255_000000000-J46T9')
        self.assertEqual(obs, ('Illumina MiSeq', 'KLM'))

        obs = get_model_and_center('K00180_0957_AHCYKKBBXY')
        self.assertEqual(obs, ('Illumina HiSeq 4000', 'IGM'))

        obs = get_model_and_center('D00611_0712_BH37W2BCX3_RKL0040')
        self.assertEqual(obs, ('Illumina HiSeq 2500', 'IGM'))

        obs = get_model_and_center('MN01225_0002_A000H2W3FY')
        self.assertEqual(obs, ('Illumina MiniSeq', 'CMI'))

    def test_get_model_and_center_by_model_prefix_err_no_match(self):
        err = ""
        with self.assertRaisesRegex(ValueError, err):
            get_model_and_center('MQ01225_0002_A000H2W3FY')

    def test_get_sequencers_w_key_value(self):
        """Test get sequencers with given key-value pair in default config."""
        obs = get_sequencers_w_key_value(
            'model_name', 'Illumina MiniSeq')
        self.assertEqual(len(obs), 1)
        self.assertEqual(obs["MiniSeq"]['machine_prefix'], 'MN')

    def test_get_sequencers_w_key_value_none(self):
        """Test no sequencers with given key-value pair in default config."""
        obs = get_sequencers_w_key_value(
            'model_name', 'Illumina YourSeq')
        self.assertEqual(len(obs), 0)

    def test_get_sequencers_w_key_value_w_external_mapping(self):
        """Test get sequencers with given key-value pair in external map."""
        external_mapping = _deep_freeze({
            "MiniSeq": {
                'machine_prefix': 'MN',
                'model_name': 'Illumina MiniSeq',
                'revcomp_samplesheet_i5_index': False,
                # extra key here that is present only for this sequencer
                # and not for others
                'delete_settings': ["MaskShortReads", "OverrideCycles"]
            },
            "NovaSeq6000": {
                'machine_prefix': 'A',
                'model_name': 'Illumina NovaSeq 6000',
                'revcomp_samplesheet_i5_index': True
            },
            "HiSeq2500": {
                'machine_prefix': 'D',
                'model_name': 'Illumina HiSeq 2500',
                'revcomp_samplesheet_i5_index': False
            },
            "HiSeq3000": {
                'machine_prefix': 'H',
                'model_name': 'Illumina HiSeq 3000',
                # No revcomp_samplesheet_i5_index key here, showing keys can
                # be omitted when not relevant
            }
        })

        obs = get_sequencers_w_key_value(
            'revcomp_samplesheet_i5_index', False,
            existing_types=external_mapping)
        self.assertEqual(len(obs), 2)
        self.assertIn('HiSeq2500', obs)
        self.assertEqual(len(obs['HiSeq2500']), 3)
        self.assertIn('MiniSeq', obs)
        self.assertEqual(len(obs['MiniSeq']), 4)

    def test_get_sequencers_w_key_value_err_malformed_mapping(self):
        """Test error getting sequencers w key-value pair in bad mapping."""
        external_mapping = MappingProxyType({
            "MiniSeq": _deep_freeze({
                'machine_prefix': 'MN',
                'model_name': 'Illumina MiniSeq',
                'revcomp_samplesheet_i5_index': False
            }),
            "NovaSeq6000": _deep_freeze({
                'machine_prefix': 'A',
                'model_name': 'Illumina NovaSeq 6000',
                'revcomp_samplesheet_i5_index': True
            }),
            "HiSeq2500": "red"
        })

        err = "Info for sequencer type 'HiSeq2500' is not a MappingProxyType."
        with self.assertRaisesRegex(ValueError, err):
            get_sequencers_w_key_value(
                'machine_prefix', 'A', existing_types=external_mapping)

    def test_get_sequencers_w_key_value_not_a_mapping(self):
        """Test error getting sequencers w key-value pair from bad input."""
        err = "existing_types must be a MappingProxyType or None."
        with self.assertRaisesRegex(ValueError, err):
            get_sequencers_w_key_value(
                'machine_prefix', 'A', existing_types='red')

    def test_get_i5_index_sequencers(self):
        external_mapping = _deep_freeze({
            "MiniSeq": {
                'machine_prefix': 'MN',
                'model_name': 'Illumina MiniSeq',
                'revcomp_samplesheet_i5_index': False
            },
            "NovaSeq6000": {
                'machine_prefix': 'A',
                'model_name': 'Illumina NovaSeq 6000',
                'revcomp_samplesheet_i5_index': True
            },
            "HiSeq2500": {
                # NB: has no revcomp_samplesheet_i5_index key so not returned
                'machine_prefix': 'D',
                'model_name': 'Illumina HiSeq 2500'
            }
        })

        obs = get_i5_index_sequencers(existing_types=external_mapping)
        self.assertEqual(len(obs), 2)
        self.assertIn('NovaSeq6000', obs)
        self.assertIn('MiniSeq', obs)

    def test_get_sequencer_type(self):
        external_mapping = MappingProxyType({
            "MiniSeq": {
                'machine_prefix': 'MN',
                'model_name': 'Illumina MiniSeq',
                'revcomp_samplesheet_i5_index': False
            },
            "NovaSeq6000": {
                'machine_prefix': 'A',
                'model_name': 'Illumina NovaSeq 6000',
                'revcomp_samplesheet_i5_index': True
            },
            "HiSeq2500": {
                'machine_prefix': 'D',
                'model_name': 'Illumina HiSeq 2500',
                'revcomp_samplesheet_i5_index': False
            }
        })

        obs = get_sequencer_type(
            'NovaSeq6000', existing_types=external_mapping)
        self.assertEqual(len(obs), 3)
        self.assertEqual(obs['machine_prefix'], 'A')
        self.assertEqual(obs['model_name'], 'Illumina NovaSeq 6000')
        self.assertEqual(obs['revcomp_samplesheet_i5_index'], True)

    def test_get_sequencer_type_err_not_found(self):
        """Test error when sequencer type not found."""
        err = "Sequencer type 'YourSeq' not found."
        with self.assertRaisesRegex(ValueError, err):
            get_sequencer_type('YourSeq')

    def test_is_i5_revcomp_sequencer_true(self):
        """Test result for sequencer that does revcomp i5."""
        obs = is_i5_revcomp_sequencer('HiSeq3000')
        self.assertTrue(obs)

    def test_is_i5_revcomp_sequencer_false(self):
        """Test result for sequencer that does not revcomp i5."""
        obs = is_i5_revcomp_sequencer('HiSeq1500')
        self.assertFalse(obs)

    def test_is_i5_revcomp_sequencer_err_not_found(self):
        """Test error when sequencer doesn't have i5 revcomp info."""
        external_mapping = MappingProxyType({
            "MiniSeq": {
                'machine_prefix': 'MN',
                'model_name': 'Illumina MiniSeq',
                'revcomp_samplesheet_i5_index': False
            },
            "NovaSeq6000": {
                # NB: no revcomp_samplesheet_i5_index key so not found
                'machine_prefix': 'A',
                'model_name': 'Illumina NovaSeq 6000'
            }
        })

        err = ("Sequencer type 'NovaSeq6000' does not have a "
               "'revcomp_samplesheet_i5_index' key in sequencer types.")
        with self.assertRaisesRegex(ValueError, err):
            is_i5_revcomp_sequencer('NovaSeq6000',
                                    existing_types=external_mapping)


if __name__ == "__main__":
    main()
