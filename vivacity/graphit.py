#!/usr/bin/env python3

import json
import os

from datetime import date, timedelta

import pandas as pd

from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

ONE_DAY = timedelta(days=1)
MM_TO_INCH = 0.0393701
A4P = (210*MM_TO_INCH, 297*MM_TO_INCH)
A3P = (297*MM_TO_INCH, 420*MM_TO_INCH)
A3L = (420*MM_TO_INCH, 297*MM_TO_INCH)

ROWS = 6
START = date(2019, 6, 24)
END = date(2019, 7, 5)
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


def do_graph(axs, row, countline, direction, start, end):

    title = COUNTLINES[countline]['name'] + ' ' + COUNTLINES[countline][direction]

    data = get_data(countline, direction, start, end)
    df = pd.DataFrame(data)
    df.columns = ('Date', 'Pedestrian', 'Cyclist', 'Motor')
    df.index = pd.to_datetime(df['Date'])

    ymax = 1000

    df.resample('H').sum().plot(y=['Pedestrian'], ax=axs[row, 0], ylim=(0, ymax), legend=False)
    df.resample('H').sum().plot(y=['Cyclist'], ax=axs[row, 1], ylim=(0, ymax), legend=False)
    df.resample('H').sum().plot(y=['Motor'], ax=axs[row, 2], ylim=(0, ymax), legend=False)

    for ctr in range(3):
        axs[row, ctr].grid(axis='y')

    title = COUNTLINES[countline]['name'] + ' ' + COUNTLINES[countline][direction]
    axs[row, 0].annotate(title, xy=(0.01, 0.9), xycoords="axes fraction")


def setup_figure():

    fig, axs = pyplot.subplots(nrows=ROWS, ncols=3, sharex=True, sharey=True)

    pyplot.figtext(0.2, 0.9, 'Cyclist', figure=fig, size='large', ha='center')
    pyplot.figtext(0.5, 0.9, 'Pedestrian', figure=fig, size='large', ha='center')
    pyplot.figtext(0.8, 0.9, 'Motor', figure=fig, size='large', ha='center')

    for ax1 in axs:
        for ax2 in ax1:
            ax2.grid(axis='y')
            ax2.set_xlabel('')
            ax2.set_ylabel('Per hour')

    return fig, axs


def run():
    '''
    For each countline
        For each of in and out
            Accumulate pedestrian/bike/other
                For each day in range
            Plot graph
    '''

    pyplot.rc('figure', figsize=A3L)

    fig, axs = setup_figure()

    row = 0
    with PdfPages('plot.pdf') as pdf:
        for countline in sorted(COUNTLINES.keys(), key=lambda k: COUNTLINES[k]['name']):
            for direction in ['in', 'out']:
                do_graph(axs, row % ROWS, countline, direction, START, END)
                row += 1
                if row % ROWS == 0:
                    pdf.savefig(fig)
                    fig, axs = setup_figure()

        pdf.savefig(fig)


if __name__ == '__main__':
    run()
