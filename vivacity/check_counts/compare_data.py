#!/usr/bin/env python3

import json
import os

from datetime import date

import pandas as pd
import matplotlib
from matplotlib.pyplot import subplots

from matplotlib.backends.backend_pdf import PdfPages

from tabulate import tabulate

'''

Vivacity to COBA 7

ped   pedestrian         Ped
cyc   cyclist            Cyc pavement + Cyc Road
mb    motorbike          M/B
car   car                Cars
      taxi               Cars
lgv   van                LGV
      minibus            Car
psv   bus                PSV
ogv1  rigid              OGV1
ogv2  truck              OGV2
      emergency car      Cars
      emergency van      Cars
      fire engine


'''

COUNTLINE = '13079'
DAY = date(2019, 7, 18)


def get_vivacity_data(countline, day, direction):
    '''
    Retrieve data for `countline` in `direction` on `day`
    Input format below. Output is a 2D array
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

    VCLASSES = ("pedestrian", "cyclist", "motorbike", "car",
                "taxi", "van", "minibus", "bus", "rigid",
                "truck", "emergency car", "emergency van",
                "fire engine")

    COLS = ("v_ped", "v_cyc", "v_mb", "v_car",
            "v_taxi", "v_lgv", "v_minibus", "v_psv", "v_ogv1",
            "v_ogv2", "v_emerg_car", "v_emerg_van",
            "v_fire_engine")


    data = []

    filename = os.path.join(
        '..',
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

    df = pd.DataFrame(data)

    df.columns = ('date',) + COLS
    df.index = pd.to_datetime(df['date'], utc=True)

    df['v_car'] = df.v_car + df.v_taxi + df.v_minibus + df.v_emerg_car + df.v_emerg_van
    df['v_gall'] = df.v_lgv + df.v_ogv1 + df.v_ogv2
    df['v_all'] = df.v_ped + df.v_cyc + df.v_mb + df.v_car + df.v_lgv + df.v_psv + df.v_ogv1 + df.v_ogv2

    df.drop(columns=['date', 'v_taxi', 'v_minibus', 'v_emerg_car', 'v_emerg_van', 'v_fire_engine'],
            inplace=True)

    df = df.resample('15T').sum()

    return df


def get_check_counts():

    names = [
      'times',
      'c_car_out', 'c_lgv_out', 'c_ogv1_out', 'c_ogv2_out', 'c_psv_out',
      'c_mb_out', 'c_cyc_road_out', 'c_cyc_pavement_out', 'c_ped_out',
      'c_car_in', 'c_lgv_in', 'c_ogv1_in', 'c_ogv2_in', 'c_psv_in',
      'c_mb_in', 'c_cyc_road_in', 'c_cyc_pavement_in', 'c_ped_in'
    ]

    cols = [0] + list(range(3, 21))

    df = pd.read_csv('counts_raw.csv', skiprows=6, names=names, usecols=cols)

    df.index = pd.to_datetime('2019-07-18T' + df.times)
    df.index = df.index.tz_localize('Europe/London')

    df['c_cyc_in'] = df.c_cyc_pavement_in + df.c_cyc_road_in
    df['c_cyc_out'] = df.c_cyc_pavement_out + df.c_cyc_road_out

    df['c_gall_in'] = (df.c_lgv_in + df.c_ogv1_in + df.c_ogv2_in)
    df['c_gall_out'] = (df.c_lgv_out + df.c_ogv1_out + df.c_ogv2_out)

    df['c_all_in'] = (df.c_ped_in + df.c_cyc_in + df.c_mb_in + df.c_car_in +
                      df.c_lgv_in + df.c_psv_in + df.c_ogv1_in + df.c_ogv2_in)
    df['c_all_out'] = (df.c_ped_out + df.c_cyc_out + df.c_mb_out + df.c_car_out +
                       df.c_lgv_out + df.c_psv_out + df.c_ogv1_out + df.c_ogv2_out)

    df.drop(columns=['times'], inplace=True)

    return df


# Vivacity 'in' is 'outbund', and vv.
vdf_outbound = get_vivacity_data(COUNTLINE, DAY, 'in')
vdf_outbound.columns = [x + '_out' for x in vdf_outbound.columns]
# print(vdf_outbound.head())

vdf_inbound = get_vivacity_data(COUNTLINE, DAY, 'out')
vdf_inbound.columns = [x + '_in' for x in vdf_inbound.columns]
# print(vdf_inbound.head())

cdf = get_check_counts()
# print(cdf.head())

# vdf_out contains 'inbound' data, and vv.
df = pd.concat([vdf_outbound, vdf_inbound, cdf], axis=1, sort=False)
# print(df[['v_ped_in', 'v_ped_out', 'c_ped_in', 'c_ped_out']])

# print((df['v_ped_in']-df['c_ped_in']).dropna())
# print(sum((df['v_ped_in']-df['c_ped_in']).dropna()))


def setup_figure():

    fig, axs_list = subplots(
        nrows=ROWS_PER_PAGE,
        ncols=2,
        sharex=True,
        sharey=False,
        figsize=FIGSIZE,
        squeeze=False)

    fig.suptitle('Vehicle count comparisons, Milton Road, 2018-07-18', fontsize=13)

    return fig, axs_list


vtypes = {
    'ped':  'Pedestrian',
    'cyc':  'Cyclist',
    'mb':   'Motorbike',
    'car':  'Car',
    'lgv':  'Light Goods (LGV)',
    'psv':  'Bus (PSV)',
    'ogv1': 'Rigid Goods (OGV1)',
    'ogv2': 'Truck (OGV2)',
    'gall': 'All Goods',
    'all':  'All Types'
}

vlimits = {
    'ped':  40,
    'cyc':  120,
    'mb':   12,
    'car':  200,
    'lgv':  50,
    'psv':  14,
    'ogv1': 12,
    'ogv2': 6,
    'gall': 80,
    'all':  400
}


MM_TO_INCH = 0.0393701
A4P = (210*MM_TO_INCH, 297*MM_TO_INCH)
A3P = (297*MM_TO_INCH, 420*MM_TO_INCH)
A3L = (420*MM_TO_INCH, 297*MM_TO_INCH)

ROWS_PER_PAGE = 4
FIGSIZE = A3L

row = 0
fig = None
with PdfPages('comparison.pdf') as pdf:
    for type_key, type_desc in vtypes.items():
        if row % ROWS_PER_PAGE == 0:
            if fig:
                fig.tight_layout(rect=[0, 0, 1, 0.96])
                pdf.savefig(fig)
            fig, axs_list = setup_figure()
            axs_list[0, 0].set_title('Inbound')
            axs_list[0, 1].set_title('Outbound')

        ax_row = axs_list[row % ROWS_PER_PAGE]

        df.plot(y=[f'v_{type_key}_in', f'c_{type_key}_in'], ax=ax_row[0], ylim=(0,vlimits[type_key]))
        df.plot(y=[f'v_{type_key}_out', f'c_{type_key}_out'], ax=ax_row[1], ylim=(0,vlimits[type_key]))

        #ax_row[0].xaxis.set_major_locator(matplotlib.dates.HourLocator(interval=1))
        ax_row[0].xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
        ax_row[0].xaxis.set_minor_locator(matplotlib.ticker.NullLocator())

        #ax_row[1].xaxis.set_major_locator(matplotlib.dates.HourLocator(interval=1))
        ax_row[1].xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
        ax_row[0].xaxis.set_minor_locator(matplotlib.ticker.NullLocator())

        ax_row[0].legend(['Vivacity', 'ATR'])
        ax_row[1].legend(['Vivacity', 'ATR'])

        ax_row[0].set(ylabel=type_desc + '\n(per 15 minutes)')

        row += 1

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    pdf.savefig(fig)


df2 = df.dropna()
print(df2)

rows = []
for type_key, type_desc in vtypes.items():
    for direction in 'in', 'out':
        v = df2[f'v_{type_key}_{direction}'].sum()
        c = df2[f'c_{type_key}_{direction}'].sum()
        rows.append((type_desc, direction, v, c, v-c, f'{(v-c)/v*100:.2f}%'))

print(tabulate(rows, headers=('Type', 'Dir', 'Vivacity', 'ATR', 'Diff', '%'),
      colalign=('left', 'left', 'right', 'right', 'right', 'right')))

for direction in 'in', 'out':
    print(f'Cyc pavement Cyc Road {direction}',
          df2[f'c_cyc_pavement_{direction}'].sum(),
          df2[f'c_cyc_road_{direction}'].sum())
