# Block types and their properties
BLOCK_TYPES = {
    1: {"color": (255, 255, 255), "durability": 1},  # Regular block (white)
    2: {"color": (0, 255, 0), "durability": 2},      # Strong block (green)
    3: {"color": (255, 0, 0), "durability": 1},      # Power block (red)
}

# Map template where:
#  0 = Empty space
#  1 = Regular block
#  2 = Strong block
#  3 = Explosive block
# -1 = Random block
MAP_TEMPLATE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Empty row
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Empty row
    [0, 0, -1, -1, -1, -1, -1, -1, 0, 0],  
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, -1, -1, -1, -1, -1, -1, -1, -1, 0],
    [0, 0, 0, -1, -1, -1, -1, 0, 0, 0]  
]