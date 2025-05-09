import microscopicXS
import periodictable 
from scipy.constants import Avogadro
import numpy as np
import sys
import fission

def getmacroXS(element_letter, A, microXS):
    iso = getattr(periodictable, element_letter)[A]
    density = iso.density
    mass = iso.mass
    atom_density = density * Avogadro / mass
    macroscopicXS = atom_density * microXS
    return macroscopicXS

def properties(material):
    if material == 0:   # void  
        content = {'Z' : 0,
                   'N' : 0, 
                   'A' : 0,
                   'molar_mass' : 0,
                   'density' : 0}

    elif material == 1: # Ca40
        calcium40 = periodictable.Ca[40]
        content = {'Z' : 20,
                   'N' : 20, 
                   'A' : 40,
                   'molar_mass' : calcium40.mass,
                   'density' : calcium40.density}
         
    elif material == 2: # Pu239
        plutonium239 = periodictable.Pu[239]
        content = {'Z' : 94,
                   'N' : 145, 
                   'A' : 239,
                   'molar_mass' : plutonium239.mass,
                   'density' : plutonium239.density}

    return content

def microXS(material, energy):
    if material == 0:   # void
        content = {'sigma_tot' : 0,
                   'sigma_s' : 0,
                   'sigma_a' : 0,
                   'sigma_f' : 0}

    elif material == 1: # Ca40
        content = {'sigma_tot' : microscopicXS.getMicro('../Diffusion-Solver/xsdata/Ca40/Ca40_totalXS.json', energy),
                   'sigma_s' : microscopicXS.getMicro('../Diffusion-Solver/xsdata/Ca40/Ca40_scatterXS.json', energy),
                   'sigma_a' : microscopicXS.getMicro('../Diffusion-Solver/xsdata/Ca40/Ca40_absorptionXS.json', energy),
                   'sigma_Ca40(n,a)Ar37': microscopicXS.getMicro('../Diffusion-Solver/xsdata/Ca40/Ca40(n,a)XS.json', energy),}
         
    elif material == 2: # Pu239
        content = {'sigma_tot' : microscopicXS.getMicro('../Diffusion-Solver/xsdata/Pu239/Pu239_totalXS.json', energy),
                   'sigma_s' : microscopicXS.getMicro('../Diffusion-Solver/xsdata/Pu239/Pu239_scatterXS.json', energy),
                   'sigma_a' : microscopicXS.getMicro('../Diffusion-Solver/xsdata/Pu239/Pu239_absorptionXS.json', energy),
                   'sigma_f' : microscopicXS.getMicro('../Diffusion-Solver/xsdata/Pu239/Pu239_fissionXS.json', energy)}

    return content

def macroXS(material, energy):
    if material == 0:   # void
        content = {'Sigma_tot' : 0,
                   'Sigma_s' : 0,
                   'Sigma_a' : 0,
                   'Sigma_f' : 0}

    elif material == 1: # Ca40
        content = {'Sigma_tot' : getmacroXS('Ca', 40, microXS(1, energy)['sigma_tot']),
                   'Sigma_s' : getmacroXS('Ca', 40, microXS(1, energy)['sigma_s']),
                   'Sigma_a' : getmacroXS('Ca', 40, microXS(1, energy)['sigma_a']),
                   'Sigma_Ca40(n,a)Ar37' : getmacroXS('Ca', 40, microXS(1, energy)['sigma_Ca40(n,a)Ar37'])}
         
    elif material == 2: # Pu239
        content = {'Sigma_tot' : getmacroXS('Pu', 239, microXS(2, energy)['sigma_tot']),
                   'Sigma_s' : getmacroXS('Pu', 239, microXS(1, energy)['sigma_s']),
                   'Sigma_a' : getmacroXS('Pu', 239, microXS(1, energy)['sigma_a']),
                   'Sigma_f' : getmacroXS('Pu', 239, microXS(1, energy)['sigma_f'])}

    return content

def getReaction(rxn_name):
    if rxn_name == 'Sigma_Ca40(n,a)Ar37':
        content = {'Target' : 'Ca40',
                   'Projectile' : 'n',
                   'Product' : 'Ar37',
                   'Ejectile' : 'a'}
    else: 
        content = {}
    return content

def generate_fission_results(material, energy):
    if material == 2:
        selected_energy = fission.fission_spectra('../Diffusion-Solver/Fission/Pu239/Pu239_energy.csv' , 0, energy)
        nu_bar = fission.get_nu_bar('../Diffusion-Solver/Fission/Pu239/Pu239_nubar.csv', selected_energy)
        num_neutron = fission.num_neutron(nu_bar)

        data = [selected_energy, nu_bar, num_neutron]

    return data