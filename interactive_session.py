import numpy as np
import geometry
import sim
import simfunction

print("""
   _____                 _                 
  / ____|               | |                
 | (___   ___  _ __ ___ | |__   __ _ _ __  
  \___ \ / _ \| '__/ _ \| '_ \ / _` | '_ \ 
  ____) | (_) | | | (_) | |_) | (_| | | | |
 |_____/ \___/|_|  \___/|_.__/ \__,_|_| |_|                                          
""")

print("Welcome to the diffusion solver. First, create your world and slab geometry:")

# Create world
user_input = input("Enter world creation command (e.g., geometry.create_world(x, y, z)): ")
world, origin = eval(user_input)
print("Great! You created an empty world. Now let's add slabs.")

# Create slabs
while True:
    user_input = input("Enter geometry creation command (or type 'done' to finish, 'delete' to reset): ")
    if user_input.strip().lower() == "done":
        print("Great! Geometry setup complete.")
        break
    if user_input.strip().lower() == "delete":
        world = np.zeros_like(world)
        print("World reset to empty.")
        continue

    world = eval(user_input)
    print(world)

# Gather simulation parameters
samples = int(input("Enter the number of samples (e.g., 1000): "))
x_pos = int(input("Enter initial x position (e.g., 0): "))
y_pos = int(input("Enter initial y position (e.g., 0): "))
z_pos = int(input("Enter initial z position (e.g., 0): "))

# Energy and weight arrays
energy_input = input("Enter energy array values separated by commas (e.g., 2.0,0.5,0.1): ")
energy_array = np.array([float(e.strip()) for e in energy_input.split(",")])

weight_input = input("Enter corresponding weight array values separated by commas (e.g., 0.5,0.3,0.2): ")
weight_array = np.array([float(w.strip()) for w in weight_input.split(",")])

# Tally types
initial_tally_input = input("Enter tally types separated by commas (e.g., scatter,fission,absorption): ")
initial_tally = [item.strip() for item in initial_tally_input.split(",")]

# Initialize tally dictionary once
tally_dict = simfunction.tally(initial_tally)

# Run the simulation
print("\nStarting simulation...")
sim.simulate(world, samples, x_pos, y_pos, z_pos, energy_array, weight_array, tally_dict)

# Print final tally results once
print("\nFinal Tally Results (after simulation):")
for tally_name, tally_value in tally_dict.items():
    print(f"{tally_name}: {tally_value}")

def setup(world):
    return world