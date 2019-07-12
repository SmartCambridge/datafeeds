#!/usr/bin/env python3

import json
import os

from datetime import date, timedelta

import pandas as pd

from matplotlib.pyplot import subplots
from matplotlib.backends.backend_pdf import PdfPages

ONE_DAY = timedelta(days=1)
MM_TO_INCH = 0.0393701
A4P = (210*MM_TO_INCH, 297*MM_TO_INCH)
A3P = (297*MM_TO_INCH, 420*MM_TO_INCH)
A3L = (420*MM_TO_INCH, 297*MM_TO_INCH)

ROWS_PER_PAGE = 6
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


VCLASSES = ("pedestrian", "cyclist", "motorbike", "car",
            "taxi", "van", "minibus", "bus", "rigid",
            "truck", "emergency car", "emergency van",
            "fire engine")


def get_data(countline, direction, start, end):
    '''
    Retrieve data for `countline` in `direction` between the days
    from `start` to `end`. Input format below. Output is a 2D array
    with one row per sample.

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
                    data_block = json.loads(line)
                    row = ([data_block['timestamp']] +
                           [data_block['counts'][key] for key in VCLASSES])
                    data.append(row)
        except FileNotFoundError:
            pass
        day += ONE_DAY

    return data


def hilight_bridge_closure(ax):
    '''
    Highlight Mill Road bridge closure

    "Mill Road bridge will be closed to motor traffic for eight weeks from Monday 1 July"

    "The bridge will be fully closed from 8.45am until 8.45pm on
    "Friday 5 July to Monday 8 July; Thursday 11 July to Saturday 13
    "July; Sunday 28 July to Wednesday 31 July and Saturday 3 August
    "to Monday 5 August.

    https://www.cambridgenetwork.co.uk/news/mill-road-remain-open-while-bridge-closed

    All end dates extended by one day so tht the highlight includes the last day
    '''

    left, right = ax.get_xlim()
    ax.axvspan(date(2019, 7, 1), date(2019, 8, 24), facecolor='k', alpha=0.1, zorder=1)
    ax.axvspan(date(2019, 7, 5), date(2019, 7, 9), facecolor='k', alpha=0.05, zorder=1)
    ax.axvspan(date(2019, 7, 11), date(2019, 7, 14), facecolor='k', alpha=0.05, zorder=1)
    ax.axvspan(date(2019, 7, 28), date(2019, 8, 1), facecolor='k', alpha=0.05, zorder=1)
    ax.axvspan(date(2019, 8, 3), date(2019, 8, 6), facecolor='k', alpha=0.05, zorder=1)
    # Reset xlim because otherwise the axvspan makes them bigger each time around!
    ax.set_xlim(left, right)


def setup_figure(labels):

    ncols = len(labels)

    fig, axs_list = subplots(
        nrows=ROWS_PER_PAGE,
        ncols=ncols,
        sharex=True,
        sharey=True,
        figsize=FIGSIZE)

    for col, label in enumerate(labels):
        axs_list[0, col].set_title(label)

    return fig, axs_list


def run_graphs(filename, start, end, labels, function):
    '''
    Draw a set of graphs for both directions on all countlines for the
    period from `start` to `end`. Use `function` to draw each set, and label
    the columns with `labels`.

    `function` has the signature

    def function(df, axs_list):

    where:

        * `df` is a data frame containing the raw data
        * `axis_list` is a list of matplotlib 'axis' objects (one
           for each member of `labels`) into which `function` should
           render graphs

    '''

    row = 0
    fig = None
    with PdfPages(filename) as pdf:
        for countline in sorted(COUNTLINES.keys(), key=lambda k: COUNTLINES[k]['name']):
            for direction in ['in', 'out']:
                if row % ROWS_PER_PAGE == 0:
                    if row > 0:
                        fig.tight_layout()
                        pdf.savefig(fig)
                    fig, axs_list = setup_figure(labels)
                # Get the data
                df = pd.DataFrame(get_data(countline, direction, start, end))
                df.columns = ('Date',) + VCLASSES
                df.index = pd.to_datetime(df['Date'])
                # ... and graph it
                function(df, axs_list[row % ROWS_PER_PAGE])
                title = (f"{COUNTLINES[countline]['name']}\n"
                         f"{COUNTLINES[countline][direction]}\n"
                         "Per day")
                axs_list[row % ROWS_PER_PAGE, 0].set(xlabel='', ylabel=title)
                row += 1

        fig.tight_layout()
        pdf.savefig(fig)
