import csv
import argparse
import numpy as np

parser = argparse.ArgumentParser(description="Verifica della correttezza degli algoritmi")
parser.add_argument("d",type=str,help="file csv con array disordinato")
parser.add_argument("o",type=str,help="file csv con array ordinato")
parser.add_argument("t",type=int,help="tipo: 0 per i numeri, 1 per le stringhe")

args = parser.parse_args()
dis = args.d
ord = args.o
t = args.t
if t==0:
    dataDis = []
    with open(dis) as csvfile:
        rd = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        for row in rd:
            dataDis = row
    # ordino con la funzione sort di python
    dataDis.sort()
    dataOrd = []
    with open(ord) as csvfile:
        rd = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        for row in rd:
            dataOrd = row
    if np.array_equal(dataDis, dataOrd):
        print("Corretto")
    else:
        print("Non corretto")
elif t==1:
    dataDis = []
    with open(dis) as csvfile:
        rd = csv.reader(csvfile, quoting=csv.QUOTE_NONE, delimiter=',')
        for row in rd:
            dataDis = row
    # ordino con la funzione sort di python
    dataDis.sort()
    dataOrd = []
    with open(ord) as csvfile:
        rd = csv.reader(csvfile, quoting=csv.QUOTE_NONE, delimiter=',')
        for row in rd:
            dataOrd = row
    if np.array_equal(dataDis, dataOrd):
        print("Corretto")
    else:
        print("Non corretto")
else: print("Tipo non supportato")


