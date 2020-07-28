# Implementation of MergeSort
import csv
import argparse
from time import process_time

parser = argparse.ArgumentParser(description="Ordinamento con l'algoritmo MergeSort")
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


# Procedura Merge
# (dati due sotto-array ordinati di arr ordina gli elementi in arr in modo da avere un'unica sequanza ordinata)
def Merge(arr,l,m,r):
    global count
    l1 = m-l+1
    l2 = r-m

    # array temporanei con gli elementi dei sotto-array
    L=[]
    R=[]
    L[0:l1] = arr[l:m+1]
    R[0:l2] = arr[m+1:r+1]

    i = 0 # indice di L
    j = 0 # indice di R
    k = l # indice di arr


    # estrae ripetutamente il minimo tra L e R e lo mette in arr
    while i < l1 and j < l2:
        if L[i] <= R[j]:
            count += 1
            arr[k] = L[i]
            i += 1
        else:
            count += 1
            arr[k] = R[j]
            j += 1
        k += 1

    # copia gli elementi rimanenti in L o R
    # ci sono ancora elementi in L
    while i < l1:
        arr[k] = L[i]
        i += 1
        k += 1
    # ci sono ancora elementi in R
    while j < l2:
        arr[k] = R[j]
        j += 1
        k += 1


def MergeSort(arr,l,r):
    global count
    if l<r:
        m = (l+r)//2 # prende la parte intera

        # chiamate ricorsive su entrambe le meta
        MergeSort(arr,l,m)
        MergeSort(arr,m+1,r)
        Merge(arr,l,m,r)



if e==0:
    data = []
    with open(input) as csvfile:
        rd = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        for row in rd:
            data = row
    MergeSort(data, 0, len(data) - 1)
    with open(output, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerow(data)
elif e==1:
    data = []
    with open(input) as csvfile:
        rd = csv.reader(csvfile, quoting=csv.QUOTE_NONE, delimiter=',')
        for row in rd:
            data = row
    MergeSort(data, 0, len(data) - 1)
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
            if type=='str': rd = csv.reader(csvfile, quoting=csv.QUOTE_NONE, delimiter=',')
            else: rd = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
            for row in rd:
                data = row
                n = len(data)
                MergeSort(data, 0, n - 1)
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
            if type=='str': rd = csv.reader(csvfile, quoting=csv.QUOTE_NONE, delimiter=',')
            else: rd = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
            for row in rd:
                data = row
                n = len(data)
                sum = 0
                for j in range(3):
                    copy = data.copy()
                    start = process_time()
                    MergeSort(copy, 0, n - 1)
                    time = process_time() - start
                    time = round(time, 10)
                    sum += time
                average = round(sum/3, 10)
                o.append((n, average))
        size = size * 2
    with open(output, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerows(o)

else: print("modalità d'esecuzione non valida")


