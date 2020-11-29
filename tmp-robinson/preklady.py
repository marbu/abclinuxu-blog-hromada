#!/usr/bin/env python3
# -*- coding: utf8 -*-

# Copyright 2020 Martin Bukatovič
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import defaultdict
import argparse
import sys

import matplotlib.pyplot as plt
import pandas as pd


DATA_FILE = "preklady.tsv"


def classify(edition_type, author):
    if "adaptation" in edition_type:
        ad_type = "jiná"
        if "German" in edition_type:
            ad_type = "dle Německé předlohy"
        elif "Russian" in edition_type:
            ad_type = "dle Ruské předlohy"
        elif "Pleva" in author:
            ad_type = "Pleva"
        return f"adaptace: {ad_type}"
    if edition_type == "translation":
        translator = "jiný"
        if "Vyskočil" in author:
            translator = 'Vyskočil'
        elif "Lounský" in author:
            translator = 'Lounský, Svákovský'
        return f"překlad: {translator}"
    return 'neurčeno'


def get_period(start_year, period_len, year):
    if year < start_year:
        return None
    n = (year - start_year) // period_len
    period = n * period_len + start_year
    return period


def add_sparse_empty_values(chart_df, period_len):
    prev_col = chart_df.columns[0]
    for col in list(chart_df.columns[1:]):
        if col != prev_col + period_len:
            for missing_col in range(prev_col+period_len, col, period_len):
                chart_df[missing_col] = pd.Series(pd.arrays.SparseArray([]))
        prev_col = col


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="plot czech edition overview")
    ap.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="dry run, don't plot a chart, just print chart data to stdout")
    ap.add_argument(
        "-p",
        "--period",
        action="store",
        type=int,
        default=10,
        help="lenght of chart period: number of years per chart datapoint")
    ap.add_argument(
        "-s",
        "--start",
        action="store",
        type=int,
        default=1790,
        help="start of the chart, year of the 1st chart period")
    ap.add_argument(
        "-o",
        "--output",
        action="store",
        type=str,
        default="preklady.png",
        help="filename of the output chart")
    args = ap.parse_args()

    # source data about all czech editions
    editions = pd.read_csv(DATA_FILE, sep="\t")

    # chart data to be plotted: {period: {group: count}}
    chart_data = {}
    for _, row in editions.iterrows():
        period = get_period(args.start, args.period, row['Year'])
        if period is None:
            continue
        group = classify(row['Type'], row['Translated/Adapted by'])
        chart_data.setdefault(period, defaultdict(int))[group] += 1

    # plotting preparation
    chart_df = pd.DataFrame(chart_data)

    if args.dry_run:
        print(chart_df)
        sys.exit(0)

    # add sparse columns for empty periods ...
    add_sparse_empty_values(chart_df, args.period)
    # and sort column order, to place new empty columns properly
    chart_df = chart_df.reindex(sorted(chart_df.columns), axis=1)

    # plotting
    chart_df.T.plot(kind='bar', stacked=True)
    plt.savefig(args.output)
