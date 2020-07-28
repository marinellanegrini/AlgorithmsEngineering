import csv
import numpy as np
import random
import string



# generazione di interi random
size = 128
for i in range(18):
    a = np.random.random_integers(0,2000,size)
    file = "./int/int" + str(size)+".csv"
    with open(file, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerow(a)
    size = size * 2

# generezione di stringhe random (lunghezza random da 3 a 6)
size = 128
letters = string.ascii_lowercase
for i in range(18):
    a=[]
    for i in range(size):
        s = ''.join((random.choice(letters) for i in range(random.randint(3,6))))
        a.append(s)
    file = "./str/str" + str(size)+".csv"
    with open(file, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerow(a)
    size = size * 2



# generazione reali random con distribuzione uniforme nell'intervallo [-2000,2000)
size = 128
for i in range(18):
    a = np.random.uniform(-2000,2000,size)
    file = "./rand_uniform/rand_uniform" + str(size)+".csv"
    with open(file, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerow(a)
    size = size * 2

# generazione reali random con distribuzione normale standard
size = 128
for i in range(18):
    a = np.random.normal(0,1,size)
    file = "./rand_normal/rand_normal" + str(size)+".csv"
    with open(file, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerow(a)
    size = size * 2


# generazione reali ordinati in ordine crescente
size = 128
for i in range(18):
    a = np.random.uniform(-2000,2000,size)
    a.sort()
    file = "./ord_asc/ord_asc" + str(size)+".csv"
    with open(file, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerow(a)
    size = size * 2

# generazione reali ordinati in ordine decrescente
size = 128
for i in range(18):
    a = np.random.uniform(-2000, 2000, size)
    a.sort()
    a =np.flip(a)
    file = "./ord_desc/ord_desc" + str(size)+".csv"
    with open(file, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerow(a)
    size = size * 2



# generazione reali ordinati in ordine crescente, con una sostituzione randomica dell'1% delle entries
size = 128
for i in range(18):
    a = np.random.uniform(-2000,2000,size)
    a.sort()
    perc = round(0.01 * size)  # numero di posizioni da sostituire
    pos = np.random.choice(size,perc) # posizioni da sostituire (scelte randomicamente)
    for i in pos:
        a[i] = np.random.uniform(-2000,2000) # sostituisco la posizione con un numero random
    file = "./perc/perc" + str(size)+".csv"
    with open(file, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerow(a)
    size = size * 2



# generazione reali random, con delle finestre pre-ordinate
# dimensione finestra: 1/10 della dimensione dell'array
# finestre ordinate: prima, quarta, settima, decima
size = 128
for i in range(18):
    a = np.random.uniform(-2000,2000,size) # random
    f = int(size/10) # dimensione finestra
    fin = np.random.uniform(-2000, 2000, f)
    fin.sort() # finestra preordinata
    for i in range(0,10,3):
        a[i * f:(i * f) + f] = fin[0:len(fin)] # inserimento delle finestre ordinate
    file = "./window/window" + str(size)+".csv"
    with open(file, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        wr.writerow(a)
    size = size * 2


