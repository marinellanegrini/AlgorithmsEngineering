import argparse
import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser(description="Plot dei risultati")
parser.add_argument("-f",type=str,help="file csv con i dati da plottare")
parser.add_argument("-o",type=str,help="file png in cui salvare il plot")

args = parser.parse_args()
input = args.f
output = args.o

obs = pd.read_csv(input)
m = [5,100,1000,10000]
n = obs['n']
C5 = obs['C(n)5']
C100 = obs['C(n)100']
C1000 = obs['C(n)1000']
C10000 = obs['C(n)10000']

for i in range(len(n)):
    y = [C5[i],C100[i],C1000[i],C10000[i]]
    plt.plot(m, y, label='n = '+str(n[i]))
plt.ylabel('C')
plt.xlabel('minGallop')
plt.legend()
plt.savefig(output)
