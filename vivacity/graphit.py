#!/usr/bin/env python3

import json
import os

from datetime import date, timedelta

import pandas as pd

from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib

ONE_DAY = timedelta(days=1)
MM_TO_INCH = 0.0393701
A4P = (210*MM_TO_INCH, 297*MM_TO_INCH)
A3P = (297*MM_TO_INCH, 420*MM_TO_INCH)
A3L = (420*MM_TO_INCH, 297*MM_TO_INCH)

ROWS_PER_PAGE = 6
START = date(2019, 5, 10)
END = date(2019, 7, 10)
YMAX = 13000
FIGSIZE = A3L

COUNTLINES = {
    '13069': {'name': 'Tennison Road', 'in': 'N-bound', 'out': 'S-bound'},
    '13070': {'name': 'Coleridge Road', 'in': 'S-bound', 'out': 'N-bound'},
    '13071': {'name': 'Mill Road (E end)', 'in': 'E-bound', 'out': 'W-bound'},
    '13072': {'name': 'Vinery Road', 'in': 'S-bound', 'out': 'N-bound'},
    '13073': {'name': 'Cherry Hinton Road', 'in': 'E-bound', 'out': 'W-bound'},
    '13074': {'name': 'Station Road', 'in': 'W-bound', 'out': 'E-bound'},
    '13075': {'name': 'East Road', 'in': 'NE-bound', 'out': 'SW-bound'},
    '13076': {'name': 'Coldhams Lane', 'in': 'S-bound', 'out': 'N-bound'},
    '13077': {'name': 'Mill Road (NW end)', 'in': 'SE-bound', 'out': 'NW-bound'},
    '13078': {'name': 'Carter Bridge', 'in': 'W-bound', 'out': 'E-bound'},
    '13079': {'name': 'Milton Road', 'in': 'NE-bound', 'out': 'SW-bound'},
    '13080': {'name': 'Hills Road', 'in': 'S-bound', 'out': 'N-bound'},
    '13081': {'name': 'Newmarket Road', 'in': 'W-bound', 'out': 'E-bound'},
    '13082': {'name': 'Histon Road', 'in': 'S-bound', 'out': 'N-bound'},
    '13086': {'name': 'Perne Road', 'in': 'N-bound', 'out': 'S-bound'},
    }


def get_data(countline, direction, start, end):

    '''
    {
        "ts": 1562284800.0,
        "timestamp": "2019-07-05T00:00:00+00:00",
        "from": "2019-07-05T00:00:00.000Z",
        "to": "2019-07-05T00:05:00.000Z",
        "countline": "13069",
        "direction": "in",
        "counts": {
            "pedestrian": 1,
            "cyclist": 0,
            "motorbike": 1,
            "car": 1,
            "taxi": 0,
            "van": 1,
            "minibus": 0,
            "bus": 0,
            "rigid": 0,
            "truck": 0,
            "emergency car": 0,
            "emergency van": 0,
            "fire engine": 0
        }
    }
    ...
    '''

    day = start
    data = []
    while day <= end:

        try:
            filename = os.path.join(
                'vivacity_data',
                day.strftime('%Y'),
                day.strftime('%m'),
                day.strftime('%d'),
                countline,
                direction + '.txt')
            with open(filename) as file:
                for line in file:
                    motors = 0
                    data_block = json.loads(line)
                    for type, count in data_block['counts'].items():
                        if type == 'pedestrian':
                            pedestrians = count
                        elif type == 'cyclist':
                            cyclists = count
                        else:
                            motors += count
                    data.append((
                        data_block['timestamp'],
                        pedestrians,
                        cyclists,
                        motors))
        except FileNotFoundError:
            pass
        day += ONE_DAY

    return data


def do_graph(df, ax, col):

    # df.plot.bar(y=[col], ax=ax, ylim=(0, YMAX), legend=False)

    ax.bar(df.index, df[col], zorder =3, align='edge')

    ax.set_ylim([0, YMAX])
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=2500))
    ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(base=500))

    ax.grid(axis='y', zorder=2)
    ax.xaxis.set_major_locator(matplotlib.dates.WeekdayLocator(byweekday=matplotlib.dates.MO))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d\n%b'))
    ax.xaxis.set_minor_locator(matplotlib.dates.DayLocator())

    # "Mill Road bridge will be closed to motor traffic for eight weeks from Monday 1 July"
    #
    # "The bridge will be fully closed from 8.45am until 8.45pm on
    # "Friday 5 July to Monday 8 July; Thursday 11 July to Saturday 13
    # "July; Sunday 28 July to Wednesday 31 July and Saturday 3 August
    # "to Monday 5 August.
    #
    # https://www.cambridgenetwork.co.uk/news/mill-road-remain-open-while-bridge-closed

    # All end dates extended by one day to include the last day

    left, right = ax.get_xlim()
    ax.axvspan(date(2019, 7, 1), date(2019, 8, 24), facecolor='k', alpha=0.1, zorder=1)
    ax.axvspan(date(2019, 7, 5), date(2019, 7, 9), facecolor='k', alpha=0.05, zorder=1)
    ax.axvspan(date(2019, 7, 11), date(2019, 7, 14), facecolor='k', alpha=0.05, zorder=1)
    ax.axvspan(date(2019, 7, 28), date(2019, 8, 1), facecolor='k', alpha=0.05, zorder=1)
    ax.axvspan(date(2019, 8, 3), date(2019, 8, 6), facecolor='k', alpha=0.05, zorder=1)
    # Reset xlim because otherwise the axvspan makes them bigger each time around!
    ax.set_xlim(left, right)


def do_graphs(axs_row, countline, direction, start, end):

    df = pd.DataFrame(get_data(countline, direction, start, end))
    df.columns = ('Date', 'Pedestrian', 'Cyclist', 'Motor')
    df.index = pd.to_datetime(df['Date'])

    df = df.resample('D').sum()

    do_graph(df, axs_row[0], col='Pedestrian')
    do_graph(df, axs_row[1], col='Cyclist')
    do_graph(df, axs_row[2], col='Motor')

    title = (f"{COUNTLINES[countline]['name']}\n"
             f"{COUNTLINES[countline][direction]}\n"
             "Per day")
    axs_row[0].set(xlabel='', ylabel=title)


def setup_figure():

    fig, axs_list = pyplot.subplots(nrows=ROWS_PER_PAGE,
                                    ncols=3,
                                    sharex=True,
                                    sharey=True,
                                    figsize=FIGSIZE)

    axs_list[0, 0].set_title('Pedestrian')
    axs_list[0, 1].set_title('Cyclist')
    axs_list[0, 2].set_title('Motor vehicle')

    return fig, axs_list


def run():
    '''
    For each countline
        For each of in and out
            Accumulate pedestrian/bike/other
                For each day in range
            Plot graph
    '''

    # 'seaborn-dark', 'seaborn-darkgrid', 'seaborn-ticks',
    # fivethirtyeight', 'seaborn-whitegrid', 'classic',
    # '_classic_test', 'fast', 'seaborn-talk', 'seaborn-dark-palette',
    # 'seaborn-bright', 'seaborn-pastel', 'grayscale',
    # 'seaborn-notebook', 'ggplot', 'seaborn-colorblind',
    # 'seaborn-muted', 'seaborn', 'Solarize_Light2', 'seaborn-paper'#,
    # 'bmh', 'tableau-colorblind10', 'seaborn-white', 'dark_background',
    # 'seaborn-poster', 'seaborn-deep']

    # pyplot.style.use('seaborn')

    row = 0
    fig = None
    with PdfPages('plot.pdf') as pdf:
        for countline in sorted(COUNTLINES.keys(), key=lambda k: COUNTLINES[k]['name']):
            for direction in ['in', 'out']:
                if row % ROWS_PER_PAGE == 0:
                    if row > 0:
                        fig.tight_layout()
                        pdf.savefig(fig)
                    fig, axs_list = setup_figure()
                do_graphs(axs_list[row % ROWS_PER_PAGE], countline, direction, START, END)
                row += 1

        fig.tight_layout()
        pdf.savefig(fig)


if __name__ == '__main__':
    run()
