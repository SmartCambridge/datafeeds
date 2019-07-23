#!/usr/bin/env python3

from matplotlib.backends.backend_pdf import PdfPages

from graphit_base import get_traffic_data, do_graph_set, day_scatter_graph, hourly_average

ZONES = [
         'cherry_hinton_road_in',
         'cherry_hinton_road_out',
         'hills_road_inner_in',
         'hills_road_inner_out',
         'gonville_place_out',
         'gonville_place_in',
         'east_road_out',
         'east_road_in',
         'perne_road_south',
         'perne_road_north',
         'hills_road_outer_in',
         'hills_road_outer_out',
         'babraham_road_in',
         'babraham_road_out',
         'lensfield_road_east',
         'lensfield_road_west',
         'cherry_hinton_road_outer_in',
         'cherry_hinton_road_outer_out',
         ]


def run():

    # Slurp the data

    df = get_traffic_data()
    df = df[df.index.dayofweek < 5]
    df = df['2019-05-01':]

    with PdfPages('journey_time_mill_road_area.pdf') as pdf:

        for between in (('07:00', '09:00'), ('16:00', '18:00')):

            title = f'Journey times, Mon-Fri, {between[0]}-{between[1]}'

            do_graph_set(pdf, df.between_time(*between).copy(), day_scatter_graph, ZONES, title, 30)

        title = 'Average journey times, Mon-Fri'
        do_graph_set(pdf, df, hourly_average, ZONES, title, 10)


if __name__ == '__main__':
    run()
