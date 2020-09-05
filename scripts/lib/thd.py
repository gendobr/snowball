#!/usr/bin/env python2
# encoding: UTF-8

import pandas as pd


def top(df_terms):
    df_tmp = df_terms[df_terms['cvalue'] > 0].sort_values('cvalue', ascending=False)
    ns = df_tmp['cvalue'] * (1.0 / sum(df_tmp['cvalue']))
    df_tmp['ns'] = ns
    df_tmp['cumsum'] = ns.cumsum()
    cumsum_max = sum(ns) * 0.5
    df_tmp = df_tmp[df_tmp['cumsum'] <= cumsum_max]
    return min(df_tmp['cvalue']), df_tmp[['cvalue']]


# "Terminological Saturation in Retrospective Text Document Collections"
# T1,T2 - the bags of terms
#    Each term T1.term
#    is accompanied with its
#    T.n-score. T1, T2 are sorted in the descending order of T.n-score.
#    inputs are dataframes (index=term, score)

def thd(_T1, _T2):
    eps_T1, df_T1 = top(_T1)
    df_T1['ns'] = df_T1['cvalue'] / max(df_T1['cvalue'])

    eps_T2, df_T2 = top(_T2)
    df_T2['ns'] = df_T2['cvalue'] / max(df_T2['cvalue'])

    # print('eps_T2=', eps_T2)
    result = pd.concat([df_T1[['ns']].rename(columns={'ns': 'ns1'}), df_T2[['ns']].rename(columns={'ns': 'ns2'})],
                       axis=1, sort=False).fillna(0)
    result = result[result['ns2'] > 0]  # ignore terms from _T1 if they are not found in _T2

    diff = result['ns2'] - result['ns1']
    _thd = sum(diff.map(abs))

    _sum = sum(df_T2['ns'])
    _thdr = _thd / _sum

    return (eps_T2, _thd, _thdr)

