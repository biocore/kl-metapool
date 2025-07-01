import os
import pandas
import re
from types import MappingProxyType
import yaml

DELETE_SETTINGS_KEY = "delete_settings"

_MACHINE_PREFIX_KEY = 'machine_prefix'
_MODEL_TYPE_KEY = 'model'
_MODEL_NAME_KEY = 'model_name'
_RUN_CENTER_KEY = 'run_center'
_REVCOMP_I5_KEY = "revcomp_samplesheet_i5_index"

_LAB_RUN_CENTER = "UCSDMI"
_SEQUENCER_TYPES_YML_FNAME = 'sequencer_types.yml'

# DEPRECATED: We no longer want to identify sequencer types by the
# instrument id, since that requires a change for every new physical machine.
# This is kept for backwards compatibility with existing data, but for anything
# new, we should use the instrument type instead.
# _MODEL_TYPE_KEY values must match up to a key in the sequencer_types.yml file.
_INSTRUMENT_LOOKUP = pandas.DataFrame({
    'FS10001773': {_MODEL_TYPE_KEY: 'iSeq', _RUN_CENTER_KEY: 'KLM'},
    'A00953': {_MODEL_TYPE_KEY: 'NovaSeq6000', _RUN_CENTER_KEY: 'IGM'},
    'A00169': {_MODEL_TYPE_KEY: 'NovaSeq6000', _RUN_CENTER_KEY: 'LJI'},
    'M05314': {_MODEL_TYPE_KEY: 'MiSeq', _RUN_CENTER_KEY: 'KLM'},
    'K00180': {_MODEL_TYPE_KEY: 'HiSeq4000', _RUN_CENTER_KEY: 'IGM'},
    'D00611': {_MODEL_TYPE_KEY: 'HiSeq2500', _RUN_CENTER_KEY: 'IGM'},
    'LH00444': {_MODEL_TYPE_KEY: 'NovaSeqX', _RUN_CENTER_KEY: 'IGM'},
    'SH00252': {_MODEL_TYPE_KEY: 'MiSeqi100', _RUN_CENTER_KEY: 'IGM'},
    'MN01225': {_MODEL_TYPE_KEY: 'MiniSeq', _RUN_CENTER_KEY: 'CMI'}}).T


def _load_sequencer_types(existing_types=None, test_only_fp=None):
    """Load sequencer types from yaml file.

    Returns
    -------
    MappingProxyType
        Immutable dictionary of sequencer types.
    """

    if existing_types is not None:
        # if an existing mapping is provided, use it
        if not isinstance(existing_types, MappingProxyType):
            raise ValueError(
                "existing_types must be a MappingProxyType or None.")
        return existing_types

    if test_only_fp is None:
        # get the path to the directory above the one this file is in
        grandmom_dir = \
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sequencers_fp = os.path.join(grandmom_dir, _SEQUENCER_TYPES_YML_FNAME)
    else:
        # for testing, use the provided file path
        sequencers_fp = test_only_fp

    with open(sequencers_fp, 'r') as file:
        sequencer_types = yaml.safe_load(file)

    immutable_sequencer_types = MappingProxyType(sequencer_types)
    return immutable_sequencer_types


def _get_machine_code(instrument_model):
    """Get the machine code for an instrument's code

    Parameters
    ----------
    instrument_model: str
        An instrument's model of the form A999999 or AA999999

    Returns
    -------
    """
    # the machine code represents the first 1 to 2 letters of the
    # instrument model
    machine_code = re.compile(r'^([a-zA-Z]{1,2})')
    matches = re.search(machine_code, instrument_model)
    if matches is None:
        raise ValueError('Cannot find a machine code. This instrument '
                         'model is malformed %s. The machine code is a '
                         'one or two character prefix.' % instrument_model)
    return matches[0]


def get_model_and_center(instrument_code):
    """Determine instrument model and center based on a lookup

    Parameters
    ----------
    instrument_code: str
        Instrument code from a run identifier.

    Returns
    -------
    str
        Instrument model.
    str
        Run center based on the machine's id.
    """

    run_center = _LAB_RUN_CENTER  # Default run center for lab data
    available_sequencer_types = _load_sequencer_types()

    instrument_id = instrument_code.split('_')[0]
    if instrument_id in _INSTRUMENT_LOOKUP.index:
        run_center = _INSTRUMENT_LOOKUP.loc[instrument_id, _RUN_CENTER_KEY]
        inst_model_type = _INSTRUMENT_LOOKUP.loc[instrument_id, _MODEL_TYPE_KEY]
    else:
        instrument_prefix = _get_machine_code(instrument_id)
        models_w_prefix = get_sequencers_w_key_value(
            _MACHINE_PREFIX_KEY, instrument_prefix,
            existing_types=available_sequencer_types)
        if len(models_w_prefix) == 0:
            raise ValueError(
                f"Unrecognized {_MACHINE_PREFIX_KEY} {instrument_prefix}")
        elif len(models_w_prefix) > 1:
            raise ValueError(
                f"Found {len(models_w_prefix)} sequencers found with "
                f"{_MACHINE_PREFIX_KEY} = '{instrument_prefix}'.")
        # end if got an unexpected number of sequencer types w given prefix
        inst_model_type = next(iter(models_w_prefix))
    # end if instrument_id is in the lookup or if must look up by prefix

    inst_sequencer_type = available_sequencer_types[inst_model_type]
    instrument_model = inst_sequencer_type[_MODEL_NAME_KEY]

    return instrument_model, run_center


def get_sequencers_w_key_value(key, value, default=None, existing_types=None):
    """Get sequencers with a specific key-value pair.

    Parameters
    ----------
    key: str
        The key to search for in the sequencer types.
    value: object
        The value to match for the given key.
    default: object, optional
        The default to use as value if key is not found in a sequencer type.
        Defaults to None.
    existing_types: MappingProxyType, optional
        A mapping of sequencer types to search in. If None, the
        sequencer types will be loaded from the YAML file.

    Returns
    -------
    MappingProxyType
        Immutable dictionary of sequencer types that match the key-value pair.
    """

    found_sequencers = {}
    sequencer_types = _load_sequencer_types(existing_types)
    for name, details in sequencer_types.items():
        if not isinstance(details, dict):
            raise ValueError(
                f"Info for sequencer type '{name}' is not a dictionary.")
        found_value = details.get(key, default)
        if found_value == value:
            found_sequencers[name] = details
        # if this sequencer has the desired key-value pair
    # next sequencer type

    immutable_found_sequencers = MappingProxyType(found_sequencers)
    return immutable_found_sequencers


def get_i5_index_sequencers(existing_types=None):
    """Get sequencer types that use an i5 index, revcomped or not."""
    result = MappingProxyType({})
    available_sequencer_types = _load_sequencer_types(existing_types)
    for curr_bool_val in [True, False]:
        curr_mapping_proxy = get_sequencers_w_key_value(
            _REVCOMP_I5_KEY, curr_bool_val,
            existing_types=available_sequencer_types)
        result = MappingProxyType(result | curr_mapping_proxy)
    # next boolean value
    return result


def get_sequencer_type(sequencer_type, existing_types=None):
    """Get the sequencer type info from the available sequencer types.

    Parameters
    ----------
    sequencer_type: str
        The name of the sequencer type to retrieve.
    existing_types: MappingProxyType, optional
        A mapping of available sequencer types. If None, the
        sequencer types will be loaded from the YAML file.

    Returns
    -------
    MappingProxyType
        Immutable dictionary of the sequencer type details.
    """
    sequencer_types = _load_sequencer_types(existing_types)
    if sequencer_type in sequencer_types:
        return MappingProxyType(sequencer_types[sequencer_type])
    # end if sequencer type is in the available sequencers

    # if we get here, the sequencer type is not found
    raise ValueError(f"Sequencer type '{sequencer_type}' not found.")


def is_i5_revcomp_sequencer(sequencer_type, existing_types=None):
    """Check if a sequencer type uses a revcomp i5 index in sample sheet."""
    sequencer_info = get_sequencer_type(
        sequencer_type, existing_types=existing_types)
    if _REVCOMP_I5_KEY in sequencer_info:
        return sequencer_info[_REVCOMP_I5_KEY]
    # end if sequencer type has the revcomp i5 key

    # if we get here, the sequencer type is not in the i5 index sequencers
    raise ValueError(
        f"Sequencer type '{sequencer_type}' does not have a "
        f"'{_REVCOMP_I5_KEY}' key in sequencer types.")
