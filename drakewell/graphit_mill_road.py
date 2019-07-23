#!/usr/bin/env python3

from matplotlib.backends.backend_pdf import PdfPages

from graphit_base import get_drakewell_data, do_graph_set, day_scatter_graph, hourly_average

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


def run():

    # Slurp the data

    df = get_drakewell_data()
    df = df[df.index.dayofweek < 5]

    with PdfPages('journey_time_mill_road_area.pdf') as pdf:

        for between in (('07:00', '09:00'), ('16:00', '18:00')):

            title = f'Journey times, Mon-Fri, {between[0]}-{between[1]}'

            do_graph_set(pdf, df.between_time(*between).copy(), day_scatter_graph, LINKS, title, 30)

        title = 'Average journey times, Mon-Fri'
        do_graph_set(pdf, df, hourly_average, LINKS, title, 10)


if __name__ == '__main__':
    run()
