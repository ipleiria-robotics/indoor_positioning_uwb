import numpy as np
import pandas as pd
from numpy import linalg as la
import matplotlib.pyplot as plt
import math as mth

df = pd.read_csv("LOS_CIR", delimiter=";", header=None)
df2 = pd.read_csv("NLOS_CIR", delimiter=";", header=None)
# index_arr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
index_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

los_anchor0_real = np.array(df.loc[:, index_arr[0]])
los_anchor0_img = np.array(df.loc[:, index_arr[1]])
los_anchor0_data = np.vstack((los_anchor0_real, los_anchor0_img))
los_anchor1_real = df.loc[:, index_arr[2]]
los_anchor1_img = df.loc[:, index_arr[3]]
los_anchor1_data = np.vstack((los_anchor1_real, los_anchor1_img))
los_anchor2_real = df.loc[:, index_arr[4]]
los_anchor2_img = df.loc[:, index_arr[5]]
los_anchor2_data = np.vstack((los_anchor2_real, los_anchor2_img))
los_anchor3_real = df.loc[:, index_arr[6]]
los_anchor3_img = df.loc[:, index_arr[7]]
los_anchor3_data = np.vstack((los_anchor3_real, los_anchor3_img))
los_anchor4_real = df.loc[:, index_arr[8]]
los_anchor4_img = df.loc[:, index_arr[9]]
los_anchor4_data = np.vstack((los_anchor4_real, los_anchor4_img))
los_anchor5_real = df.loc[:, index_arr[10]]
los_anchor5_img = df.loc[:, index_arr[11]]
los_anchor5_data = np.vstack((los_anchor5_real, los_anchor5_img))
los_anchor6_real = df.loc[:, index_arr[12]]
los_anchor6_img = df.loc[:, index_arr[13]]
los_anchor6_data = np.vstack((los_anchor6_real, los_anchor6_img))
los_anchor7_real = df.loc[:, index_arr[14]]
los_anchor7_img = df.loc[:, index_arr[15]]
los_anchor7_data = np.vstack((los_anchor7_real, los_anchor7_img))


nlos_anchor0_real = np.array(df2.loc[:, index_arr[0]])
nlos_anchor0_img = np.array(df2.loc[:, index_arr[1]])
nlos_anchor0_data = np.vstack((nlos_anchor0_real, nlos_anchor0_img))
nlos_anchor1_real = df2.loc[:, index_arr[2]]
nlos_anchor1_img = df2.loc[:, index_arr[3]]
nlos_anchor1_data = np.vstack((nlos_anchor1_real, nlos_anchor1_img))
nlos_anchor2_real = df2.loc[:, index_arr[4]]
nlos_anchor2_img = df2.loc[:, index_arr[5]]
nlos_anchor2_data = np.vstack((nlos_anchor2_real, nlos_anchor2_img))
nlos_anchor3_real = df2.loc[:, index_arr[6]]
nlos_anchor3_img = df2.loc[:, index_arr[7]]
nlos_anchor3_data = np.vstack((nlos_anchor3_real, nlos_anchor3_img))
nlos_anchor4_real = df2.loc[:, index_arr[8]]
nlos_anchor4_img = df2.loc[:, index_arr[9]]
nlos_anchor4_data = np.vstack((nlos_anchor4_real, nlos_anchor4_img))
nlos_anchor5_real = df2.loc[:, index_arr[10]]
nlos_anchor5_img = df2.loc[:, index_arr[11]]
nlos_anchor5_data = np.vstack((nlos_anchor5_real, nlos_anchor5_img))
nlos_anchor6_real = df2.loc[:, index_arr[12]]
nlos_anchor6_img = df2.loc[:, index_arr[13]]
nlos_anchor6_data = np.vstack((nlos_anchor6_real, nlos_anchor6_img))
nlos_anchor7_real = df2.loc[:, index_arr[14]]
nlos_anchor7_img = df2.loc[:, index_arr[15]]
nlos_anchor7_data = np.vstack((nlos_anchor7_real, nlos_anchor7_img))


start = 740
end = 800
lenth = len(df.loc[:, 0])
ele = np.arange(0, lenth)
los_anc0 = np.zeros(lenth)
los_anc1 = np.zeros(lenth)
los_anc2 = np.zeros(lenth)
los_anc3 = np.zeros(lenth)
los_anc4 = np.zeros(lenth)
los_anc5 = np.zeros(lenth)
los_anc6 = np.zeros(lenth)
los_anc7 = np.zeros(lenth)
nlos_anc0 = np.zeros(lenth)
nlos_anc1 = np.zeros(lenth)
nlos_anc2 = np.zeros(lenth)
nlos_anc3 = np.zeros(lenth)
nlos_anc4 = np.zeros(lenth)
nlos_anc5 = np.zeros(lenth)
nlos_anc6 = np.zeros(lenth)
nlos_anc7 = np.zeros(lenth)


for i in range(0, len(los_anchor0_real)):
    los_anc0[i] = la.norm(los_anchor0_data[:, i])
    los_anc1[i] = la.norm(los_anchor1_data[:, i])
    los_anc2[i] = la.norm(los_anchor2_data[:, i])
    los_anc3[i] = la.norm(los_anchor3_data[:, i])
    los_anc4[i] = la.norm(los_anchor4_data[:, i])
    los_anc5[i] = la.norm(los_anchor5_data[:, i])
    los_anc6[i] = la.norm(los_anchor6_data[:, i])
    los_anc7[i] = la.norm(los_anchor7_data[:, i])

    nlos_anc0[i] = la.norm(nlos_anchor0_data[:, i])
    nlos_anc1[i] = la.norm(nlos_anchor1_data[:, i])
    nlos_anc2[i] = la.norm(nlos_anchor2_data[:, i])
    nlos_anc3[i] = la.norm(nlos_anchor3_data[:, i])
    nlos_anc4[i] = la.norm(nlos_anchor4_data[:, i])
    nlos_anc5[i] = la.norm(nlos_anchor5_data[:, i])
    nlos_anc6[i] = la.norm(nlos_anchor6_data[:, i])
    nlos_anc7[i] = la.norm(nlos_anchor7_data[:, i])


# for i in range(0, len(los_anc0)):
#     print(f"{nlos_anc5[i]}")


# plotting data
fig, axis = plt.subplots(2, 4)

axis[0, 0].set_title(f'CIR Anc0')
axis[0, 0].plot(ele[start:end], los_anc0[start:end], 'r')
axis[0, 0].plot(ele[start:end], nlos_anc0[start:end], 'b')
axis[0, 0].set_xlabel("slots")
axis[0, 0].set_ylabel("Amp")
axis[0, 0].grid()

axis[0, 1].set_title(f'CIR Anc1')
axis[0, 1].plot(ele[start:end], los_anc1[start:end], 'r')
axis[0, 1].plot(ele[start:end], nlos_anc1[start:end], 'b')
axis[0, 1].set_xlabel("slots")
axis[0, 1].set_ylabel("Amp")
axis[0, 1].grid()

axis[0, 2].set_title(f'CIR Anc2')
axis[0, 2].plot(ele[start:end], los_anc2[start:end], 'r')
axis[0, 2].plot(ele[start:end], nlos_anc2[start:end], 'b')
axis[0, 2].set_xlabel("slots")
axis[0, 2].set_ylabel("Amp")
axis[0, 2].grid()

axis[0, 3].set_title(f'CIR Anc3')
axis[0, 3].plot(ele[start:end], los_anc3[start:end], 'r')
axis[0, 3].plot(ele[start:end], nlos_anc3[start:end], 'b')
axis[0, 3].set_xlabel("slots")
axis[0, 3].set_ylabel("Amp")
axis[0, 3].grid()

axis[1, 0].set_title(f'CIR Anc4')
axis[1, 0].plot(ele[start:end], los_anc4[start:end], 'r')
axis[1, 0].plot(ele[start:end], nlos_anc4[start:end], 'b')
axis[1, 0].set_xlabel("slots")
axis[1, 0].set_ylabel("Amp")
axis[1, 0].grid()

axis[1, 1].set_title(f'CIR Anc5')
axis[1, 1].plot(ele[start:end], los_anc5[start:end], 'r')
axis[1, 1].plot(ele[start:end], nlos_anc5[start:end], 'b')
axis[1, 1].set_xlabel("slots")
axis[1, 1].set_ylabel("Amp")
axis[1, 1].grid()

axis[1, 2].set_title(f'CIR Anc6')
axis[1, 2].plot(ele[start:end], los_anc6[start:end], 'r')
axis[1, 2].plot(ele[start:end], nlos_anc6[start:end], 'b')
axis[1, 2].set_xlabel("slots")
axis[1, 2].set_ylabel("Amp")
axis[1, 2].grid()

axis[1, 3].plot(ele[start:end], los_anc7[start:end], 'r')
axis[1, 3].plot(ele[start:end], nlos_anc7[start:end], 'b')
axis[1, 3].set_title(f'CIR Anc7')
axis[1, 3].set_xlabel("slots")
axis[1, 3].set_ylabel("Amp")
axis[1, 3].grid()

plt.show()
