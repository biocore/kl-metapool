"""Shared utilities for multi-notebook workflows.

This module provides functions and constants used across the shotgun_metag
notebook series (and potentially other notebook series) for:
- Extracting attributes from study dictionaries
- Detecting file separators based on file extensions
"""

import warnings


def get_studies_attr_list(studies_dict, desired_key):
    """Extract a specific attribute from each study in a list.

    Parameters
    ----------
    studies_dict : list of dict
        List of study dictionaries, each containing study metadata.
    desired_key : str
        The key to extract from each study dictionary.

    Returns
    -------
    list
        List of values for the specified key from each study.
    """
    return [x[desired_key] for x in studies_dict]


def pick_expected_separator(fps_list):
    """Determine the expected separator based on file extensions.

    Analyzes file extensions to determine the most likely delimiter:
    - All .csv files → comma separator
    - All .tsv or .txt files → tab separator
    - Mixed extensions → defaults to tab with a warning

    Parameters
    ----------
    fps_list : list of str
        List of file paths to analyze.

    Returns
    -------
    tuple
        (separator, visible_name) where separator is the delimiter character
        and visible_name is a human-readable description ('tab' or 'comma').
    """
    sep = "\t"
    visible_sep = "tab"

    num_fps = len(fps_list)
    num_csv = sum([x.endswith('.csv') for x in fps_list])
    num_txt = sum([x.endswith('.txt') for x in fps_list])
    num_tsv = sum([x.endswith('.tsv') for x in fps_list])

    if num_csv == num_fps:
        sep = ','
        visible_sep = "comma"
    elif (num_tsv + num_txt) != num_fps:
        warnings.warn(
            "Could not determine separator; defaulting to " + visible_sep)

    return sep, visible_sep
