import pandas
import numpy as np
import scipy.stats
from sklearn import preprocessing

# CSVの読み込み
data = pandas.read_csv('data.csv').fillna(0)
print(data)

str_maximize = "maximize\n"
str_subject_to = "subject to\n"
str_c1 = "c1: "
str_c2 = "c2: "
str_c3 = "c3: "
str_bounds = "bounds\n"
str_general = "binary\n"

M = len(data)

# データから各配列に定数を格納する
ev = []
cp = []
sz = []
wh = []
ts = []
co = []
pw = []
pr = []
po = []
pt = []
cl = []
se = []
before_i = 0
for row in range(M):
    i = data.iat[row, 0]
    j = data.iat[row, 13]

    # 製品ごとに変化する定数
    if before_i != i:
        ev.append(data.iat[row, 3])
        cp.append(data.iat[row, 5])
        sz.append(data.iat[row, 6] * data.iat[row, 7] * data.iat[row, 8])
        wh.append(data.iat[row, 9])
        ts.append(data.iat[row, 10])
        co.append(data.iat[row, 11])
        pw.append(data.iat[row, 12])
        before_i = i

    # 販売店舗ごとに変化する定数
    pr.append(data.iat[row, 15])
    po.append(data.iat[row, 16])
    pt.append(data.iat[row, 17])
    cl.append(data.iat[row, 18])
    se.append(data.iat[row, 20])

# 商品の総数
total_products = before_i

# 正規化
ev_d = preprocessing.minmax_scale(ev)
cp_d = preprocessing.minmax_scale(cp)
sz_d = preprocessing.minmax_scale(sz)
wh_d = preprocessing.minmax_scale(wh)
ts_d = preprocessing.minmax_scale(ts)
co_d = preprocessing.minmax_scale(co)
pw_d = preprocessing.minmax_scale(pw)

se_d = preprocessing.minmax_scale(se)


def add_value(plus, v):
    if plus:
        if v < 0.0:
            return " - " + str(abs(v))
        else:
            return " + " + str(v)
    else:
        if v < 0.0:
            return " + " + str(abs(v))
        else:
            return " - " + str(v)


# 重み係数の定義
w_ev = 10
w_ts = 10
w_sz = 5
w_wh = 5
w_pw = 2
w_co = 2
w_pr = 20
w_po = 18
w_pt = 18
w_cl = 5
w_se = 5

"""
w_ev = 80
w_ts = 80
w_sz = 10
w_wh = 10
w_pw = 5
w_co = 5
w_pr = 100
w_po = 100
w_pt = 100
w_cl = 10
w_se = 10
"""

# 文字列型として目的関数と各成約式の文字列を生成
for row in range(M):
    i = data.iat[row, 0]
    j = data.iat[row, 13]

    # 変数名
    var_name = "x(" + str(i) + "," + str(j) + ")"

    # 各データの取得
    ev_i = ev_d[i - 1]
    cp_i = cp_d[i - 1]
    sz_i = sz_d[i - 1]
    wh_i = wh_d[i - 1]
    ts_i = ts_d[i - 1]
    co_i = co_d[i - 1]
    pw_i = pw_d[i - 1]
    pr_ij = data.iat[row, 15] * 0.0001
    po_ij = data.iat[row, 16] * 0.0001
    pt_ij = data.iat[row, 17] * 0.0001
    cl_ij = data.iat[row, 18] * 0.0001
    se_ij = se_d[row]

    # 目的関数セッション
    str_maximize += add_value(True, w_ev * ev_i) + " " + var_name
    str_maximize += add_value(False, w_sz * sz_i) + " " + var_name
    str_maximize += add_value(False, w_wh * wh_i) + " " + var_name
    str_maximize += add_value(False, w_pw * pw_i) + " " + var_name
    str_maximize += add_value(True, w_co * co_i) + " " + var_name
    str_maximize += add_value(False, w_pr * pr_ij) + " " + var_name
    str_maximize += add_value(False, w_po * po_ij) + " " + var_name
    str_maximize += add_value(True, w_pt * pt_ij) + " " + var_name
    str_maximize += add_value(True, w_cl * cl_ij) + " " + var_name
    str_maximize += add_value(True, w_se * se_ij) + " " + var_name

    if row < M - 1:
        str_maximize += " + "

    # 制約式セッション
    str_c1 += var_name
    if row < M - 1:
        str_c1 += " + "

    str_c2 += str(cp[i - 1]) + " " + var_name
    if row < M - 1:
        str_c2 += " + "

    str_c3 += str(pr[row]) + " " + var_name
    if row < M - 1:
        str_c3 += " + "

    # 上下限セッション
    str_bounds += var_name
    if row < M - 1:
        str_bounds += "\n"

    # 変数型セッション
    str_general += var_name
    if row < M - 1:
        str_general += "\n"

str_c1 += " >= 1"
str_c2 += " >= 6000"
str_c3 += " <= 30000"
str_subject_to += str_c1 + "\n" + str_c2 + "\n" + str_c3 + "\n"

i_num = 1
str_c4p = "c4: "
for row in range(M):
    i = data.iat[row, 0]
    j = data.iat[row, 13]

    if i_num != i:
        i_num = i
        str_c4p += " <= 1"
        str_subject_to += str_c4p + "\n"
        str_c4p = "c" + str(4 - 1 + i) + ": "

    if j > 1:
        str_c4p += " + "
    str_c4p += "x(" + str(i) + "," + str(j) + ")"

str_c4p += " <= 1"
str_subject_to += str_c4p

print(str_maximize)
print(str_subject_to)
print(str_bounds)
print(str_general)
print("end")

f = open('buy_hdd.lp', 'w')
f.write(str_maximize + "\n" + str_subject_to + "\n" + str_bounds + "\n" + str_general + "\nend")
f.close()
