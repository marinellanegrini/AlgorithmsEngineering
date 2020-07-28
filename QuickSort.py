# Implementation of QuickSort
from time import process_time
import sys
sys.setrecursionlimit(250000)
import csv
import argparse

parser = argparse.ArgumentParser(description="Ordinamento con l'algoritmo QuickSort")
parser.add_argument("-i",type=str,help="file csv con array di input")
parser.add_argument("-o",type=str,help="file in cui viene salvato l'output")
parser.add_argument("-t",type=str,help="tipologia di input")
parser.add_argument("-r",type=int,help="numero di taglie da considerare (fino a 18)")
parser.add_argument("-e",type=int,help="modalità d'esecuzione")

args = parser.parse_args()
input = args.i
output = args.o
type = args.t
e = args.e
r = args.r
count = 0

def Partition(arr,start,end):
    global count
    #scelgo come pivot il primo elemento
    pivot = arr[start]
    i = start+1
    j = end
    while True:
        while i<=j and arr[i]<=pivot:
            count += 1
            i += 1
        while i<=j and arr[j]>=pivot:
            count += 1
            j -= 1
        if i<=j:
            # siamo usciti dai cicli perche due elementi sono nella porzione sbagliata e vanno scambiati
            arr[i], arr[j] = arr[j], arr[i]
        else:
            # siamo usciti perche gli indici si sono incontrati
            break
    # scambio il pivot con l'indice al quale mi sono fermata
    arr[start], arr[j] = arr[j], arr[start]
    return j

def QuickSort (arr,i,f):
    global count
    if i<f:
        m = Partition(arr,i,f)
        QuickSort(arr,i,m-1)
        QuickSort(arr,m+1,f)

if e==0:
    data = []
    with open(input) as csvfile:
        rd = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        for row in rd:
            data = row
    QuickSort(data, 0, len(data) - 1)
    with open(output, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerow(data)
elif e==1:
    data = []
    with open(input) as csvfile:
        rd = csv.reader(csvfile, quoting=csv.QUOTE_NONE, delimiter=',')
        for row in rd:
            data = row
    QuickSort(data, 0, len(data) - 1)
    with open(output, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerow(data)
elif e==2:
    count = 0
    data = []
    o = [('n', 'C(n)')]
    size = 128
    for i in range(r):
        file = "./inputs/" + type + "/"+type + str(size) + ".csv"
        with open(file) as csvfile:
            if type == 'str':
                rd = csv.reader(csvfile, quoting=csv.QUOTE_NONE, delimiter=',')
            else:
                rd = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
            for row in rd:
                data = row
                n = len(data)
                QuickSort(data, 0, n - 1)
                o.append((n, count))
                count = 0
        size = size * 2
    with open(output, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerows(o)

elif e==3:
    data = []
    o = [('n', 'T(n)')]
    size = 128
    for i in range(r):
        file = "./inputs/" + type + "/" + type + str(size) + ".csv"
        with open(file) as csvfile:
            if type == 'str':
                rd = csv.reader(csvfile, quoting=csv.QUOTE_NONE, delimiter=',')
            else:
                rd = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
            for row in rd:
                data = row
                n = len(data)
                sum = 0
                for j in range(3):
                    copy = data.copy()
                    start = process_time()
                    QuickSort(copy, 0, n - 1)
                    time = process_time() - start
                    time = round(time, 10)
                    sum += time
                average = round(sum / 3, 10)
                o.append((n, average))
        size = size * 2
    with open(output, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerows(o)

else: print("modalità d'esecuzione non valida")



