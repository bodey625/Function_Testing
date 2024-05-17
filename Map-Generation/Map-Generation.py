import random
from PIL import Image, ImageDraw

def initialize_rng(seed: str):
    random.seed(seed)

def generate_map(width: int, height: int):
    map_grid = []
    for y in range(height):
        row = []
        for x in range(width):
            # Example: 0 for water, 1 for land
            cell = random.choice([0, 1])
            row.append(cell)
        map_grid.append(row)
    return map_grid

def display_map(map_grid):
    height = len(map_grid)
    width = len(map_grid[0])
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    
    for y in range(height):
        for x in range(width):
            color = (0, 0, 255) if map_grid[y][x] == 0 else (34, 139, 34)
            draw.point((x, y), fill=color)
    
    image.show()

def main(seed: str, width: int, height: int):
    initialize_rng(seed)
    map_grid = generate_map(width, height)
    display_map(map_grid)

if __name__ == "__main__":
    seed = "BBB"
    width, height = 1000, 1000  # Set desired map dimensions
    main(seed, width, height)
