#!/usr/bin/env python3

from matplotlib.backends.backend_pdf import PdfPages

from graphit_base import get_traffic_data, do_graph_set, day_scatter_graph, hourly_average

ZONES = [
         'madingley_road_outer_in',
         'madingley_road_outer_out',
         'madingley_road_in',
         'madingley_road_out',
         ]


def run():

    # Slurp the data

    df = get_traffic_data()
    df = df[df.index.dayofweek < 5]
    df = df['2019-05-01':]

    with PdfPages('journey_time_maddingley_road_area_buses.pdf') as pdf:

        for between in (('07:00', '09:00'), ('16:00', '18:00')):

            title = f'Journey times, Mon-Fri, {between[0]}-{between[1]}'

            # do_graph_set(pdf, df.between_time(*between).copy(), day_scatter_graph, ZONES, title, 30)
            do_graph_set(pdf, df.between_time(*between).copy(), day_scatter_graph, ZONES, title, 50)

        title = 'Average journey times, Mon-Fri'
        # do_graph_set(pdf, df, hourly_average, ZONES, title, 10)
        do_graph_set(pdf, df, hourly_average, ZONES, title, 15)


if __name__ == '__main__':
    run()
