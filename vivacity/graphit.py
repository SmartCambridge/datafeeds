#!/usr/bin/env python3

import matplotlib

from datetime import date

from graphit_base import run_graphs, hilight_bridge_closure

START = date(2019, 5, 10)
END = date(2019, 7, 11)

YMAX = 13000


def do_bar_graph(df, ax, col, ymax):
    '''
    Plot column `col` from data frame `df` onto axis `ax` as a bar graph.
    '''

    ax.bar(df.index, df[col], zorder=3, align='edge')

    ax.set_ylim([0, ymax])
    if ymax < 1000:
        ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=200))
        ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(base=100))
    elif ymax < 3000:
        ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=1000))
        ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(base=200))
    else:
        ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=2500))
        ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(base=500))


    ax.grid(axis='y', zorder=2)
    ax.xaxis.set_major_locator(matplotlib.dates.WeekdayLocator(byweekday=matplotlib.dates.MO))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d\n%b'))
    ax.xaxis.set_minor_locator(matplotlib.dates.DayLocator())

    hilight_bridge_closure(ax)


def do_daily_bar_graphs(df, axs_row):

    col_list = list(df)
    col_list.remove('pedestrian')
    col_list.remove('cyclist')
    df['motor'] = df[col_list].sum(axis=1)

    df = df.resample('D').sum()

    do_bar_graph(df, axs_row[0], 'pedestrian', YMAX)
    do_bar_graph(df, axs_row[1], 'cyclist', YMAX)
    do_bar_graph(df, axs_row[2], 'motor', YMAX)


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

    do_bar_graph(df, axs_row[0], 'car_taxi', 12000)
    do_bar_graph(df, axs_row[1], 'goods', 2500)
    do_bar_graph(df, axs_row[2], 'all_bus', 600)
    do_bar_graph(df, axs_row[3], 'motorbike', 600)


def do_daily_motor_bar_graphs_fixed(df, axs_row):

    '''
    As do_daily_motor_bar_graphs, but with a common y axis scale
    '''

    df = df.resample('D').sum()

    df['car_taxi'] = df['car'] + df['taxi']
    df['all_bus'] = df['minibus'] + df['bus']
    df['goods'] = df['van'] + df['rigid'] + df['truck']

    # df['emergency'] = df['emergency car'] + df['emergency van'] + df['fire engine']

    do_bar_graph(df, axs_row[0], 'car_taxi', 12000)
    do_bar_graph(df, axs_row[1], 'goods', 12000)
    do_bar_graph(df, axs_row[2], 'all_bus', 12000)
    do_bar_graph(df, axs_row[3], 'motorbike', 12000)



def run():

    # run_graphs('3way.pdf', START, END, ('Pedestrian', 'Cyclist', 'Motor'), do_daily_bar_graphs)

    run_graphs(
        'motor.pdf', START, END,
        ('Cars (incl. Taxis)', 'Goods vehicles (Vans, Rigid and Trucks)',
            'Buses (and Minibuses)', 'Motorbikes'),
        do_daily_motor_bar_graphs, sharey=False)

    run_graphs(
        'motor2.pdf', START, END,
        ('Cars (incl. Taxis)', 'Goods vehicles (Vans, Rigid and Trucks)',
            'Buses (and Minibuses)', 'Motorbikes'),
        do_daily_motor_bar_graphs_fixed, sharey=True)


if __name__ == '__main__':
    run()
