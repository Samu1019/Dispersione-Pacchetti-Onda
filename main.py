import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft
from parameters import b, c, v_min, v_max
from waves import WavePacket, evolve_wp


def parse_arguments():

    parser = argparse.ArgumentParser(description="Analisi dispersione pacchetti d'onda",
                                    usage="python3 main.py  --option")
    parser.add_argument("-g","--genpacket",   action="store_true",    help="Genera pacchetti d'onda, con un numero crescente di componenti, a partire da distribuzioni di probabilità date per le frequenze e le relative ampiezze")
    parser.add_argument("-n","--dist_tipo", type=int, default=1, help="Tipo di distribuzione di probabilità per le frequenze: 1 per k/nu, 2 per k/nu^2, 3 per una distribuzione gaussiana")
    parser.add_argument("-d","--rel_disp", type=int, default=1, help="Relazione di dispersione da utilizzare: 1 per w = sqrt(c*k), 2 per w = sqrt(c*(k^2)), 3 per w = sqrt(c*k^3), 4 per w = sqrt(b + c*k^2)")
    parser.add_argument("--t0", action="store_true", help="Mostra i pacchetti generati al tempo t=0")
    parser.add_argument("-e","--evolve", action="store_true", help="Mostra l'evoluzione dei pacchetti generati al variare del tempo")
    parser.add_argument("-f","--fourier", action="store_true", help="Mostra lo spettro di potenza di Fourier dei pacchetti generati")
    return  parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    labels_dist = {1: r"$\frac{k}{\nu}$", 2: r"$\frac{k}{\nu^2}$", 3: "gaussiana"}
    labels_rel = {1: r"${\omega} = \sqrt{ck}$", 2: r"${\omega} = \sqrt{ck^2}$", 3: r"${\omega} = \sqrt{ck^3}$", 4: r"${\omega} = \sqrt{b + ck^2}$"}
    packets=[]
    distr_freq= args.dist_tipo
    rel_disp = args.rel_disp
    if (args.genpacket):         #Generazione di 4 pacchetti d'onda con frequenza tra 1Hz e 10Hz
        N_val=[10,500,1000,1500]
        for i, N in enumerate(N_val):
            packet=WavePacket(N, v_min, v_max, distr_freq)
            packets.append(packet)      
    if (args.evolve):             #Evoluzione dei vari pacchetti d'onda per 4 istanti di tempo nell'intervallo [0,200]s
        if (not packets):
            print("ERRORE: Non è stato generato alcun pacchetto d'onda con l'opzione --genpacket")
            sys.exit(1)
        t_istanti=np.linspace(0, 200, 4)
        x_ax = np.linspace(-20, 1000, 20000)
        for p in packets:
            fig, axs = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)
            fig.suptitle(fr"Pacchetto con N={p.N},Relazione di Dispersione {labels_rel.get(rel_disp,'')}, Distribuzione di frequenza {labels_dist.get(distr_freq, '')}", fontsize=12)
            for i, t in enumerate(t_istanti):
                riga = i // 2
                colonna = i % 2
                evo_packet = evolve_wp(p, x_ax, t, rel_disp, b, c)
                ax = axs[riga, colonna]
                ax.plot(x_ax, evo_packet, lw=0.6, color='darkblue')
                ax.set_title(f"Istante t = {t:.2f} s", fontsize=10)
                ax.grid(True, linestyle=':', alpha=0.6)
                if riga == 1:
                    ax.set_xlabel("Spazio[m]")
                if colonna == 0:
                    ax.set_ylabel("Ampiezza")
            plt.tight_layout()
            plt.show()  
            plt.close('all')
    if(args.t0):    #Plot dei pacchetti all'istante t=0
        if(not packets):
            print("ERRORE: Non è stato generato alcun pacchetto d'onda con l'opzione --genpacket")
            sys.exit(1)
        x_ax = np.linspace(-20, 1000, 20000)
        fig, axs =plt.subplots(2,2, figsize=(10,8), sharex=True, sharey=True)
        for i, p in enumerate(packets):
            phi_0=evolve_wp(p,x_ax,0,rel_disp,b,c)
            riga=i//2
            colonna=i%2
            ax=axs[riga,colonna]
            ax.plot(x_ax, phi_0, lw=0.6, color="darkblue")
            ax.set_title(f"Pacchetto con N={p.N}", fontsize=10)
            ax.grid(True, linestyle=":", lw= 0.6,alpha=0.6)
            if riga == 1:
                ax.set_xlabel("Spazio[m]")
            if colonna == 0:
                ax.set_ylabel("Ampiezza")
        plt.tight_layout()
        plt.show()
        plt.close('all')

    if(args.fourier):             #Analisi dello spettro di fourier per i pacchetti generati, in x=0
        if(not packets):
            print("ERRORE: Non è stato generato alcun pacchetto d'onda con l'opzione --genpacket")
            sys.exit(1)
        t_fft=np.linspace(0, 100, 10000)
        dt = t_fft[1] - t_fft[0]
        for p in packets:
            psi_start=evolve_wp(p,0,t_fft,rel_disp,b,c)  #Pacchetto a x=0
            c_k = fft.rfft(psi_start)
            pow=np.power(np.abs(c_k),2)
            freq=fft.rfftfreq(len(psi_start), d=dt)
            plt.figure(figsize=(10, 6))
            mask = (freq > 0) & (freq <= v_max * 1.1) 
            f_plot = freq[mask]
            p_plot = pow[mask]
            plt.plot(freq[mask], pow[mask], color='crimson', lw=0.6, alpha=0.8)
            plt.title(fr"Analisi di Fourier del pacchetto con N={p.N}, Distribuzione di frequenza {labels_dist.get(distr_freq, '')}")
            plt.xlabel("Frequenza[Hz]")
            plt.ylabel("Potenza $|c_k|^2$")
            plt.grid(True, linestyle=':', alpha=0.6)
            plt.tight_layout()
            plt.show()
            plt.close('all')