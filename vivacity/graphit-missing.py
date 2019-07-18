#!/usr/bin/env python3

from graphit_base import run_graphs, do_bar_graph, START, END

YMAX = 13000


def do_daily_bar_graphs(df, axs_row):

    col_list = list(df)
    df['total'] = df[col_list].sum(axis=1)
    df = df[df.total == 0]
    df = df.between_time('06:00:00', '23:59:00')

    df = df.resample('D').count()

    do_bar_graph(df, axs_row[0], 'total', 60)


def run():

    run_graphs('missing.pdf', START, END, ['Number of zero data blocks', 'x'], do_daily_bar_graphs)


if __name__ == '__main__':
    run()
