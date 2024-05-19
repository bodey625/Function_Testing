import random
from PIL import Image, ImageDraw
# Refer to Pillow Documentation here: https://pillow.readthedocs.io/en/latest/handbook/index.html

# Be sure to use environments when importing libraries for specific projects, so as to avoid 
# overbloating your default / global interpretation settings


# Initialize the random number generator with a given seed
def initialize_rng(seed: str):
    random.seed(seed)




# SmoothStep function to smooth the kinks in the lerp function
def SmoothStep(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

# Linear interpolation function (creating points in between existing points to refine the resolution of the graph)
# t is the function weight, should be in range [0.0, 1,0]
def lerp(t, a, b):
    return a + t * (b - a)
# Also option to add further derivatives to further smooth out the function, look at 
# Smoothstep: return (a1 - a0) * (3.0 - w * 2.0) * w * w + a0;
# or Smootherstep: return (a1 - a0) * ((w * (w * 6.0 - 15.0) + 10.0) * w * w * w) + a0;

# where t is the weight (current value), a is the min value, and b is the max value
def inverseLerp(t, a, b):
    try:
        return (t - a) / (b - a)
    except ZeroDivisionError:
        return 1



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

    # Compute SmoothStep curves for x and y
    u = SmoothStep(xfloat)
    v = SmoothStep(yfloat)

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
def generate_perlin_noise_map(width: int, height: int, scale: float, seed: int, octaves: int, persistance: float, lacunarity: float):
    # Initialize the random number generator
    random.seed(seed)

    # Create a permutation table and duplicate it
    permutation = [i for i in range(256)]
    random.shuffle(permutation)
    perm = permutation * 2

    # Initialize a 2D array to store the noise values
    world = [[0 for _ in range(width)] for _ in range(height)]

    minNoiseHeight = float('inf')
    maxNoiseHeight = float('-inf')

    # Generate noise values for each cell in the 2D array
    for y in range(height):
        for x in range(width):

            amplitude = 1.0
            frequency = 1.0
            noiseHeight = 0.0

            for _ in range(octaves):
                 # Normalize coordinates to the scale
                nx = x / scale * frequency
                ny = y / scale * frequency
                # Generate Perlin noise value for the current coordinates
                #       world[y][x] = perlin(nx, ny, perm)
                perlinValue = perlin(nx, ny, perm) * 2 - 1   # * 2 - 1 allows for negative values so that it may decrease
                noiseHeight += perlinValue * amplitude
                amplitude *= persistance
                frequency *= lacunarity

            if noiseHeight > maxNoiseHeight:
                maxNoiseHeight = noiseHeight
            elif noiseHeight < minNoiseHeight:
                minNoiseHeight = noiseHeight
            world[y][x] = noiseHeight

    # normalize values before adding to map
    for y in range(height):
        for x in range(width):
            world[y][x] = inverseLerp(world[y][x], minNoiseHeight, maxNoiseHeight)
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

            colorSet_1 = [(0, 0, 0), (25, 25, 25), (50, 50, 50), (75, 75, 75), (150, 150, 150), (255, 255, 255)] # greyscale
            colorSet_2 = [(0, 0, 255), (25, 150, 255), (200, 175, 50), (34, 200, 34), (34, 139, 34), (100, 100, 100)] # Good land gradient from sea to forest
            #              Pure Blue       Teal            Yellow       light Green     Deep Green

            # o:4 p:0.5 l:1.5   wow, you can really tell that most of the space here is taken up by colorset[3]. unfortunately, thats also just sand.
            # seems to be a fairly common theme. might be good to break up the <.6 with < .5


            colorset = colorSet_1

            #  # Determine color based on noise value, range [0.0, 1.0]:
            if value < .2:
                color = colorset[0] # (34, 139, 34)  # Land, Green
            elif value < .4:
                color = colorset[1]
            elif value < .5:
                color = colorset[2]
            elif value < .6:
                color = colorset[3]
            elif value < .8:
                color = colorset[4]
            else: 
                color = colorset[5] # Mountain?

            draw.point((x, y), fill=color)
    
    return image


def main(seed: str, scale: int, width: int, height: int, octaves: int, persistance: float, lacunarity: float):
    initialize_rng(seed)
    seed_int = random.randint(0, 100)
    
    map_grid = generate_perlin_noise_map(width, height, scale, seed_int, octaves, persistance, lacunarity)
    image = map_to_image(map_grid)
    image.show()

# Entry point, initialize base values
if __name__ == "__main__":
    seed = "Astley" # Case sensitive!
    scale = 40  # Adjust the scale to change the zoom level of the noise
    width, height = 512, 512  # Set desired map dimensions

    octaves = 4 # seems to affect zoom, actually effectively halves the length of a cell, creating more detail
    persistance = .5 # reduces the strength each successive octave has on the last (reccommend < 1)
    lacunarity = 2.0  # determines octave scaling. (4 octaves with lacu. of 2.0 is 4 layers, each at half the size as the last)


    main(seed, scale, width, height, octaves, persistance, lacunarity)



# This script has a few issues i can identify, some of which you might not even classify as issues typically.
# - this script should have a x and y offset function to scroll through the map, and is worse for not having one
# - This script would do better to be continually updated as you adjust the values, and for that purpose it would be best to move it into unity or unreal
# - if you zoom far enough in, the normalization function will start changing geography
#       (Limited effect at all levels of scale, but destroys consistent geography above scale = 200)
# - Scale zooms in on top left corner, center would be better
# - Overall this script is a bit of a mess, and id like to come back and clean it up
#
#
#   TODO: We should rebulid this and test as we build. this video is a good resource:
#   https://www.youtube.com/watch?v=ZsEnnB2wrbI&list=TLPQMTkwNTIwMjR67wN7pfENKA