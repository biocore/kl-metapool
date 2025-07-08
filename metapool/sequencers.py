from importlib.resources import files
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
_SEQUENCER_TYPES_DIR = "config"
_SEQUENCER_TYPES_YML_FNAME = 'sequencer_types.yml'

# DEPRECATED: We no longer want to identify sequencer types by the
# instrument id, since that requires a change for every new physical machine.
# This is kept for backwards compatibility with existing data, but for anything
# new, we should use the instrument type instead.
# _MODEL_TYPE_KEY values must match to a key in the sequencer_types.yml file.
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


def _deep_freeze(obj):
    """Recursively freeze a Python object to make it immutable.
    This function converts mutable objects (dicts, lists, sets) into their
    immutable counterparts (MappingProxyType, tuples, frozensets) while
    leaving immutable objects (strings, numbers, etc.) unchanged.

    Parameters
    ----------
    obj: Any
        The object to freeze. It can be a dict, list, set, tuple, or any
        immutable type (like str, int, float, etc.).

    Returns
    -------
    Any
        An immutable version of the input object. If the input is a dict,
        it returns a MappingProxyType; if it's a list, it returns a tuple;
        if it's a set, it returns a frozenset; otherwise, it returns the
        original object unchanged.
    """
    if isinstance(obj, dict):
        # Recursively freeze values and return a read-only MappingProxyType
        return MappingProxyType({k: _deep_freeze(v) for k, v in obj.items()})
    elif isinstance(obj, list):
        # Convert list to tuple after freezing elements
        return tuple(_deep_freeze(v) for v in obj)
    elif isinstance(obj, set):
        # Convert set to frozenset after freezing elements
        return frozenset(_deep_freeze(v) for v in obj)
    elif isinstance(obj, tuple):
        # Freeze all elements in the tuple
        return tuple(_deep_freeze(v) for v in obj)
    else:
        # Assume everything else is immutable
        return obj


def _load_sequencer_types(existing_types=None, test_only_fp=None):
    """Load sequencer types from sequencer types yaml file.

    Parameters
    ----------
    existing_types: MappingProxyType, optional
        A mapping of sequencer types to use instead of loading from file.
        If None, the sequencer types will be loaded from the YAML file; if
        provided, will short-circuit the loading process and return input.
    test_only_fp: str, optional
        For testing purposes ONLY, a test file path to load the sequencer
        types from. If None, the default sequencer types YAML file will be
        used; should always be None in production code.

    Returns
    -------
    MappingProxyType
        Immutable dictionary of sequencer types.

    Raises
    ------
    ValueError
        If existing_types is not a MappingProxyType or None.
    """

    if existing_types is not None:
        # if an existing mapping is provided, use it
        if not isinstance(existing_types, MappingProxyType):
            raise ValueError(
                "existing_types must be a MappingProxyType or None.")
        # end if existing_types is not a MappingProxyType

        sequencer_types = existing_types
    else:
        if test_only_fp is None:
            # get the path to the directory above the one this file is in
            files_dir = files('metapool')
            sequencers_fp = files_dir.joinpath(
                f"{_SEQUENCER_TYPES_DIR}/{_SEQUENCER_TYPES_YML_FNAME}")
        else:
            # for testing, use the provided file path
            sequencers_fp = test_only_fp

        with open(sequencers_fp, 'r') as file:
            sequencer_types = yaml.safe_load(file)
    # end if existing_types is None or not

    immutable_sequencer_types = _deep_freeze(sequencer_types)
    return immutable_sequencer_types


def _get_machine_code(instrument_model):
    """Get the machine code for an instrument's model string

    Parameters
    ----------
    instrument_model: str
        An instrument's model of the form A999999 or AA999999

    Returns
    -------
    str
        The machine code, which is the first 1 or 2 letters of the instrument
        model.

    Raises
    ------
    ValueError
        If the instrument model is malformed and does not contain a valid
        machine code.
    """
    # the machine code is everything before the first number
    # (we expect these to be letters, so pattern could be improved ...)
    matches = re.match(r"^(.*?)\d.*", instrument_model)

    if matches is not None:
        machine_code = matches.group(1)
        if machine_code != "":
            return machine_code

    raise ValueError(f"Cannot find a machine code; the instrument "
                     f"model '{instrument_model}' is malformed.")


def _get_model_by_machine_prefix(instrument_prefix, sequencer_types=None):
    """Get the instrument model by its machine prefix.

    Parameters
    ----------
    instrument_prefix: str
        The machine prefix of the instrument, e.g., 'MN' for MN01225.
    sequencer_types: MappingProxyType, optional
        A mapping of available sequencer types. If None, the
        sequencer types will be loaded from the YAML file.

    Returns
    -------
    MappingProxyType
        Immutable dictionary of the instrument model details.

    Raises
    ------
    ValueError
        If the instrument prefix is not recognized or if multiple
        sequencer types match the given prefix.
    """
    models_w_prefix = get_sequencers_w_key_value(
        _MACHINE_PREFIX_KEY, instrument_prefix,
        existing_types=sequencer_types)
    if len(models_w_prefix) == 0:
        raise ValueError(
            f"Unrecognized {_MACHINE_PREFIX_KEY} '{instrument_prefix}'.")
    elif len(models_w_prefix) > 1:
        raise ValueError(
            f"Found {len(models_w_prefix)} sequencer types with "
            f"{_MACHINE_PREFIX_KEY} '{instrument_prefix}': "
            f"{', '.join(models_w_prefix)}.")
    # end if got an unexpected number of sequencer types w given prefix

    inst_model_type = next(iter(models_w_prefix))
    instrument_model = _get_model_by_sequencer_type_name(
        inst_model_type, sequencer_types=models_w_prefix)
    return instrument_model


def get_model_by_instrument_id(instrument_id, sequencer_types=None):
    """

    Parameters
    ----------
    instrument_id
    sequencer_types

    Returns
    -------

    """
    sequencer_types = _load_sequencer_types(existing_types=sequencer_types)
    instrument_prefix = _get_machine_code(instrument_id)
    instrument_model = _get_model_by_machine_prefix(
        instrument_prefix, sequencer_types=sequencer_types)
    return instrument_model


def get_model_and_center(instrument_code):
    """Determine instrument model and center using instrument code.

    Parameters
    ----------
    instrument_code: str
        Instrument code from a run identifier.

    Returns
    -------
    str
        Instrument model.
    str
        Run center associated with the instrument.

    Raises
    ------
    ValueError
        If zero or more than one machine prefixes are associated with
        the instrument code.
    """

    run_center = _LAB_RUN_CENTER  # Default run center for lab data
    available_sequencer_types = _load_sequencer_types()

    instrument_id = instrument_code.split('_')[0]
    if instrument_id in _INSTRUMENT_LOOKUP.index:
        run_center = _INSTRUMENT_LOOKUP.loc[instrument_id, _RUN_CENTER_KEY]
        inst_model_type = _INSTRUMENT_LOOKUP.loc[
            instrument_id, _MODEL_TYPE_KEY]
        instrument_model = _get_model_by_sequencer_type_name(
            inst_model_type, sequencer_types=available_sequencer_types)
    else:
        instrument_model = get_model_by_instrument_id(
            instrument_id, sequencer_types=available_sequencer_types)
    # end if instrument_id is in the lookup or if must look up by prefix

    return instrument_model, run_center


def _get_model_by_sequencer_type_name(inst_model_type, sequencer_types):
    """Get the instrument model by its sequencer type name.

    Parameters
    ----------
    inst_model_type: str
        The sequencer type name, e.g., 'iSeq', 'NovaSeq6000', etc.
    sequencer_types: MappingProxyType
        A mapping of available sequencer types.

    Returns
    -------
    MappingProxyType
        Immutable dictionary of the instrument model details.

    Raises
    ------
    ValueError
        If the sequencer type name is not recognized or if it does not
        contain a model name.
    """
    inst_sequencer_type = sequencer_types[inst_model_type]
    instrument_model = inst_sequencer_type[_MODEL_NAME_KEY]
    return instrument_model


def get_sequencers_w_key_value(key, value, default=None, existing_types=None):
    """Get all sequencers with a specific key-value pair.

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

    Raises
    ------
    ValueError
        If the info for a sequencer type is not a dictionary.
    """

    found_sequencers = {}
    sequencer_types = _load_sequencer_types(existing_types)
    for name, details in sequencer_types.items():
        if not isinstance(details, MappingProxyType):
            raise ValueError(
                f"Info for sequencer type '{name}' is not a MappingProxyType.")
        found_value = details.get(key, default)
        if found_value == value:
            found_sequencers[name] = details
        # if this sequencer has the desired key-value pair
    # next sequencer type

    immutable_found_sequencers = _deep_freeze(found_sequencers)
    return immutable_found_sequencers


def get_i5_index_sequencers(existing_types=None):
    """Get sequencer types that use an i5 index, revcomped or not.

    Parameters
    ----------
    existing_types: MappingProxyType, optional
        A mapping of available sequencer types. If None, the
        sequencer types will be loaded from the YAML file.

    Returns
    -------
    MappingProxyType
        Immutable dictionary of sequencer types that use an i5 index, with or
        without revcomping.
    """
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

    Raises
    ------
    ValueError
        If the sequencer type is not found in the available sequencer types.
    """
    sequencer_types = _load_sequencer_types(existing_types)
    if sequencer_type in sequencer_types:
        return _deep_freeze(sequencer_types[sequencer_type])
    # end if sequencer type is in the available sequencers

    # if we get here, the sequencer type is not found
    raise ValueError(f"Sequencer type '{sequencer_type}' not found.")


def is_i5_revcomp_sequencer(sequencer_type, existing_types=None):
    """Check if sequencer type uses a revcomped i5 index in sample sheets.

    Parameters
    ----------
    sequencer_type: str
        The name of the sequencer type to check.
    existing_types: MappingProxyType, optional
        A mapping of available sequencer types. If None, the
        sequencer types will be loaded from the YAML file.

    Returns
    -------
    bool
        True if the sequencer type uses a revcomped i5 index, False otherwise.

    Raises
    ------
    ValueError
        If the sequencer type does not have a revcomp i5 key in the sequencer
        types.
    """
    sequencer_info = get_sequencer_type(
        sequencer_type, existing_types=existing_types)
    if _REVCOMP_I5_KEY in sequencer_info:
        return sequencer_info[_REVCOMP_I5_KEY]
    # end if sequencer type has the revcomp i5 key

    # if we get here, the sequencer type is not in the i5 index sequencers
    raise ValueError(
        f"Sequencer type '{sequencer_type}' does not have a "
        f"'{_REVCOMP_I5_KEY}' key in sequencer types.")
