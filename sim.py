import geometry
import numpy as np
import material
import random
import simfunction
import fission
from functools import lru_cache

@lru_cache(maxsize=None)
def cached_macroXS(ele_mat, energy):
    return material.macroXS(ele_mat, energy)

def simulate(world, samples, x_pos, y_pos, z_pos, energy_array, weight_array, tally_dict, max_depth=10, depth=0):
    if depth > max_depth:
        return

    w_cutoff = 0.25
    w_survival = 1
    weight_array_normalized = weight_array / np.sum(weight_array)

    for _ in range(samples):
        energy = np.random.choice(energy_array, p=weight_array_normalized)
        w = 1
        current_pos = [x_pos, y_pos, z_pos]

        alive = True
        while alive:
            surr_ele = simfunction.surr_elements(world, *current_pos)
            if not surr_ele:
                break  # particle leaves geometry, terminate

            targ_ele = random.choice(surr_ele)
            distance = np.linalg.norm(np.array(targ_ele) - np.array(current_pos))
            proj = np.linalg.norm([targ_ele[0] - current_pos[0], targ_ele[1] - current_pos[1]])
            cos_theta = proj / distance if distance != 0 else 1

            ele_mat = world[targ_ele[0], targ_ele[1], targ_ele[2]]
            macro_xs_dict = cached_macroXS(ele_mat, energy)
            total_xs = sum(macro_xs_dict.values())
            Sigma_s = macro_xs_dict.get('Sigma_s', 0)
            Sigma_t = Sigma_s * (1 - cos_theta)
            prob_interact = 1 - Sigma_t * distance

            rng_move = np.random.uniform(0, 1)

            if prob_interact == 0 or rng_move < prob_interact:
                current_pos = simfunction.continue_path(current_pos, targ_ele)
                continue  # particle moves without interaction

            # Interaction occurs here
            rng_reaction = np.random.uniform(0, total_xs)
            cumulative_prob = 0

            for reaction, xs_value in macro_xs_dict.items():
                cumulative_prob += xs_value

                if rng_reaction <= cumulative_prob:
                    if reaction == 'Sigma_s':
                        tally_dict['scatter'] = tally_dict.get('scatter', 0) + 1

                        # Implicit capture
                        w *= (Sigma_s / total_xs)
                        if w < w_cutoff:
                            if np.random.random() < (1 - Sigma_s / total_xs):
                                alive = False
                                break
                            else:
                                w = w_survival

                        new_pos = random.choice(simfunction.surr_elements(world, *current_pos))
                        simulate(world, 1, *new_pos, energy_array, weight_array, tally_dict, max_depth, depth+1)
                        alive = False
                        break

                    elif reaction == 'Sigma_f':
                        tally_dict['fission'] = tally_dict.get('fission', 0) + 1
                        fission_results = fission.generate_fission_results(ele_mat, energy)
                        n_prod = fission_results[2]
                        new_energy_array = fission_results[0]

                        for _ in range(n_prod):
                            new_pos = random.choice(simfunction.surr_elements(world, *current_pos))
                            simulate(world, 1, *new_pos, new_energy_array, [1], tally_dict, max_depth, depth+1)

                        alive = False
                        break

                    elif reaction == 'Sigma_a':
                        tally_dict['absorption'] = tally_dict.get('absorption', 0) + 1
                        alive = False
                        break

                    else:  # other reactions
                        reaction_info = material.getReaction(reaction)
                        product = reaction_info.get('Product')
                        if product:
                            tally_dict[product] = tally_dict.get(product, 0) + 1
                        alive = False
                        break

                    break  # reaction handled, exit loop
