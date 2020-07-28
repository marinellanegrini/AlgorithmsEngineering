import argparse
import matplotlib.pyplot as plt
import pandas as pd
import math

parser = argparse.ArgumentParser(description="Plot dei risultati")
parser.add_argument("-f",type=str,help="file csv con i dati da plottare")
parser.add_argument("-o",type=str,help="file png in cui salvare il plot")
parser.add_argument("-nl",type=int,help="n*logn")
parser.add_argument("-q",type=int,help="n*n")
parser.add_argument("-l",type=int,help="n")
parser.add_argument("-e",type=int,help="Tipo di plot (C(n) o T(n))")


args = parser.parse_args()
input = args.f
output = args.o
nl = args.nl
q = args.q
l = args.l
e = args.e

obs = pd.read_csv(input)
n = obs['n']
if e==0:
    Cn = obs['C(n)']
    plt.plot(n, Cn, 'ro', label='C(n)')  # andamento ottenuto
    plt.ylabel('C(n)')
elif e==1:
    Tn = obs['T(n)']
    plt.plot(n, Tn, 'ro', label='T(n)')  # andamento ottenuto
    plt.ylabel('T(n)')
else: print("Modalità d'esecuzione non valida")
plt.xlabel('n')
if nl==1:
    nlogn = []
    for i in range(len(n)):
        nlogn.append(n[i] * math.log(n[i], 2))
    plt.plot(n, nlogn, label='n*log(n)')
if q==1:
    nn = []
    for i in range(len(n)):
        nn.append(n[i] * n[i])
    plt.plot(n, nn, label='n*n')
if l==1:
    plt.plot(n, n, label='n')

plt.legend()
plt.savefig(output)