#!/usr/bin/env python3

import matplotlib

from datetime import date

from graphit_base import run_graphs, hilight_bridge_closure

START = date(2019, 5, 10)
END = date(2019, 7, 11)

YMAX = 13000


def do_bar_graph(df, ax, col):
    '''
    Plot column `col` from data frame `df` onto axis `ax` as a bar graph.
    '''

    # df.plot.bar(y=[col], ax=ax, ylim=(0, YMAX), legend=False)

    ax.bar(df.index, df[col], zorder=3, align='edge')

    ax.set_ylim([0, YMAX])
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=2500))
    ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(base=500))

    ax.grid(axis='y', zorder=2)
    ax.xaxis.set_major_locator(matplotlib.dates.WeekdayLocator(byweekday=matplotlib.dates.MO))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d\n%b'))
    ax.xaxis.set_minor_locator(matplotlib.dates.DayLocator())

    hilight_bridge_closure(ax)


def do_daily_bar_graphs(df, axs_row):

    col_list = list(df)
    col_list.remove('pedestrian')
    col_list.remove('cyclist')
    df['motor'] = df[col_list].sum(axis=1)

    df = df.resample('D').sum()

    do_bar_graph(df, axs_row[0], col='pedestrian')
    do_bar_graph(df, axs_row[1], col='cyclist')
    do_bar_graph(df, axs_row[2], col='motor')


def run():

    run_graphs('plot.pdf', START, END, ('Pedestrian', 'Cyclist', 'Motor'), do_daily_bar_graphs)


if __name__ == '__main__':
    run()
