import geometry
import numpy as np
import material
import random

def surr_elements(world, x, y, z):
    x_length, y_length, z_length = world.shape
    possible_neighbors = [
        # surrounding coordinates at z = 0
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x + 1, y + 1, z),
        (x + 1, y - 1, z),
        (x - 1, y - 1, z),
        (x - 1, y + 1, z),

        # surrounding coordinates at z = -1
        (x, y, z - 1),
        (x - 1, y, z - 1),
        (x + 1, y, z - 1),
        (x, y - 1, z - 1),
        (x, y + 1, z - 1),
        (x + 1, y + 1, z - 1),
        (x + 1, y - 1, z - 1),
        (x - 1, y - 1, z - 1),
        (x - 1, y + 1, z - 1),

        # surrounding coordinates at z = +1
        (x, y, z + 1),
        (x - 1, y, z + 1),
        (x + 1, y, z + 1),
        (x, y - 1, z + 1),
        (x, y + 1, z + 1),
        (x + 1, y + 1, z + 1),
        (x + 1, y - 1, z + 1),
        (x - 1, y - 1, z + 1),
        (x - 1, y + 1, z + 1),
    ]

    valid_neighbors = []
    for xi, yi, zi in possible_neighbors:
        if (0 <= xi < x_length) and (0 <= yi < y_length) and (0 <= zi < z_length):
            valid_neighbors.append((xi, yi, zi))

    return valid_neighbors


def simulate(world, samples, x_pos, y_pos, z_pos, num_iter):
    num_scat = []
    num_abs = []
    num_fis = []

    start_pos = world[x_pos, y_pos, z_pos]
    for i in range(samples):
        print(f"Sampling {i} particles")
        surr_ele = surr_elements(world, x_pos, y_pos, z_pos)  
        targ_ele = random.choice(surr_ele)         
        distance = np.linalg.norm(np.array(targ_ele) - np.array([x_pos, y_pos, z_pos]))
        
        ele_mat = world[targ_ele[0], targ_ele[1], targ_ele[2]]

        prob_interact = 1 - (material.properties(ele_mat)[0] + material.properties(ele_mat)[1]) * distance   
        # ^^ see material.py --> material.properties(0) and material.properties(1) is hardcoded as scatter and absorption XS respectfully ^^ #
        rng = np.random.uniform(0, 1)
        if rng <= prob_interact:
            total_xs = material.properties(ele_mat)[0] + material.properties(ele_mat)[1] + material.properties(ele_mat)[2]
            rng = np.random.uniform(0, total_xs)
            if rng <= material.properties(ele_mat)[0]:
                while rng < material.properties(ele_mat)[0]:
                    num_scat.append(1) # data collection

                    start_pos = np.array([targ_ele[0], targ_ele[1], targ_ele[2]])
                    targ_ele = random.choice(surr_elements(world, start_pos[0], start_pos[1], start_pos[2])) # refreshes targe_ele[] in previous line
                    rng = np.random.uniform(0, total_xs)
                    if rng > material.properties(ele_mat)[0]:
                        break
            elif rng <= material.properties(ele_mat)[0] + material.properties(ele_mat)[1]:
                num_abs.append(1)
                pass
            elif rng <= total_xs:
                num_fis.append(1)
                iter = 0
                while rng <= total_xs and iter < num_iter:
                    iter += 1
                    n_prod = random.choice([1, 2, 3, 4, 5])
                    for i in range(n_prod):
                        n_pos = random.choice(surr_elements(world, targ_ele[0], targ_ele[1], targ_ele[2]))
                        simulate(world, 1, n_pos[0], n_pos[1], n_pos[2], num_iter)
    
    num_scat_tot = np.sum(num_scat)
    num_abs_tot = np.sum(num_abs)
    num_fis_tot = np.sum(num_fis)
    
    print(f"Total # of scatters: {num_scat_tot} \
            Total # of absorption: {num_abs_tot} \
            Total # of fission: {num_fis_tot}")
    return 0
