def properties(material):
    if material == 0:
        Sigma_s = 0
        Sigma_a = 0
        Sigma_f = 0
        density = 0 
        content = [Sigma_s, Sigma_a, Sigma_f, density, material]
        # add more physical properties
    elif material == 1:
        Sigma_s = 0.5
        Sigma_a = 0.4
        Sigma_f = 0.1
        density = 0 
        content = [Sigma_s, Sigma_a, Sigma_f, density, material]
    return content