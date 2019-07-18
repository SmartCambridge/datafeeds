#!/usr/bin/env python3

import argparse
import sys

import dateutil.parser

from graphit_base import run_graphs, do_line_graph_by_day

YMAX = 800


def do_daily_line_graphs(df, axs_row):

    df = df.resample('H').sum()

    df['car_taxi'] = df['car'] + df['taxi']
    df['all_bus'] = df['minibus'] + df['bus']
    df['goods'] = df['van'] + df['rigid'] + df['truck']

    # df['emergency'] = df['emergency car'] + df['emergency van'] + df['fire engine']
    do_line_graph_by_day(df, axs_row[0], 'car_taxi', 800)
    do_line_graph_by_day(df, axs_row[1], 'goods', 210)
    do_line_graph_by_day(df, axs_row[2], 'all_bus', 40)
    do_line_graph_by_day(df, axs_row[3], 'motorbike', 40)


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
        'Motor traffic',
        params.start,
        params.end,
        ('Cars (incl. Taxis)', 'Goods vehicles (Vans, Rigid and Trucks)',
            'Buses (and Minibuses)', 'Motorbikes'),
        do_daily_line_graphs,
        'Per hour',
        sharey=False)


if __name__ == '__main__':
    run()
