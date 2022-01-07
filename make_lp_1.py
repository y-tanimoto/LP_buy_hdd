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

for row in range(M):
    i = data.iat[row, 0]
    j = data.iat[row, 13]

    # 変数名
    var_name = "x(" + str(i) + "," + str(j) + ")"

    # 各データの取得
    ev_i = data.iat[row, 3]
    cp_i = data.iat[row, 5]
    sz_i = data.iat[row, 6] * data.iat[row, 7] * data.iat[row, 8]
    wh_i = data.iat[row, 9]
    ts_i = data.iat[row, 10]
    co_i = data.iat[row, 11]
    pw_i = data.iat[row, 12]
    pr_ij = data.iat[row, 15]
    po_ij = data.iat[row, 16]
    pt_ij = data.iat[row, 17]
    cl_ij = data.iat[row, 18]
    se_ij = data.iat[row, 20]

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
    if np.isnan(co_i):
        co_i = 0
    if np.isnan(pw_i):
        pw_i = 0
    if np.isnan(pr_ij):
        pr_ij = 0
    if np.isnan(po_ij):
        po_ij = 0
    if np.isnan(pt_ij):
        pt_ij = 0
    if np.isnan(cl_ij):
        cl_ij = 0
    if np.isnan(se_ij):
        se_ij = 0

    # 目的関数セッション
    str_maximize += str(ev_i) + " " + var_name
    str_maximize += " + " + str(ts_i) + " " + var_name
    str_maximize += " - " + str(sz_i) + " " + var_name
    str_maximize += " - " + str(wh_i) + " " + var_name
    str_maximize += " - " + str(pw_i) + " " + var_name
    str_maximize += " + " + str(co_i) + " " + var_name
    str_maximize += " - " + str(pr_ij) + " " + var_name
    str_maximize += " - " + str(po_ij) + " " + var_name
    str_maximize += " + " + str(pt_ij) + " " + var_name
    str_maximize += " + " + str(cl_ij) + " " + var_name
    str_maximize += " + " + str(se_ij) + " " + var_name

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
