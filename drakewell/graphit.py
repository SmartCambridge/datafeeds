#!/usr/bin/env python3

import json
import matplotlib.pyplot
import re
import sys

import pandas as pd

sys.path.append('../vivacity')
from graphit_base import hilight_bridge_closure, setup_axies

TO_MPH = 2.23694
GRAPHS_PER_ROW = 2
GRAPHS_PER_PAGE = GRAPHS_PER_ROW * 3
MM_TO_INCH = 0.0393701
A4P = (210*MM_TO_INCH, 297*MM_TO_INCH)
A3P = (297*MM_TO_INCH, 420*MM_TO_INCH)
A3L = (420*MM_TO_INCH, 297*MM_TO_INCH)
FIGSIZE = A3L

YMAX = 50

DATAFILES = [
    'downloaded_data/2019-05.csv',
    'downloaded_data/2019-06.csv',
    'downloaded_data/2019-07.csv'
]

LINKS = [
    '9800YBB3C3Z3',
    '9800XZIHFPWW',
    '9800XMD9MJ0V',
    '9800XFYLRKEG',
    '9800WBKMTUIZ',
    '9800ZNBKR5BY',
    '9800ZFE9FFOQ',
    '9800YGD93F5D',
    '9800ZMJIIRA4',
    '9800WUW4QTBC',
    '9800XIVHRXA0',
    '9800WLZSM8UU',
    '9800YIZKVIHJ',
    '9800W1NX9BF2',
    '9800YLJPNESW',
    '9800XVT0GHMV',

    '9800WG6CCW1R',
    '9800ZJUF0PLK',
    '9800XXIR2CRV',
    '9800WRNP76Y5',
    '9800X7A57PMZ',
    '9800X4FQ1IJQ',
    '9800ZACH8L2P',
    '9800X0IM4Q3M',
    '9800XYNTVQMQ',
    '9800XKGQVE1Z',
    '9800YEDVIYOL',
    '9800WOZGV4D2',
    '9800WSL0VRZ2',
    '9800YRC720KT',
    '9800Y6CS0QK2',
    '9800YDKVJZKE',
    '9800WENYEPFN',
    '9800YHOTYC18',
    '9800X0SVTS0E',
    '9800ZJZCXDYW'
]


def percentile(n):
    def percentile_(x):
        return x.quantile(n)
    percentile_.__name__ = 'percentile_{:2.0f}'.format(n*100)
    return percentile_


def do_graph(ax, df, link, length, title):

    df2 = df[df.cosit == link]
    df2 = df2[df2.index.dayofweek < 5]

    df2['speed'] = (length / df2['seconds']) * TO_MPH

    params = {
        'speed': [
            min,
            percentile(0.25),
            'median',
            percentile(0.75),
            max
        ]
    }
    grouped = df2.resample('D').agg(params)
    grouped.columns = grouped.columns.droplevel(level=0)

    ax.errorbar(
        grouped.index,
        grouped['median'],
        yerr=[grouped['median'] - grouped['min'], grouped['max'] - grouped['median']],
        fmt='none',
        elinewidth=1,
        capsize=3,
        capwidth=2,
        ecolor='k')

    ax.errorbar(
        grouped.index,
        grouped['median'],
        yerr=[grouped['median'] - grouped['percentile_25'],
              grouped['percentile_75'] - grouped['median']],
        marker='_',
        mfc='k',
        mew='1',
        mec='k',
        ms=8,
        lw=0,
        elinewidth=4,
        capsize=0)

    hilight_bridge_closure(ax)

    setup_axies(ax, YMAX)

    ax.xaxis.set_major_locator(matplotlib.dates.DayLocator(1))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('\n%b\n%Y'))
    ax.xaxis.set_minor_locator(matplotlib.dates.WeekdayLocator(matplotlib.dates.MO))
    ax.xaxis.set_minor_formatter(matplotlib.dates.DateFormatter('%d'))

    ax.grid(axis='y', which='major', zorder=2)
    ax.grid(axis='x', which='minor', zorder=2)

    ax.set_title(title)


def setup_figure(between):

    fig, axs_list = matplotlib.pyplot.subplots(
        nrows=GRAPHS_PER_PAGE // GRAPHS_PER_ROW,
        ncols=GRAPHS_PER_ROW,
        sharex=True,
        sharey=True,
        figsize=FIGSIZE,
        squeeze=False)

    fig.suptitle(f'Traffic speeds, Mon-Fri, {between[0]}-{between[1]}', fontsize=13)

    return fig, axs_list


def do_graph_set(pdf, df, links, between):

    graph = 0
    fig = None

    for link in LINKS:

        if graph % GRAPHS_PER_PAGE == 0:
            if graph > 0:
                fig.tight_layout(rect=[0, 0, 1, 0.96])
                pdf.savefig(fig)
                print('Page!')
            fig, axs_list = setup_figure(between)

        row = (graph % GRAPHS_PER_PAGE) // GRAPHS_PER_ROW
        col = graph % GRAPHS_PER_ROW
        print(f'Link: {link}, graph: {graph}, row: {row}, col: {col}')

        do_graph(axs_list[row, col], df, link, links[link]['length'], links[link]['name'])

        if col == 0:
            axs_list[row, col].set(ylabel='Speed (mph)')

        graph += 1

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    pdf.savefig(fig)
    print('Last page!')


def run():

    # Slurp the data

    df = pd.concat(map(pd.read_csv, DATAFILES))
    df.columns = ['node', 'cosit', 'timestamp', 'period', 'seconds', 'count']
    df.index = pd.to_datetime(df['timestamp'])
    df.drop('timestamp', axis=1, inplace=True)

    # Slurp link details
    with open('locations.json') as f:
        locations = json.load(f)
    links = {re.sub(r'CAMBRIDGE_JTMS\|', '', record['id']): record for record in locations['links']}

    with matplotlib.backends.backend_pdf.PdfPages('traffic_speed.pdf') as pdf:

        for between in (('07:00', '09:00'), ('16:00', '18:00')):

            df2 = df.between_time(*between)

            do_graph_set(pdf, df2, links, between)


if __name__ == '__main__':
    run()
