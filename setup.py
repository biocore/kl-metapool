from setuptools import setup, find_packages
from glob import glob
from os.path import dirname
import versioneer

# collect notebook data files
notebooks_fp = [(dirname(fp), [fp]) for fp in glob('notebooks/*.ipynb')]

setup(
    name="metapool",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(
        exclude=("notebooks", "notebooks.*", "tests", "tests.*", "docs", "docs.*")
    ),
    include_package_data=True,
    package_data={
        # keep your data files
        "metapool": ["data/*.tsv", "data/*.xlsx", "tests/data/*.csv"]
    },
    # include notebooks (if you still want them installed)
    data_files=notebooks_fp,

    # Conda-canonical: leave runtime deps to your conda recipe
    # install_requires=[],

    entry_points={
        "console_scripts": [
            "seqpro=metapool.scripts.seqpro:format_preparation_files",
            "seqpro_mf=metapool.scripts.seqpro_mf:format_preparation_files_mf",
        ],
    },

    python_requires=">=3.9",
)
