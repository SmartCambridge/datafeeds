#!/usr/bin/env python3

from matplotlib.backends.backend_pdf import PdfPages

from graphit_base import get_drakewell_data, do_graph_set, day_scatter_graph, hourly_average

LINKS = [
    '9800ZQVSTZQ0',
    '9800X9JXWMZU',
    '9800W3ZWF41I',
    '9800XVOXBNLX'
]


def run():

    # Slurp the data

    df = get_drakewell_data()
    df = df[df.index.dayofweek < 5]

    with PdfPages('journey_time_madingley_road.pdf') as pdf:

        for between in (('07:00', '09:00'), ('16:00', '18:00')):

            title = f'Journey times, Mon-Fri, {between[0]}-{between[1]}'

            do_graph_set(pdf, df.between_time(*between).copy(), day_scatter_graph, LINKS, title, 50)

        title = 'Average journey times, Mon-Fri'
        do_graph_set(pdf, df, hourly_average, LINKS, title, 15)


if __name__ == '__main__':
    run()
