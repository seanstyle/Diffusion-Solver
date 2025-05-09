import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import linregress

def energy_spectra(file, e_min, e_max):

    def watt_spectrum(E, a, b, C):
        return C * np.sinh(np.sqrt(a * E)) * np.exp(-b * E)
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    E = df['x']
    P = df['y']
    popt, pcov = curve_fit(watt_spectrum, E, P, p0=[1.0, 1.0, 1.0])
    a_fit, b_fit, c_fit = popt

    energy_axis = np.linspace(e_min, e_max, int(1e6))
    prob_axis = watt_spectrum(energy_axis, a_fit, b_fit, c_fit)
    prob_axis = prob_axis / np.sum(prob_axis)
    selected_energy = np.random.choice(energy_axis, p=prob_axis)

    return selected_energy

def get_nu_bar(file, selected_energy): # gives you nu_bar(E) at a given energy
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    energy = np.array(df['x'])
    energy = energy * 1e6   # conversion from MeV to eV -- data file was in units of eV and our input is in MeV
    nu_bar = np.array(df['y'])

    ln_nu_bar = np.log(nu_bar)
    slope, intercept, r_value, p_value, std_err = linregress(energy, ln_nu_bar)
    b = slope
    a = np.exp(intercept)

    nu_bar = a + b*selected_energy
    return nu_bar

import numpy as np

def num_neutron(nu_bar):
    W = 1.08  # Standard deviation from MCNP standard
    nu_axis = np.linspace(0, 7, int(1e6))  # neutron multiplicity axis
    prob_axis = np.exp(-((nu_axis - nu_bar)**2) / (2 * W**2))
    prob_axis /= np.sum(prob_axis)
    selected_number_neutron = np.random.choice(nu_axis, p=prob_axis)
    selected_number_neutron = int(np.round(selected_number_neutron))
    
    return selected_number_neutron
