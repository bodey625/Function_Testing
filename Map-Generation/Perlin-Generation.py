import random
from PIL import Image, ImageDraw
# Refer to Pillow Documentation here: https://pillow.readthedocs.io/en/latest/handbook/index.html

# Be sure to use environments when importing libraries for specific projects, so as to avoid 
# overbloating your default / global interpretation settings


# Initialize the random number generator with a given seed
def initialize_rng(seed: str):
    random.seed(seed)




# Fade function to smooth the interpolation
def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

# Linear interpolation function (creating points in between existing points to refine the resolution of the graph)
# t is the function weight, should be in range [0.0, 1,0]
def lerp(t, a, b):
    return a + t * (b - a)
# Also option to add further derivatives to further smooth out the function, look at 
# Smoothstep: return (a1 - a0) * (3.0 - w * 2.0) * w * w + a0;
# or Smootherstep: return (a1 - a0) * ((w * (w * 6.0 - 15.0) + 10.0) * w * w * w) + a0;


# Gradient function to calculate dot product of the distance and gradient vectors
def grad(hash, x, y):
    # hash is used to determine the gradient vector direction
    # h is the lower 2 bits of the hash
    h = hash & 3
    u = x if h & 1 == 0 else -x
    v = y if h & 2 == 0 else -y
    
    # Return the dot product of the selected gradient and the distance vector (x, y)
    return u + v


# Perlin noise function to generate noise values at a given coordinate
def perlin(x, y, perm):
    # Calculate the unit grid cell coordinates (upper-left corner)
    xint = int(x) & 255
    yint = int(y) & 255

    # Calculate relative coordinates within the grid cell
    xfloat = x - int(x)
    yfloat = y - int(y)

    # Compute fade curves for x and y
    u = fade(xfloat)
    v = fade(yfloat)

    # Hash coordinates of the 4 grid corners
    aa = perm[perm[xint] + yint]
    ab = perm[perm[xint] + yint + 1]
    ba = perm[perm[xint + 1] + yint]
    bb = perm[perm[xint + 1] + yint + 1]

    # Calculate the gradient and interpolate
    x1 = lerp(u, grad(aa, xfloat, yfloat), grad(ba, xfloat - 1, yfloat))
    x2 = lerp(u, grad(ab, xfloat, yfloat - 1), grad(bb, xfloat - 1, yfloat - 1))
    return lerp(v, x1, x2)


# This is the function that actually creates the perlin map
def generate_perlin_noise_map(width: int, height: int, scale: float, seed: int):
    # Initialize the random number generator
    random.seed(seed)

    # Create a permutation table and duplicate it
    permutation = [i for i in range(256)]
    random.shuffle(permutation)
    perm = permutation * 2

    # Initialize a 2D array to store the noise values
    world = [[0 for _ in range(width)] for _ in range(height)]

    # Generate noise values for each cell in the 2D array
    for y in range(height):
        for x in range(width):
            # Normalize coordinates to the scale
            nx = x / scale
            ny = y / scale
            # Generate Perlin noise value for the current coordinates
            world[y][x] = perlin(nx, ny, perm)
    return world


# Most or all of this perlin code could be imported from a library instead of just using it here like this
# but its useful for learning how it works


# Convert the map of noise values to the output image
def map_to_image(map_grid):
    height = len(map_grid)
    width = len(map_grid[0])
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    for y in range(height):
        for x in range(width):
            value = map_grid[y][x]

             # Determine color based on noise value, range [0.0, 1.0]:
            if value < 0:  # Adjust the threshold for water/land
                color = (255, 255, 255) # (0, 0, 255)  # Water, blue 
            # elif value < .2:
            #     color = (150, 150, 150) # (34, 139, 34)  # Land, Green
            # elif value < .4:
            #     color = (75, 75, 75)
            # elif value < .6:
            #     color = (50, 50, 50)
            # elif value < .8:
            #     color = (25, 25 ,25)  
            else: 
                color = (0, 0, 0) # Mountain?

            # put the color on the image at that point
            draw.point((x, y), fill=color)
    
    return image


def main(seed: str, width: int, height: int):
    initialize_rng(seed)
    scale = 10.0  # Adjust the scale to change the zoom level of the noise
    seed_int = random.randint(0, 100)
    
    map_grid = generate_perlin_noise_map(width, height, scale, seed_int)
    image = map_to_image(map_grid)
    image.show()

# Entry point, initialize base values
if __name__ == "__main__":
    seed = "your_seed_string"
    width, height = 1000, 1000  # Set desired map dimensions
    main(seed, width, height)
