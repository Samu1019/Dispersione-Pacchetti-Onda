import numpy as np
import sys
from parameters import a, b, c
def w(nu):
    """
    Pulsazione in funzione della frequenza
    """
    return 2*np.pi*nu
def k_v_onda(w,rel_disp,b,c):
    """
    Numero d'onda calcolato a seconda della relazione di dispersione
    """
    if (rel_disp == 1):
        return np.power(w, 2)/c
    elif (rel_disp == 2):
        return w/np.sqrt(c)
    elif (rel_disp == 3):
        return np.power(np.power(w,2)/c,1/3)
    elif (rel_disp == 4):
        rad = (np.power(w, 2) - b) / c
        return np.sqrt(rad.clip(min=0))
    else:
        print("ERRORE: relazione di dispersione non valida.")
        sys.exit(1)

class WavePacket:
    def __init__(self, N, nu_min, nu_max, distr_freq):
        self.N = N
        self.nu_min= nu_min
        self.nu_max= nu_max
        self.distr_freq= distr_freq
        self.nu = self._gen_nu()
        self.A = self._gen_A()
        self.k = self._calc_k()
    def _calc_k(self):
        """
        calcolo della costante di normalizzazione k in base alla distribuzione scelta
        """
        if self.distr_freq == 1:
            return 1/np.log(self.nu_max / self.nu_min)
        elif self.distr_freq == 2:
            return 1/(1/self.nu_min - 1/self.nu_max)
    def _gen_nu(self):
        y = np.random.random(self.N)
        """
        generazione frequenze attraverso il metodo dell'inversa della cumulativa
        y: numero random [0, 1]
        """
        if self.distr_freq == 1:
            return self.nu_min * (self.nu_max / self.nu_min)**y
        elif self.distr_freq == 2:
            term_min, term_max = 1/self.nu_min, 1/self.nu_max
            return 1/(term_min - y * (term_min - term_max))
        else:
            media = (self.nu_max + self.nu_min) / 2
            sigma = (self.nu_max - self.nu_min) / 20
            return np.abs(np.random.normal(loc=media, scale=sigma, size=self.N))
    def _gen_A(self):
        A_max=a/np.sqrt(self.nu)
        y = np.random.random(self.N)
        """
        generazione ampiezze attraverso il metodo dell'inversa della cumulativa
        y: numero random [0, 1]
        """
        return A_max* np.sqrt(y)
def evolve_wp(packet, x, t, rel_disp, b_cost,c_cost):
    """
    Evoluzione temporale del pacchetto d'onda
    packet: istanza della classe WavePacket
    t: array di tempi
    x: array della coordinata spaziale
    """
    omega=w(packet.nu)
    k_reldisp=k_v_onda(omega,rel_disp,b,c)
    x_ax = max(np.size(x), np.size(t))
    psi = np.zeros(x_ax)
    for i in range(packet.N):
        psi += packet.A[i] * np.cos(k_reldisp[i] * x - omega[i] * t)
    return psi 