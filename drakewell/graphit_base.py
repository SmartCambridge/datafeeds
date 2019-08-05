#!/usr/bin/env python3

import json
import matplotlib.pyplot
import re

from datetime import date

import pandas as pd

TO_MPH = 2.23694
GRAPHS_PER_ROW = 2
GRAPHS_PER_PAGE = GRAPHS_PER_ROW * 3
MM_TO_INCH = 0.0393701
A4P = (210*MM_TO_INCH, 297*MM_TO_INCH)
A3P = (297*MM_TO_INCH, 420*MM_TO_INCH)
A3L = (420*MM_TO_INCH, 297*MM_TO_INCH)
FIGSIZE = A3L

YMAX = 30

DATAFILES = [
    'downloaded_data/2019-05.csv',
    'downloaded_data/2019-06.csv',
    'downloaded_data/2019-07.csv',
    'downloaded_data/2019-08.csv'
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

sites = {}
links = {}


def hilight_bridge_closure(ax):

    left, right = ax.get_xlim()
    ax.axvspan(date(2019, 7, 1), date(2019, 8, 24), facecolor='k', alpha=0.1, zorder=1)
    ax.set_xlim(left, right)


def percentile(n):
    def percentile_(x):
        return x.quantile(n)
    percentile_.__name__ = 'percentile_{:2.0f}'.format(n*100)
    return percentile_


def do_bar_and_wisker_graph(ax, df, link):

    df2 = df[df.cosit == link]
    df2['minutes'] = df2['seconds']/60

    params = {
        'minutes': [
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

    ax.xaxis.set_major_locator(matplotlib.dates.DayLocator(1))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('\n%b\n%Y'))
    ax.xaxis.set_minor_locator(matplotlib.dates.WeekdayLocator(matplotlib.dates.MO))
    ax.xaxis.set_minor_formatter(matplotlib.dates.DateFormatter('%d'))

    ax.grid(axis='y', which='major', zorder=2)
    ax.grid(axis='x', which='minor', zorder=2)


def day_scatter_graph(ax, df, link):

    df2 = df[df.cosit == link].copy()
    df2.index = df2.index.normalize()
    df2['minutes'] = df2['seconds']/60

    ax.plot(df2.index, df2['minutes'], '. b')

    df2 = df2.resample('D').mean()

    ax.plot(df2.index, df2['minutes'], '_ k')

    hilight_bridge_closure(ax)

    ax.xaxis.set_major_locator(matplotlib.dates.DayLocator(1))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('\n%b\n%Y'))
    ax.xaxis.set_minor_locator(matplotlib.dates.WeekdayLocator(matplotlib.dates.MO))
    ax.xaxis.set_minor_formatter(matplotlib.dates.DateFormatter('%d'))

    ax.grid(axis='y', which='major', zorder=2)
    ax.grid(axis='x', which='minor', zorder=2)


def hourly_average(ax, df, link):

    df2 = df[df.cosit == link]
    df2 = df2.groupby(df2.index.hour).mean()
    df2['minutes'] = df2['seconds']/60

    ax.bar(df2.index, df2['minutes'], align='edge')

    ax.set_xlim([0, 24])
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=4))
    ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(base=1))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%02d:00'))

    ax.grid(axis='y', which='major', zorder=2)


def setup_figure(title):

    fig, axs_list = matplotlib.pyplot.subplots(
        nrows=GRAPHS_PER_PAGE // GRAPHS_PER_ROW,
        ncols=GRAPHS_PER_ROW,
        sharex=True,
        sharey=True,
        figsize=FIGSIZE,
        squeeze=False)

    fig.suptitle(title, fontsize=13)

    return fig, axs_list


def setup_axies(ax, ymax):
    '''
    Common axis setup code
    '''

    if ymax:
        ax.set_ylim([0, ymax])

    ax.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))


def get_drakewell_data():

    global links, sites

    # Slurp link and site details
    with open('locations.json') as f:
        locations = json.load(f)
    links = {re.sub(r'CAMBRIDGE_JTMS\|', '', record['id']): record for record in locations['links']}
    sites = {record['id']: record for record in locations['sites']}

    df = pd.concat(map(pd.read_csv, DATAFILES))
    df.columns = ['node', 'cosit', 'timestamp', 'period', 'seconds', 'count']
    df.index = pd.to_datetime(df['timestamp'])
    df.drop('timestamp', axis=1, inplace=True)

    return df


def do_graph_set(pdf, df, graph_fn, link_list, page_title, ymax):

    graph = 0
    fig = None

    for link in link_list:

        if graph % GRAPHS_PER_PAGE == 0:
            if graph > 0:
                fig.tight_layout(rect=[0, 0, 1, 0.96])
                pdf.savefig(fig)
                print('Page!')
            fig, axs_list = setup_figure(page_title)

        row = (graph % GRAPHS_PER_PAGE) // GRAPHS_PER_ROW
        col = graph % GRAPHS_PER_ROW
        print(f'Link: {link}, graph: {graph}, row: {row}, col: {col}')
        ax = axs_list[row, col]

        start_point = sites[links[link]['sites'][0]]
        end_point = sites[links[link]['sites'][1]]
        graph_fn(ax, df, link)
        setup_axies(ax, ymax)
        ax.set_title(f'{links[link]["name"]}\n{start_point["description"]} --> '
                     f'{end_point["description"]}\n{links[link]["length"]:,.0f} m')

        if col == 0:
            axs_list[row, col].set(ylabel='Journey time (minutes)')

        graph += 1

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    pdf.savefig(fig)
    print('Last page!')
