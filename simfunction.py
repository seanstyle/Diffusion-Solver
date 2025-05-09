'''
"simfunction.py" is a function that aids "sim.py" by facilitating physical processes of particle transport.
'''

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

def continue_path(current_position, possible_neighbor):
    x1, y1, z1 = current_position
    x2, y2, z2 = possible_neighbor
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    
    forward = (x1 + dx, y1 + dy, z1 + dz)
    return forward

def tally(list_of_interactions):
    return {reaction: 0 for reaction in set(list_of_interactions)}
