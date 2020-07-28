# Implementation of TimSort
from collections import deque
import contextlib
import numpy
import argparse
import csv
from time import process_time


parser = argparse.ArgumentParser(description="Ordinamento con l'algoritmo TimSort")
parser.add_argument("-i",type=str,help="file csv con array di input")
parser.add_argument("-o",type=str,help="file in cui viene salvato l'output")
parser.add_argument("-t",type=str,help="tipologia di input")
parser.add_argument("-r",type=int,help="numero di taglie da considerare (fino a 18)")
parser.add_argument("-e",type=int,help="modalità d'esecuzione")
parser.add_argument("-m",type=int,default=7,help="minGallop: numero iniziale di wins consecutive di una stessa Run prima di entrare nel Galloping mode (7 di default)")

args = parser.parse_args()

input = args.i
output = args.o
type = args.t
r = args.r
e = args.e
m = args.m

count = 0

@contextlib.contextmanager
def escapable():
    class Escape(RuntimeError): pass
    class Unblock(object):
        def escape(self):
            raise Escape()

    try:
        yield Unblock()
    except Escape:
        pass


minGallop = m  # inizializzato con il parametro da riga di comando, poi mergeLo e mergeHi possono aumentarlo e diminuirlo a seconda dei casi

# Minrun compreso tra 32 e 64 inclusi,
# in modo che n diviso minrun e uguale a (o leggermente meno di) una potenza di 2
def compute_minrun(n):
    minrun = n
    remaining_bits = n.bit_length() - 6

    if remaining_bits > 0:
        minrun = n >> remaining_bits
        mask = (1 << remaining_bits) - 1
        if (n & mask) > 0: minrun += 1
    return minrun


# reverse se ordine decrescente
def reverse(arr,i,j):
    while i<j:
        arr[i], arr[j] = arr[j], arr[i]
        i += 1
        j -= 1


# InsertionSort binario
def insertion_sort(arr,start,size):
   for i in range(1, size):
      temp = arr[start+i]
      pos = binary_search(arr, temp, start, start+i) + 1 # posizione in cui inserire l'elemento (tramite ricerca binaria)
      for k in range(start+i, pos, -1):
         arr[k] = arr[k - 1] # sposto a dx tutti gli elementi successivi a quello da inserire
      arr[pos] = temp
# ricerca binaria della posizione in cui inserire l'elemento nell'InsertionSort
def binary_search(arr, key, start, end):
   global count
   #key
   if end - start <= 1:
      if key < arr[start]:
         return start - 1
      else:
         return start
   mid = (start + end)//2
   if arr[mid] < key:
       count +=1
       return binary_search(arr, key, mid, end)
   elif arr[mid] > key:
      count += 1
      return binary_search(arr, key, start, mid)
   else:
      return mid

# verifica in che posizione inserire la key nel range tra base e base+len, cominciando la ricerca all'indice hint
# se nel range e presente un elemento uguale a key, ritorna l'indice dell'elemento a piu a sx uguale
def gallopLeft(key, arr, base, len, hint):
    global count
    lastOfs = 0
    ofs = 1
    if key > arr[base + hint]: #gallop right
        count += 1
        maxOfs = len - hint
        while ofs < maxOfs and key > arr[base + hint + ofs]:
            count += 1
            lastOfs = ofs
            ofs = (ofs * 2) + 1
            if ofs <= 0: ofs = maxOfs
        if ofs > maxOfs: ofs = maxOfs
        lastOfs += hint
        ofs += hint
    else: #gallop left
        count += 1
        maxOfs = hint + 1
        while ofs < maxOfs and key<=arr[base + hint - ofs]:
            count += 1
            lastOfs = ofs
            ofs = (ofs * 2) + 1
            if ofs <= 0: ofs = maxOfs
        if ofs > maxOfs: ofs = maxOfs
        tmp = lastOfs
        lastOfs = hint - ofs
        ofs = hint - tmp
    lastOfs += 1
    while lastOfs < ofs:
        m = lastOfs + numpy.right_shift((ofs - lastOfs),1)
        if key>arr[base + m]:
            lastOfs = m + 1
            count += 1
        else:
            ofs = m
            count += 1
    return ofs


# verifica in che posizione inserire la key nel range tra base e base+len, cominciando la ricerca all'indice hint
# se nel range e presente un elemento uguale a key, ritorna l'indice dopo l'elemento piu a dx uguale
def gallopRight(key, arr, base, len, hint):
    global count
    lastOfs = 0
    ofs = 1
    if key < arr[base+hint]: #gallop left
        count += 1
        maxOfs = hint + 1
        while ofs < maxOfs and key < arr[base+hint-ofs]:
            count += 1
            lastOfs = ofs
            ofs = (ofs * 2) + 1
            if ofs<=0:
                ofs = maxOfs
        if ofs > maxOfs: ofs = maxOfs
        tmp = lastOfs
        lastOfs = hint - ofs
        ofs = hint - tmp
    else: #gallop right
        count += 1
        maxOfs = len - hint
        while ofs < maxOfs and key >= arr[base + hint + ofs]:
            count += 1
            lastOfs = ofs
            ofs = (ofs * 2) + 1
            if ofs <= 0: ofs = maxOfs
        if ofs > maxOfs: ofs = maxOfs
        lastOfs += hint
        ofs += hint
    lastOfs += 1
    while lastOfs < ofs:
        m = lastOfs + numpy.right_shift((ofs - lastOfs),1)
        if key < arr[base + m]:
            ofs = m
            count += 1
        else:
            lastOfs = m + 1
            count += 1
    return ofs

# fusione di due runs adiacenti, quando l1<=l2
# avendo gia richiamato la Gallop, sicuramente arr[b1] > arr[b2]
def mergeLo(arr,b1,l1,b2,l2):
    global count
    global minGallop
    #la prima Run (piu breve) e copiata in un array temporaneo
    temp=[]
    temp[0:l1] = arr[b1:b1 + l1]
    cursor1 = 0 # indice in temp
    cursor2 = b2 # indice in Run2
    dest = b1 # indice in arr

    # posso spostare il primo elemento di Run2 in arr, perche arr[b1] > arr[b2]
    arr[dest] = arr[cursor2]
    dest += 1
    cursor2 += 1
    l2 -= 1
    if l2==0:
        arr[dest:dest+l1]=temp[cursor1:cursor1+l1]
        return
    if l1==1:
        arr[dest:dest+l2] = arr[cursor2:cursor2+l2]
        arr[dest + l2] = temp[cursor1]
        return
    with escapable() as a:
        while True:
            count1 = 0  # numero di vittorie consecutive di Run1
            count2 = 0  # numero di vittorie consecutive di Run2
            # merge classico fino a che non vince sempre una delle due Run
            while not (count1 | count2) >= minGallop:
                if arr[cursor2] < temp[cursor1]:
                    count += 1
                    arr[dest] = arr[cursor2]
                    dest += 1
                    cursor2 += 1
                    count2 += 1
                    count1 = 0
                    l2 -= 1
                    if l2==0: a.escape()
                else:
                    count += 1
                    arr[dest] = temp[cursor1]
                    dest += 1
                    cursor1 += 1
                    count1 +=1
                    count2 = 0
                    l1 -= 1
                    if l1 == 1: a.escape()

            # una Run sta vincendo, quindi provo il Galloping mode fino a che una delle Run smette di vincere sempre
            while not count1 < minGallop & count2 < minGallop:
                count1 = gallopRight(arr[cursor2], temp, cursor1, l1, 0)
                if count1 != 0:
                    arr[dest:dest + count1] = temp[cursor1:cursor1+count1]
                    dest += count1
                    cursor1 += count1
                    l1 -= count1
                    if l1 <= 1: a.escape()
                arr[dest] = arr[cursor2]
                dest += 1
                cursor2 += 1
                l2 -= 1
                if l2 == 0: a.escape()
                count2 = gallopLeft(temp[cursor1], arr, cursor2, l2,0)
                if count2 != 0:
                    arr[dest:dest + count2] = arr[cursor2:cursor2 + count2]
                    dest += count2
                    cursor2 += count2
                    l2 -= count2
                    if l2 == 0: a.escape()
                arr[dest] = temp[cursor1]
                dest += 1
                cursor1 += 1
                l1 -= 1
                if l1==1: a.escape()
                minGallop -= 1 # Favorisco l'entrata nel Galloping mode successivamente
            if minGallop < 0:
                minGallop = 0
            minGallop += 2 # Penalizzazione (sara piu difficile entrare nel Galloping mode successivamente)
    if minGallop < 1:
        minGallop = 1
    if l1==1:
        arr[dest:dest+l2] = arr[cursor2:cursor2+l2]
        arr[dest + l2] = temp[cursor1]
    else:
        arr[dest:dest+l1]=temp[cursor1:cursor1+l1]


# fusione di due runs adiacenti, quando l1>=l2
# avendo gia richiamato la Gallop sicuramente arr[b1 + l1-1] e > di tutti gli elementi in Run2
def mergeHi(arr,b1,l1,b2,l2): #la seconda Run (piu breve) e copiata in un array temporaneo
    global count
    global minGallop
    temp = []
    temp[0:l2] = arr[b2:b2+l2]
    cursor1 = b1 + l1 - 1 #indice di a
    cursor2 = l2 - 1 #indice di temp
    dest = b2 + l2 - 1 #indice di arr

    # posso spostare l'ultimo elemento di Run1 in arr, perche arr[b1 + l1-1] e > di tutti gli elementi in Run2
    arr[dest] = arr[cursor1]
    dest -= 1
    cursor1 -= 1
    l1 -= 1
    if l1 == 0:
        arr[dest - (l2 - 1):dest - (l2 - 1)+ l2] = temp[0:l2]
        return
    if l2 == 1:
        dest -= l1
        cursor1 -= l1
        arr[dest+1:dest+1+l1]=arr[cursor1 + 1:cursor1 + 1+l1]
        arr[dest] = temp[cursor2]
        return
    with escapable() as a:
        while True:
            count1 = 0  # numero di vittorie consecutive di Run1
            count2 = 0  # numero di vittorie consecutive di Run2
            # merge classico fino a che non vince sempre una delle due Run
            while not (count1 | count2) >= minGallop:
                if temp[cursor2] < arr[cursor1]:
                    count += 1
                    arr[dest] = arr[cursor1]
                    dest -= 1
                    cursor1 -= 1
                    count1 += 1
                    count2 = 0
                    l1 -= 1
                    if l1==0: a.escape()
                else:
                    count += 1
                    arr[dest] = temp[cursor2]
                    dest -= 1
                    cursor2 -= 1
                    count2 +=1
                    count1 = 0
                    l2 -= 1
                    if l2 == 1: a.escape()
            # una Run sta vincendo, quindi provo il Galloping mode fino a che una delle Run smette di vincere sempre
            while not count1 < minGallop & count2 < minGallop:
                count1 = l1 - gallopRight(temp[cursor2], arr, b1, l1, l1 - 1)
                if count1 != 0:
                    dest -= count1
                    cursor1 -= count1
                    l1 -= count1
                    arr[dest + 1:dest + 1+count1] = arr[cursor1 + 1:cursor1 + 1+count1]
                    if l1 == 0: a.escape()
                arr[dest] = temp[cursor2]
                dest -= 1
                cursor2 -= 1
                l2 -= 1
                if l2 == 1: a.escape()
                count2 = l2 - gallopLeft(arr[cursor1], temp, 0, l2, l2 - 1)
                if count2 != 0:
                    dest -= count2
                    cursor2 -= count2
                    l2 -= count2
                    arr[dest + 1:dest + 1 + count2] = temp[cursor2 + 1:cursor2 + 1 + count2]
                    if l2 <= 1: a.escape()
                arr[dest] = arr[cursor1]
                dest -= 1
                cursor1 -= 1
                l1 -= 1
                if l1==0: a.escape()
                minGallop -= 1 # Favorisco l'entrata nel Galloping mode successivamente
            if minGallop < 0:
                minGallop = 0
            minGallop += 2 # Penalizzazione (sara piu difficile entrare nel Galloping mode
    if minGallop < 1:
        minGallop = 1
    if l2==1:
        dest -= l1
        cursor1 -= l1
        arr[dest + 1:dest + 1+l1] = arr[cursor1 + 1:cursor1 + 1+l1]
        arr[dest] = temp[cursor2]
    else:
        arr[dest - (l2 - 1):dest - (l2 - 1)+l2]=temp[0:l2]


def mergeAt(n, stack, arr):
    # lunghezze delle 2 porzioni da fondere
    l1 = stack[n][1]
    l2 = stack[n+1][1]
    # base address delle 2 porzioni da fondere
    b1 = stack[n][0]
    b2 = stack[n+1][0]

    # aggiornamento dello stack
    if n == len(stack) - 2:  # sono state fuse le ultime due
        stack.pop()
        stack.pop()
        stack.append((min(b1, b2), l1 + l2))
    else:  # sono state fuse la penultima e terzultima
        t = stack.pop()
        stack.pop()
        stack.pop()
        stack.append((min(b1, b2), l1 + l2))
        stack.append(t)

    # trova dove va inserito il primo elemento di Run2 all'interno di Run1
    # quelli prima di tale posizione in Run1 possono essere ignorati (gia al loro posto)
    k = gallopRight(arr[b2], arr, b1, l1, 0)
    b1 += k # quelli prima di k sono ignorati
    l1 -= k
    if l1 == 0: return

    # trova dove va inserito l'ultimo elemento di Run1 all'interno di Run2
    # quelli dopo di tale posizione in Run2 possono essere ignorati (gia al loro posto)
    l2 = gallopLeft(arr[b1 + l1 - 1], arr, b2, l2, l2 - 1) # per ignorare gli ultimi elementi di Run2 basta dimunuire l2
    if l2 == 0: return

    # merge delle porzioni rimanenti, usando mergeLo o mergeHi a seconda se l1<=l2 o l1>=l2
    if l1<=l2:
        mergeLo(arr,b1, l1, b2, l2)
    else: mergeHi(arr,b1, l1, b2, l2)



# richiamata ogni volta che una nuova Run e aggiunta allo stack
# fa in modo che le due proprieta sulle 3 Run in alto siano sempre rispettate, ovvero
# 1. |Z| > |Y| + |X|
# 2. |Y| > |X|
def mergeCollapse(stack,arr):
    while len(stack)>1:
        n = len(stack)-2
        if n>0 and stack[n-1][1] <= stack[n][1]+stack[n+1][1]:
            if stack[n-1][1] < stack[n+1][1]: n-=1 # andro a fondere la penultima e la terzultima
            mergeAt(n, stack, arr)
        elif stack[n][1] <= stack[n+1][1]: mergeAt(n, stack, arr)
        else:
            break

# richiamata alla fine per fondere le ultime Runs ordinate rimanste nello stack
def mergeForceCollapse(stack,arr):
    while len(stack) > 1:
        n = len(stack) - 2
        if n > 0 and stack[n - 1][1] < stack[n + 1][1]:
            n -= 1
        mergeAt(n, stack, arr)

def TimSort(arr):
    global count
    stack = deque() # lo stack contiene coppie (base_addr, size) per ogni Run
    n = len(arr)
    minrun = compute_minrun(n)
    base_addr = 0
    i = 0
    while i<n-1:
        if arr[i]<=arr[i+1]: asc=True # ordine crescente
        else: asc=False # ordine decrescente
        if asc:
            while i<n-1 and arr[i] <= arr[i + 1]:
                count += 1
                i += 1
        else:
            while i<n-1 and arr[i] > arr[i + 1]:
                count += 1
                i += 1
        size = i - base_addr + 1 # numero di elementi in ordine crescente/decrescente consecutivi
        if not asc:
            reverse(arr,base_addr,i) # invertire il sottoarray
        if size < minrun: # insertionSort per arrivare a dimensione minrun
            insertion_sort(arr,base_addr,min(minrun,n-base_addr)) # se e l'ultima run la dimensione puo essere < della minrun
            stack.append((base_addr,min(minrun,n-base_addr)))
            i = base_addr+minrun
            base_addr = i
        else:
            stack.append((base_addr,size))
            i += 1
            base_addr = i
        mergeCollapse(stack,arr)
    if i==n-1:
        stack.append((i,1)) # ultima Run di un solo elemento
        mergeCollapse(stack,arr)
    mergeForceCollapse(stack,arr)

if e==0:
    data = []
    with open(input) as csvfile:
        rd = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        for row in rd:
            data = row
    TimSort(data)
    with open(output, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerow(data)
elif e==1:
    data = []
    with open(input) as csvfile:
        rd = csv.reader(csvfile, quoting=csv.QUOTE_NONE, delimiter=',')
        for row in rd:
            data = row
    TimSort(data)
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
                TimSort(data)
                o.append((n, count))
                minGallop = m
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
                    TimSort(copy)
                    time = process_time() - start
                    time = round(time, 10)
                    sum += time
                    minGallop = m
                average = round(sum / 3, 10)
                o.append((n, average))
        size = size * 2
    with open(output, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerows(o)

elif e==4:
    count = 0
    data = []
    o = [('n','C(n)5','C(n)100','C(n)1000','C(n)10000')]
    size = 262144
    minGallopValues = [5,100,1000,10000]
    for i in range(5):
        file = "./inputs/" + type + "/" + type + str(size) + ".csv"
        c=[]
        with open(file) as csvfile:
            rd = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
            for row in rd:
                data = row
                n = len(data)
                for j in minGallopValues:
                    minGallop = j
                    copy = data.copy()
                    TimSort(copy)
                    c.append(count)
                    count = 0
                o.append(((n,) + tuple(c)))
        size = size * 2
    with open(output, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerows(o)
elif e==5:
    count = 0
    data = []
    o = [('n','m5','m100','m1000','m10000')]
    size = 262144
    minGallopValues = [5,100,1000,10000]
    for i in range(5):
        file = "./inputs/" + type + "/" + type + str(size) + ".csv"
        m=[]
        with open(file) as csvfile:
            rd = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
            for row in rd:
                data = row
                n = len(data)
                for j in minGallopValues:
                    minGallop = j
                    copy = data.copy()
                    TimSort(copy)
                    m.append(minGallop)
                    count = 0
                o.append(((n,) + tuple(m)))
        size = size * 2
    with open(output, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerows(o)

else: print("modalità d'esecuzione non valida")







