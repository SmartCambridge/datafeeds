#!/usr/bin/env python3


from graphit_base import run_graphs, do_bar_graph_by_day, do_bar_graph_by_hour, START, END

YMAX = 13000


def do_daily_bar_graphs(df, axs_row):

    col_list = list(df)
    col_list.remove('pedestrian')
    col_list.remove('cyclist')
    df['motor'] = df[col_list].sum(axis=1)

    df = df.resample('D').sum()

    do_bar_graph_by_day(df, axs_row[0], 'pedestrian', YMAX)
    do_bar_graph_by_day(df, axs_row[1], 'cyclist', YMAX)
    do_bar_graph_by_day(df, axs_row[2], 'motor', YMAX)


def do_hourly_bar_graphs(df, axs_row):

    col_list = list(df)
    col_list.remove('pedestrian')
    col_list.remove('cyclist')
    df['motor'] = df[col_list].sum(axis=1)

    df = df.resample('H').sum()
    df = df.groupby(df.index.hour).mean()

    do_bar_graph_by_hour(df, axs_row[0], 'pedestrian', 300)
    do_bar_graph_by_hour(df, axs_row[1], 'cyclist', 450)
    do_bar_graph_by_hour(df, axs_row[2], 'motor', 800)


def run():

    run_graphs(
        '3way-date.pdf',
        'Traffic',
        START,
        END,
        ('Pedestrian', 'Cyclist', 'Motor'),
        do_daily_bar_graphs,
        'Per day')

    run_graphs(
        '3way-hour.pdf',
        f'Average hourly traffic ({START.isoformat()} - {END.isoformat()})',
        START,
        END,
        ('Pedestrian', 'Cyclist', 'Motor'),
        do_hourly_bar_graphs,
        'Per hour',
        sharey=False)


if __name__ == '__main__':
    run()
