"""Top-level package for montecarlo."""
import numpy as np
import math      
import copy as cp       


class BitString:
    """
    Simple class to implement a config of bits
    """
    def __init__(self, N):
        self.N = N
        self.config = np.zeros(N, dtype=int) 

    def __repr__(self):
        out = ""
        for i in self.config:
            out += str(i)
        return out

    def __eq__(self, other):        
        return all(self.config == other.config)
    
    def __len__(self):
        return len(self.config)

    def on(self):
        return np.sum(self.config == 1)

    def off(self):
        return np.sum(self.config == 0)

    def flip_site(self,i):
        N = len(self.config)
        self.config[N - 1 - i] = 1 - self.config[N - 1 - i]
    
    def integer(self):

        N = len(self.config)
        sum = 0
        for i in range(len(self.config)):
            sum += self.config[i] * (2 ** (N - 1 - i))
        return sum
 

    def set_config(self, s:list[int]):
        self.config = np.array(s, dtype = int)

    def set_integer_config(self, dec:int):
        bit = []
        for _ in range(self.N):
            bit.append(dec % 2)
            dec //= 2
        bit.reverse()
        self.config = np.array(bit, dtype=int)


class IsingHamiltonian:
    def __init__(self, G):
        self.G = G
        self.N = len(G.nodes)
        self.mus = [0.0] * len(G.nodes)
        self.config = BitString(len(G.nodes))
    
    def energy(self, config):
        su = 0.0

        for i, j in self.G.edges():
            w = self.G.edges[i, j].get('weight', 1.0)

            spini = 2 * config.config[i] - 1
            spinj = 2 * config.config[j] - 1

            su += w * spini * spinj 

        ma = 0.0
        for i in range(len(config)):
            spini = 2 * config.config[i] - 1
            ma += self.mus[i] * spini

        return su + ma
    
    def set_mu(self, mus):
        self.mus = mus

    def compute_average_values(self, T):
            E  = 0.0
            M  = 0.0
            Z  = 0.0
            EE = 0.0
            MM = 0.0

            k = 1

            # Write your function here!

            for i in range(2**self.config.N):
                self.config.set_integer_config(i)
                e = self.energy(self.config)
                Z = Z + np.exp(-1/(k * T)*e)

            
            for i in range(2**self.config.N):
                self.config.set_integer_config(i)
                e = self.energy(self.config)
                P = np.exp(-1/(k * T)*e)/Z
                E = E + P*e
                EE = EE + P*e*e

                m = self.config.on() - self.config.off()
                M = M + P*m
                MM = MM + P*m*m

            HC = (EE - E*E)/(T*T)
            MS = (MM - M*M)/(T)
            
            return E, M, HC, MS


class MonteCarlo:
    def __init__(self, hamiltonian):
        self.ham = hamiltonian
        self.config = cp.deepcopy(hamiltonian.config)

    def run(self, T, n_samples, n_burn):
        k = 1.0
        N = len(self.config)

        E = []
        M = []

        total_steps = n_burn + n_samples

        for step in range(total_steps):

            for i in range(N):

                currentE = self.ham.energy(self.config)

                new_config = cp.deepcopy(self.config)
                new_config.flip_site(i)

                check = self.ham.energy(new_config)

                dE = check - currentE

                if dE <= 0 or np.random.rand() < np.exp(-dE / (k * T)):
                    self.config = new_config 

            if step >= n_burn:
                e = self.ham.energy(self.config)
                m = self.config.on() - self.config.off()

                E.append(e)
                M.append(m)

        return np.array(E), np.array(M)