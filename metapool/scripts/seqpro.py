#!/usr/bin/env python

import click
import os

from metapool import (preparations_for_run, KLSampleSheet,
                      sample_sheet_to_dataframe, run_counts)


@click.command()
@click.argument('run_dir', type=click.Path(exists=True, dir_okay=True,
                                           file_okay=False))
@click.argument('sample_sheet', type=click.Path(exists=True, dir_okay=False,
                                                file_okay=True))
@click.argument('output_dir', type=click.Path(writable=True))
@click.option('--pipeline', help='Which pipeline generated the data',
              show_default=True, default='fastp-and-minimap2',
              type=click.Choice(['atropos-and-bowtie2', 'fastp-and-minimap2']))
def format_preparation_files(run_dir, sample_sheet, output_dir, pipeline):
    """Generate the preparation files for the projects in a run

    RUN_DIR: should be the directory where the results of running bcl2fastq are
    saved.

    SAMPLE_SHEET: should be a CSV file that includes information for the
    samples and projects in RUN_DIR.

    OUTPUT_DIR: directory where the outputted preparations should be saved to.

    Preparations are stratified by project and by lane. Only samples with
    non-empty files are included. If "fastp-and-minimap2" is used, the script
    will collect sequence count stats for each sample and add them as columns
    in the preparation file.
    """
    sample_sheet = KLSampleSheet(sample_sheet)
    df_sheet = sample_sheet_to_dataframe(sample_sheet)

    if pipeline == 'atropos-and-bowtie2':
        click.echo('Stats collection is not supported for pipeline '
                   'atropos-and-bowtie2')
    else:
        stats = run_counts(run_dir, sample_sheet)

        # stats don't include well description which is the primary key to
        # merge with the preps in the loop below
        stats['sample_name'] = \
            df_sheet.set_index('lane', append=True)['well_description']

    # returns a map of (run, project_name, lane) -> preparation frame
    preps = preparations_for_run(run_dir, df_sheet, pipeline=pipeline)

    os.makedirs(output_dir, exist_ok=True)

    for (run, project, lane), df in preps.items():
        filename = os.path.join(output_dir, f'{run}.{project}.{lane}.tsv')

        if pipeline == 'fastp-and-minimap2':
            # stats are indexed by sample name and lane, lane is the first
            # level index. When merging, make sure to select the lane subset
            # that we care about, otherwise we'll end up with repeated rows
            df = df.merge(stats.xs(lane, level=1), how='left',
                          on='sample_name')

        df.to_csv(filename, sep='\t', index=False)


if __name__ == '__main__':
    format_preparation_files()
