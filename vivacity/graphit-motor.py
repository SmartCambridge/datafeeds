#!/usr/bin/env python3

from graphit_base import run_graphs, do_bar_graph_by_day, do_bar_graph_by_hour, START, END

YMAX = 13000


def do_daily_motor_bar_graphs(df, axs_row):

    '''
    motorbike, car + taxi, minibus + bus, van + rigid + truck,
    emergency car + emergency van + fire engine
    '''

    df = df.resample('D').sum()

    df['car_taxi'] = df['car'] + df['taxi']
    df['all_bus'] = df['minibus'] + df['bus']
    df['goods'] = df['van'] + df['rigid'] + df['truck']

    # df['emergency'] = df['emergency car'] + df['emergency van'] + df['fire engine']

    do_bar_graph_by_day(df, axs_row[0], 'car_taxi', 12000)
    do_bar_graph_by_day(df, axs_row[1], 'goods', 2500)
    do_bar_graph_by_day(df, axs_row[2], 'all_bus', 600)
    do_bar_graph_by_day(df, axs_row[3], 'motorbike', 600)


def do_daily_motor_bar_graphs_fixed(df, axs_row):

    '''
    As do_daily_motor_bar_graphs, but with a common y axis scale
    '''

    df = df.resample('D').sum()

    df['car_taxi'] = df['car'] + df['taxi']
    df['all_bus'] = df['minibus'] + df['bus']
    df['goods'] = df['van'] + df['rigid'] + df['truck']

    # df['emergency'] = df['emergency car'] + df['emergency van'] + df['fire engine']
    do_bar_graph_by_day(df, axs_row[0], 'car_taxi', 12000)
    do_bar_graph_by_day(df, axs_row[1], 'goods', 12000)
    do_bar_graph_by_day(df, axs_row[2], 'all_bus', 12000)
    do_bar_graph_by_day(df, axs_row[3], 'motorbike', 12000)


def do_hourly_bar_graphs(df, axs_row):

    df = df.resample('H').sum()

    df['car_taxi'] = df['car'] + df['taxi']
    df['all_bus'] = df['minibus'] + df['bus']
    df['goods'] = df['van'] + df['rigid'] + df['truck']

    df = df.groupby(df.index.hour).mean()

    do_bar_graph_by_hour(df, axs_row[0], 'car_taxi', 700)
    do_bar_graph_by_hour(df, axs_row[1], 'goods', 150)
    do_bar_graph_by_hour(df, axs_row[2], 'all_bus', 40)
    do_bar_graph_by_hour(df, axs_row[3], 'motorbike', 40)


def run():

    run_graphs(
        'motor-date.pdf',
        'Motor traffic',
        START,
        END,
        ('Cars (incl. Taxis)', 'Goods vehicles (Vans, Rigid and Trucks)',
            'Buses (and Minibuses)', 'Motorbikes'),
        do_daily_motor_bar_graphs,
        'Per day',
        sharey=False)

    run_graphs(
        'motor-date-fixed.pdf',
        'Motor traffic (uniform Y axis)',
        START,
        END,
        ('Cars (incl. Taxis)', 'Goods vehicles (Vans, Rigid and Trucks)',
            'Buses (and Minibuses)', 'Motorbikes'),
        do_daily_motor_bar_graphs_fixed,
        'Per day',
        sharey=True)

    run_graphs(
        'motor-hour.pdf',
        f'Average hourly motor traffic ({START.isoformat()} - {END.isoformat()})',
        START,
        END,
        ('Cars (incl. Taxis)', 'Goods vehicles (Vans, Rigid and Trucks)',
            'Buses (and Minibuses)', 'Motorbikes'),
        do_hourly_bar_graphs,
        'Per hour',
        sharey=False)


if __name__ == '__main__':
    run()
