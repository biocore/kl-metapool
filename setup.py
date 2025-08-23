from setuptools import setup, find_packages
import versioneer

setup(
    name="metapool",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(
        exclude=("notebooks", "notebooks.*", "tests", "tests.*", "docs", "docs.*")
    ),
    include_package_data=True,
    python_requires=">=3.9",
    entry_points={"console_scripts": ["metapool=metapool.cli:main"]},
    # install_requires=[],  # leave empty for conda-canonical
)
