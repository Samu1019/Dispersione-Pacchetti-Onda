# Analisi della Dispersione di Pacchetti d'Onda

Il progetto si occupa della generazione, l'evoluzione temporale e l'analisi di Fourier di pacchetti d'onda composti da $N$ componenti cosinusoidali, permettendo di studiare come diverse distribuzioni di frequenza e relazioni di dispersione influenzino la propagazione dell'onda nel tempo e nello spazio.

## Composizione del Progetto
* **`main.py`**: Gestisce l'interfaccia da terminale e la visualizzazione dei grafici.
* **`waves.py`**: Contiene la struttura computazionale della generazione ed evoluzione dei pacchetti d'onda. Contiene la classe `WavePacket`, che genera i pacchetti d'onda, le le funzioni di evoluzione e altre funzioni di calcolo.
* **`parameters.py`**: Contiene le costanti di configurazione ($a, b, c$) che definiscono scala di ampiezze e relazioni di dispersione.

## Modalità d'uso
Per poter utilizzare il programma occorre scaricare tutti i file .py presenti nella repository e interfacciarsi solo con main.py.
Il programma deve essere lanciato da terminale utilizzando i flag desiderati. Di seguito i comandi utilizzabili dove -o è la forma short del comando mentre --option la versione estesa.
* -g --genpacket genera 4 pacchetti d'onda
* -n --dist_tipo permette di selezionare la distribuzione di probabilità dalla quale vengono generate frequenze, è possibile scegliere tra "1: $1/\nu$, 2: $1/\nu^2$, 3: Gaussiana" (default=1)
* -d --rel_disp permette di selezionare la relazione di dispersione del pacchetto. "1: $\omega = \sqrt{bk}$, 2: $\omega = \sqrt{ck}$, 3: $\omega = \sqrt{ck^3}$, 4 per $\omega = \sqrt{b + ck^2}$" (default=1)
* --t0 permette di visualizzare i pacchetti a t=0
* -e --evolve, permette di visualizzare i pacchetti in 4 istanti temporali equidistanti.
* -f --fourier permette di visualizzare lo spettro di potenza dei pacchetti a x=0.
Un esempio di corretto lancio del programma è il seguente:


```bash
python3 main.py --genpacket --dist_tipo 3 --evolve --rel_disp 1
```
Equivalentemente in forma abbreviata: 
```bash
python3 main.py -g -n 3 -e -d 1
```
## Requisiti
Per la corretta esecuzione del programma è necessario installare i moduli presenti nel file: "requirements.txt". Per farlo è sufficiente scaricare il file e utilizzare il seguente comando da terminale:
```bash
pip install -r requirements.txt
``` 
