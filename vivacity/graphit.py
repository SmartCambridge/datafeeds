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
END = date(2019, 7, 8)
YMAX = 13000
FIGSIZE = A3L

COUNTLINES = {
    '13069': {'name': 'Tennison Road', 'in': 'north-bound', 'out': 'south-bound'},
    '13070': {'name': 'Coleridge Road', 'in': 'south-bound', 'out': 'north-bound'},
    '13071': {'name': 'Mill Road (Prene Road end)', 'in': 'west-bound', 'out': 'east-bound'},
    '13072': {'name': 'Vinery Road', 'in': 'south-bound', 'out': 'north-bound'},
    '13073': {'name': 'Cherry Hinton Road', 'in': 'east-bound', 'out': 'west-bound'},
    '13074': {'name': 'Station Road', 'in': 'west-bound', 'out': 'east-bound'},
    '13075': {'name': 'East Road', 'in': 'north-east-bound', 'out': 'south-west-bound'},
    '13076': {'name': 'Coldhams Lane', 'in': 'south-bound', 'out': 'north-bound'},
    '13077': {'name': 'Mill Road (city end)', 'in': 'south-east-bound', 'out': 'north-west-bound'},
    '13078': {'name': 'Carter Bridge', 'in': 'west-bound', 'out': 'east-bound'},
    '13079': {'name': 'Milton Road', 'in': 'north-east-bound', 'out': 'south-west-bound'},
    '13080': {'name': 'Hills Road', 'in': 'south-bound', 'out': 'north-bound'},
    '13081': {'name': 'Newmarket Road', 'in': 'west-bound', 'out': 'east-bound'},
    '13082': {'name': 'Histon Road', 'in': 'south-bound', 'out': 'north-bound'},
    '13086': {'name': 'Perne Road', 'in': 'north-bound', 'out': 'south-bound'},
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

    ax.bar(df.index, df[col], zorder =3)

    ax.grid(axis='y', zorder=2)
    ax.xaxis.set_major_locator(matplotlib.dates.WeekdayLocator(byweekday=matplotlib.dates.MO))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d\n%b'))
    ax.xaxis.set_minor_locator(matplotlib.dates.DayLocator())

    left, right = ax.get_xlim()
    ax.axvspan(date(2019, 7, 1), matplotlib.dates.num2date(right), facecolor='k', alpha=0.1, zorder=1)
    # Reset xlim becasue otherwise the axvspan makes them bigger each time around!
    ax.set_xlim(left, right)


def do_graphs(axs, row, countline, direction, start, end):

    df = pd.DataFrame(get_data(countline, direction, start, end))
    df.columns = ('Date', 'Pedestrian', 'Cyclist', 'Motor')
    df.index = pd.to_datetime(df['Date'])

    df = df.resample('D').sum()

    do_graph(df, axs[row, 0], col='Pedestrian')
    do_graph(df, axs[row, 1], col='Cyclist')
    do_graph(df, axs[row, 2], col='Motor')

    title = (f"{COUNTLINES[countline]['name']} "
             f"{COUNTLINES[countline][direction]} "
             f"[{countline} {direction}]")
    axs[row, 0].annotate(title, xy=(0.01, 0.85), xycoords="axes fraction")
    axs[row, 0].set(xlabel='', ylabel='Per day')

    if row % ROWS_PER_PAGE == 0:
        axs[row, 0].set_title('Pedestrian')
        axs[row, 1].set_title('Cyclist')
        axs[row, 2].set_title('Motor vehicle')


def setup_figure():

    fig, axs = pyplot.subplots(nrows=ROWS_PER_PAGE,
                               ncols=3,
                               sharex=True,
                               sharey=True,
                               figsize=FIGSIZE)

    #fig.tight_layout()

    return fig, axs


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
                        pdf.savefig(fig)
                    fig, axs = setup_figure()
                do_graphs(axs, row % ROWS_PER_PAGE, countline, direction, START, END)
                row += 1

        pdf.savefig(fig)


if __name__ == '__main__':
    run()
