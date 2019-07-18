#!/usr/bin/env python3

import argparse
import sys

import dateutil.parser

from graphit_base import run_graphs, do_line_graph_by_day

YMAX = 800


def do_daily_line_graphs(df, axs_row):

    col_list = list(df)
    col_list.remove('pedestrian')
    col_list.remove('cyclist')
    df['motor'] = df[col_list].sum(axis=1)

    df = df.resample('H').sum()

    do_line_graph_by_day(df, axs_row[0], 'pedestrian', YMAX)
    do_line_graph_by_day(df, axs_row[1], 'cyclist', YMAX)
    do_line_graph_by_day(df, axs_row[2], 'motor', YMAX)


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('start', help='first (or only) day to process')
    parser.add_argument('--end', '-e', help='last day to process')
    parser.add_argument('--out', '-o', help='output file name', default='custom.pdf')

    args = parser.parse_args()

    try:
        args.start = dateutil.parser.parse(args.start).date()
        if args.end:
            args.end = dateutil.parser.parse(args.end).date()
        else:
            args.end = args.start
    except ValueError as e:
        print(''.join(e.args), file=sys.stderr)
        sys.exit(1)

    return args


def run():

    params = parse_args()

    run_graphs(
        params.out,
        'Traffic',
        params.start,
        params.end,
        ('Pedestrian', 'Cyclist', 'Motor'),
        do_daily_line_graphs,
        'Per hour')


if __name__ == '__main__':
    run()
