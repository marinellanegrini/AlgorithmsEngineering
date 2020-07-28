import argparse
import matplotlib.pyplot as plt
import pandas as pd
import math

parser = argparse.ArgumentParser(description="Plot multipli dei risultati")
parser.add_argument("-o",type=str,help="file png in cui salvare il plot")
parser.add_argument("-m",type=int,help="MergeSort")
parser.add_argument("-qk",type=int,help="QuickSort")
parser.add_argument("-t",type=int,help="TimSort")
parser.add_argument("-oa",type=int,help="ord_asc")
parser.add_argument("-od",type=int,help="ord_desc")
parser.add_argument("-p",type=int,help="perc")
parser.add_argument("-rn",type=int,help="rand_normal")
parser.add_argument("-ru",type=int,help="rand_uniform")
parser.add_argument("-w",type=int,help="window")
parser.add_argument("-nl",type=int,help="n*logn")
parser.add_argument("-q",type=int,help="n*n")
parser.add_argument("-l",type=int,help="n")
parser.add_argument("-e",type=int,help="Tipo di plot (C(n) o T(n))")

args = parser.parse_args()
output = args.o
m = args.m
qk = args.qk
t = args.t
oa = args.oa
od = args.od
p = args.p
rn = args.rn
ru = args.ru
w = args.w
nl = args.nl
q = args.q
l = args.l
e = args.e

type = []
if oa==1 : type.append('ord_asc')
if od==1: type.append('ord_desc')
if p==1: type.append('perc')
if rn==1: type.append('rand_normal')
if ru==1: type.append('rand_uniform')
if w==1: type.append('window')

if e==0:
    if m == 1:
        for i in type:
            obs = pd.read_csv('./instr_count/Mergesort_' + i + '.csv')
            n = obs['n']
            Cn = obs['C(n)']
            plt.plot(n, Cn, label='Mergesort ' + i)
    if qk == 1:
        for i in type:
            obs = pd.read_csv('./instr_count/Quicksort_' + i + '.csv')
            n = obs['n']
            Cn = obs['C(n)']
            plt.plot(n, Cn, label='Quicksort ' + i)
    if t == 1:
        for i in type:
            obs = pd.read_csv('./instr_count/Timsort_' + i + '.csv')
            n = obs['n']
            Cn = obs['C(n)']
            plt.plot(n, Cn, label='Timsort ' + i)
    plt.ylabel('C(n)')
    size = 128
    x = []
    for i in range(18):
        x.append(size)
        size = size * 2
    if nl == 1:
        nlogn = []
        for i in range(len(x)):
            nlogn.append(x[i] * math.log(x[i], 2))
        plt.plot(x, nlogn, 'ro', label='n*log(n)')
    if q == 1:
        nn = []
        for i in range(len(x)):
            nn.append(x[i] * x[i])
        plt.plot(x, nn, 'bo', label='n*n')
    if l == 1:
        plt.plot(x, x, 'go', label='n')

elif e==1:
    if m == 1:
        for i in type:
            obs = pd.read_csv('./time_proc/Mergesort_' + i + '.csv')
            n = obs['n']
            Tn = obs['T(n)']
            plt.plot(n, Tn, label='Mergesort ' + i)
    if qk == 1:
        for i in type:
            obs = pd.read_csv('./time_proc/Quicksort_' + i + '.csv')
            n = obs['n']
            Tn = obs['T(n)']
            plt.plot(n, Tn, label='Quicksort ' + i)
    if t == 1:
        for i in type:
            obs = pd.read_csv('./time_proc/Timsort_' + i + '.csv')
            n = obs['n']
            Tn = obs['T(n)']
            plt.plot(n, Tn, label='Timsort ' + i)
    plt.ylabel('T(n)')
else:
    print("Modalità d'esecuzione non valida")

plt.xlabel('n')
plt.legend()
plt.savefig(output)