import numpy as np
import geometry


print("Welcome to the diffusion solver. To get things started, please create your world, and then slab geometry:")
user_input = input("Enter world creation command (e.g., geometry.create_world(x, y, z)): ")
world, origin = eval(user_input)
print(f"Great ! You created an empty void. Type in the slab that you want to create")


while True:
    user_input = input("Enter a geometry creation command (e.g., geometry.create_slab(world, origin, xi, xf, yi, yf, zi, zf)): ")

    if user_input.strip().lower() == "done":
        print(f"Great ! You created a slab")
        break

    if user_input.strip().lower() == "delete":
        world = np.zeros_like(world)
        continue

    world = eval(user_input)
    print(world)



