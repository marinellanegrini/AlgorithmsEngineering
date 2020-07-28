
# TimSort_algorithm

Implementazione degli algoritmi Mergesort, Quicksort e Timsort e studio sperimentale sul loro comportamento per diversi dati di input.

## Linguaggio utilizzato
Python 3.6

## Librerie utilizzate

- NumPy
- matplotlib
- pandas

## Generazione degli inputs

Tutti gli inputs utilizzati per lo studio sono stati salvati nella cartella "inputs" ed è possibile generarli tramite lo script "input_gen.py" situato nella stessa cartella.


## Esecuzione degli algoritmi

Per l'esecuzione dei tre algoritmi sono disponibili le seguenti opzioni:

- ```-i``` path del file csv contenente l'array di input da ordinare (nel formato di quelli contenuti nella cartella "inputs")
- ```-o``` path del file di output
- ```-t``` tipo di dato da ordinare {"int", "ord_asc", "ord_desc", "perc", "rand_normal", "rand_uniform", "str", "window"}
- ```-r``` numero di taglie di input da considerare (fino a 18)
- ```-m``` minGallop (solo per il Timsort, 7 di default)
- ```-e``` modalità d'esecuzione {0: esecuzione con input numerici, 1: esecuzione con stringhe, 2: test sul numero di operazioni dominanti, 3: test sul tempo di CPU, 4(SOLO PER TIMSORT): test su minGallop (numero di istruzioni), 5(SOLO PER TIMSORT): test su minGallop (minGallop dopo esecuzione)}

####Esempi

- ``` python3 ./MergeSort.py -i "./inputs/int/int256.csv" -o "output.csv" -e 0 ``` : esegue l'algoritmo Mergesort sull'array di numeri specificato e salva l'array ordinato nel file "output.csv" (le esecuzioni del Quicksort e Timsort sono analoghe)
- ``` python3 ./MergeSort.py -i "./inputs/str/str256.csv" -o "output.csv" -e 1 ``` : esegue l'algoritmo Mergesort sull'array di stringhe specificato e salva l'array ordinato nel file "output.csv" (le esecuzioni del Quicksort e Timsort sono analoghe)
- ``` python3 ./MergeSort.py -t "perc" -o "output.csv" -r 18 -e 2  ``` : esegue il conteggio del numero di istruzioni dominanti per l'algoritmo Mergesort, per il tipo "perc", considerando 18 taglie di input e salva l'output nel file "output.csv" (le esecuzioni del Quicksort e Timsort sono analoghe)
- ``` python3 ./MergeSort.py -t "ord_asc" -o "output.csv" -r 10  -e 3``` : esegue il calcolo del tempo di CPU per l'algoritmo Mergesort, per il tipo "ord_asc", considerando 10 taglie di input e salva l'output nel file "output.csv" (le esecuzioni del Quicksort e Timsort sono analoghe)
- ``` python3 ./TimSort.py -t "ord_asc" -o "output.csv" -e 4``` :  esegue l'algoritmo Timsort per diversi valori di minGallop e salva il numero di istruzioni dominanti eseguite nel file "output.csv", per il tipo "ord_asc" (SOLO PER IL TIMSORT)
- ``` python3 ./TimSort.py -t "ord_asc" -o "output.csv" -e 5``` : esegue l'algoritmo Timsort per diversi valori di minGallop e salva il valore di minGallop dopo l'esecuzione nel file "output.csv", per il tipo "ord_asc" (SOLO PER IL TIMSORT)


## Verifica della correttezza degli algoritmi
Eseguendo lo script "Verification.py" è possibile verificare la correttezza di un risultato calcolato.
E' necessario fornire 3 parametri posizionali:
- ```d``` path del file contenente l'array di partenza
- ```o``` path del file contenente l'array ordinato tramite uno degli algoritmi (è l'output dell'esecuzione degli stessi)
- ```t``` tipo di dato {0: input numerici, 1: stringhe}

####Esempio
- ```  python3 ./Verification.py "./inputs/window/window256.csv" "arrayOrdinato.csv" 0 ``` : verifica se l'array contenuto nel file "arrayOrdinato.csv" è la versione ordinata dell'array contenuto nel file "./inputs/window/window256.csv"
- ```  python3 ./Verification.py "./inputs/str/str256.csv" "arrayOrdinato.csv" 1 ```: verifica se l'array contenuto nel file "arrayOrdinato.csv" è la versione ordinata dell'array contenuto nel file "./inputs/str/str256.csv"


## Plot di grafici singoli
Eseguendo lo script "Plot.py" è possibile plottare (in funzione di n) il numero di operazioni elementari oppure il tempo d'esecuzione.
Sono disponibili le seguenti opzioni:
- ```-f``` path del file csv contenente i dati da plottare (nel formato dei file prodotti eseguendo gli algoritmi con le modalità ```-e``` 2 e ```-e``` 3)
- ```-o``` path del file png di output
- ```-nl``` plotta anche l'andamento n*log(n) 
- ```-q``` plotta anche l'andamento n^2
- ```-l``` plotta anche l'andamento n
- ```-e``` tipo di plot {0: numero di istruzioni C(n), 1: tempo di CPU T(n)}

####Esempi
- ```  python3 ./Plot.py -f "./instr_count/Timsort_int.csv" -o "img.png" -nl 1 -l 1 -e 0 ``` : esegue il plot dei dati contenuti nel file "./instr_count/Timsort_int.csv" (numero di istruzioni **C(n)**) e salva il plot nel file "img.png", plottando anche l'andamento n*log(n) e n
- ```  python3 ./Plot.py -f "./time_proc/Quicksort_rand_normal.csv" -o "img.png" -e 1 ``` : esegue il plot dei dati contenuti nel file "./time_proc/Quicksort_rand_normal.csv" (tempo di CPU **T(n)**) e salva il plot nel file "img.png"

## Plot di grafici multipli
Eseguendo lo script "MultiplePlot.py" è possibile plottare (in funzione di n) più andamenti nello stesso grafico.
In questo caso le opzioni permettono di specificare sia gli algoritmi di cui si vuole osservare il plot, sia i tipi di inputs.
N.B.: in questo caso lo script prende i dati da plottare dalle cartelle "instr_count" o "time_proc" (a seconda dei casi) e considera file salvati nel formato "nomeAlgortimo_tipo.csv"
Sono disponibili le seguenti opzioni:
- ```-o``` path del file png di output
- ```-m``` Mergesort
- ```-qk``` Quicksort
- ```-t``` Timsort
- ```-oa``` ord_asc
- ```-od``` ord_desc
- ```-p``` perc
- ```-rn``` rand_normal
- ```-ru``` rand_uniform
- ```-w``` window
- ```-nl``` plotta anche l'andamento n*log(n) 
- ```-q``` plotta anche l'andamento n^2
- ```-l``` plotta anche l'andamento n
- ```-e``` tipo di plot {0: numero di istruzioni C(n), 1: tempo di CPU T(n)}

####Esempi
- ``` python3 ./MultiplePlots.py -o "img.png" -m 1 -qk 1 -t 1 -oa 1 -e 0``` : esegue il plot del numero di instruzioni **C(n)** per Mergesort, Quicksort e Timsort per il tipo ord_asc, salvando il plot nel file "img.png"
- ``` python3 ./MultiplePlots.py -o "img.png" -m 1 -qk 1 -t 1 -w 1 -e 1```: esegue il plot del tempo di CPU **T(n)** per Mergesort, Quicksort e Timsort per il tipo window, salvando il plot nel file "img.png"
- ``` python3 ./MultiplePlots.py -o "img.png" -m 1 -oa 1 -od 1 -rn 1 -p 1 -ru 1 -w 1 -nl 1 -e 0```:  esegue il plot del numero di instruzioni **C(n)** per il Mergesort, per tutti i tipi e plottando anche l'andamento n*log(n), salvando il plot nel file "img.png"
- ``` python3 ./MultiplePlots.py -o "img.png" -t 1 -oa 1 -od 1 -rn 1 -p 1 -ru 1 -w 1 -e 1```:  esegue il plot del tempo di CPU **T(n)** per il Timsort, per tutti i tipi, salvando il plot nel file "img.png"

## Plot dei test sul minGallop
Eseguendo lo script "minGallopPlot.py" è possibile plottare (in funzione di minGallop) il numero di operazioni elementari per i vari valori di n.
Sono disponibili le seguenti opzioni:
- ```-f``` path del file csv contenente i dati da plottare (nel formato dei file prodotti eseguendo il Timsort con la modalità ```-e``` 4)
- ```-o``` path del file png di output

####Esempi
- ``` python3 ./minGallopPlot.py -f "./minGallop/count/ord_asc.csv" -o "img.png"``` : esegue il plot richiesto dei dati contenuti nel file  "./minGallop/count/ord_asc.csv" e salva il plot nel file "img.png"