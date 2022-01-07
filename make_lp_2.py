import pandas
import numpy as np
import scipy.stats
import itertools

# CSVの読み込み
data = pandas.read_csv('data.csv').fillna(0)

print(data)
print(data[18:19][['値段']])

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

# 標準化
ev_d = scipy.stats.zscore(ev)
cp_d = scipy.stats.zscore(cp)
sz_d = scipy.stats.zscore(sz)
wh_d = scipy.stats.zscore(wh)
ts_d = scipy.stats.zscore(ts)
co_d = scipy.stats.zscore(co)
pw_d = scipy.stats.zscore(pw)

pr_d = scipy.stats.zscore(pr)
po_d = scipy.stats.zscore(po)
pt_d = scipy.stats.zscore(pt)
cl_d = scipy.stats.zscore(cl)
se_d = scipy.stats.zscore(se)


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

print(sz_d)
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
    pr_ij = pr_d[row]
    po_ij = po_d[row]
    pt_ij = pt_d[row]
    cl_ij = cl_d[row]
    se_ij = se_d[row]

    # 目的関数セッション
    str_maximize += add_value(True, ev_i) + " " + var_name
    str_maximize += add_value(False, sz_i) + " " + var_name
    str_maximize += add_value(False, wh_i) + " " + var_name
    str_maximize += add_value(False, pw_i) + " " + var_name
    str_maximize += add_value(True, co_i) + " " + var_name
    str_maximize += add_value(False, pr_ij) + " " + var_name
    str_maximize += add_value(False, po_ij) + " " + var_name
    str_maximize += add_value(True, pt_ij) + " " + var_name
    str_maximize += add_value(True, cl_ij) + " " + var_name
    str_maximize += add_value(True, se_ij) + " " + var_name

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
