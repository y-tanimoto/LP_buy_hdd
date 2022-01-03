import pandas
import numpy as np

# CSVの読み込み
data = pandas.read_csv('data.csv')

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

max_pr = 0
max_sz = 0
max_po = 0

for row in range(M):
    sz_i = data.iat[row, 6] * data.iat[row, 7] * data.iat[row, 8]
    pr_ij = data.iat[row, 16]
    po_ij = data.iat[row, 17]

    if sz_i > max_sz:
        max_sz = sz_i
    if pr_ij > max_pr:
        max_pr = pr_ij
    if po_ij > max_po:
        max_po = po_ij

for row in range(M):
    i = data.iat[row, 0]
    j = data.iat[row, 14]

    # 変数名
    var_name = "x(" + str(i) + "," + str(j) + ")"

    # 各データの取得
    ev_i = data.iat[row, 3]
    cp_i = data.iat[row, 5]
    sz_i = data.iat[row, 6] * data.iat[row, 7] * data.iat[row, 8]
    wh_i = data.iat[row, 9]
    ts_i = data.iat[row, 12]
    pr_ij = data.iat[row, 16]
    po_ij = data.iat[row, 17]
    pt_ij = data.iat[row, 18] + data.iat[row, 19]

    if np.isnan(ev_i):
        ev_i = 0
    if np.isnan(cp_i):
        cp_i = 0
    if np.isnan(sz_i):
        sz_i = 0
    if np.isnan(wh_i):
        wh_i = 0
    if np.isnan(ts_i):
        ts_i = 0
    if np.isnan(pr_ij):
        pr_ij = 0
    if np.isnan(po_ij):
        po_ij = 0
    if np.isnan(pt_ij):
        pt_ij = 0

    # 目的関数セッション
    str_maximize += str(max_pr - pr_ij) + " " + var_name + " + "
    str_maximize += str(cp_i) + " " + var_name + " + "
    str_maximize += str(ev_i) + " " + var_name + " + "
    str_maximize += str(ts_i) + " " + var_name + " + "
    str_maximize += str(max_sz - sz_i) + " " + var_name + " + "
    str_maximize += str(wh_i) + " " + var_name + " + "
    str_maximize += str(max_po - po_ij) + " " + var_name + " + "
    str_maximize += str(pt_ij) + " " + var_name

    if row < M - 1:
        str_maximize += " + "

    # 制約式セッション
    str_c1 += var_name
    if row < M - 1:
        str_c1 += " + "

    str_c2 += str(cp_i) + " " + var_name
    if row < M - 1:
        str_c2 += " + "

    str_c3 += str(pr_ij) + " " + var_name
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
str_c2 += " = 8000"
str_c3 += " <= 50000"

str_subject_to += str_c1 + "\n" + str_c2 + "\n" + str_c3

print(str_maximize)
print(str_subject_to)
print(str_bounds)
print(str_general)
print("end")

f = open('buy_hdd.lp', 'w')
f.write(str_maximize + "\n" + str_subject_to + "\n" + str_bounds + "\n" + str_general + "\nend")
f.close()
