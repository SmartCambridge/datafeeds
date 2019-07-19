#!/usr/bin/env python3

import json
import matplotlib.pyplot
import re
import sys

from datetime import date

import pandas as pd

sys.path.append('../vivacity')
from graphit_base import hilight_bridge_closure, setup_axies

TO_MPH = 2.23694

DATAFILES = [
    'downloaded_data/2019-05.csv',
    'downloaded_data/2019-06.csv',
    'downloaded_data/2019-07.csv'
]

LINKS = [
    '9800YBB3C3Z3',
]

'''
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
    '9800XVT0GHMV'
]
'''


def fix_labels(labels):

    result = []
    for label in labels:
        day = date.fromisoformat(label.get_text())
        if day.day == 1:
            result.append(day.strftime('%d\n%b\n%Y'))
        elif day.day in (8, 15, 22):
            result.append(day.strftime('%d'))
        else:
            result.append('')
    return result


def percentile(n):
    def percentile_(x):
        return x.quantile(n)
    percentile_.__name__ = 'percentile_{:2.0f}'.format(n*100)
    return percentile_


# Slurp the data

df = pd.concat(map(pd.read_csv, DATAFILES))
df.columns = ['node', 'cosit', 'timestamp', 'period', 'seconds', 'count']
df.index = pd.to_datetime(df['timestamp'])
df.drop('timestamp', axis=1, inplace=True)

# Slurp link details
with open('locations.json') as f:
    locations = json.load(f)
links = {re.sub(r'CAMBRIDGE_JTMS\|', '', record['id']): record for record in locations['links']}

print(links)

# Select morning peak
df = df.between_time('07:00', '09:00')

for link in LINKS:

    df2 = df[df.cosit == link]
    df2 = df2[df2.index.dayofweek < 5]

    df2['speed'] = (links[link]['length'] / df2['seconds']) * TO_MPH

    params = {
        'speed': [
            min,
            percentile(0.25),
            'median',
            percentile(0.75),
            max
        ]
    }
    grouped = df2.resample('D').agg(params)
    grouped.columns = grouped.columns.droplevel(level=0)
    print(grouped.head())

    fig, ax = matplotlib.pyplot.subplots(nrows=1, ncols=1, figsize=(10, 7))

    ax.errorbar(
        grouped.index,
        grouped['median'],
        yerr=[grouped['median'] - grouped['min'], grouped['max'] - grouped['median']],
        fmt='none',
        elinewidth=1,
        capsize=3,
        capwidth=2,
        ecolor='k')

    ax.errorbar(
        grouped.index,
        grouped['median'],
        yerr=[grouped['median'] - grouped['percentile_25'], grouped['percentile_75'] - grouped['median']],
        marker='_',
        mfc='k',
        mew='1',
        mec='k',
        ms=8,
        lw=0,
        elinewidth=4,
        capsize=0)

    hilight_bridge_closure(ax)

    setup_axies(ax, None)

    ax.xaxis.set_major_locator(matplotlib.dates.DayLocator(1))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('\n%b\n%Y'))
    ax.xaxis.set_minor_locator(matplotlib.dates.WeekdayLocator(matplotlib.dates.MO))
    ax.xaxis.set_minor_formatter(matplotlib.dates.DateFormatter('%d'))

    ax.grid(axis='y', which='major', zorder=2)
    ax.grid(axis='x', which='minor', zorder=2)

    matplotlib.pyplot.show()
    matplotlib.pyplot.close()
