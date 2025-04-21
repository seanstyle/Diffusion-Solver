import numpy as np
def create_world(x, y, z):
        x_length = len(np.zeros(x))
        y_length = len(np.zeros(y))
        z_length = len(np.zeros(z))
        
        x_axis = int(x_length/2)
        y_axis = int(y_length/2)
        z_axis = int(z_length/2)

        geometry = np.zeros((x_length, y_length, z_length))
        origin = np.array([x_axis, y_axis, z_axis])

        print(geometry)
        return geometry, origin

def create_slab(geometry, origin, xi, xf, yi, yf, zi, zf):
        x_length = xf - xi + 1
        y_length = yf - yi + 1
        z_length = zf - zi + 1
        
        x_array = []
        for i in range(x_length):
                x_array.append(int(xi + i))
        y_array = []
        for i in range(y_length):
                y_array.append(int(yi + i))
        z_array = []
        for i in range(z_length):
                z_array.append(int(zi + i))

        for i in range(x_length):
                for j in range(y_length):
                        for k in range(z_length):
                                geometry[origin[0] + x_array[i],
                                         origin[1] + y_array[j],
                                         origin[2] + z_array[k]
                                         ] = 1
                                        

        #print(geometry)
        return geometry