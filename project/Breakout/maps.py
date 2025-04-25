# Block types and their properties
BLOCK_TYPES = {
    1: {"color": (255, 255, 255), "durability": 1},  # Regular block (white)
    2: {"color": (0, 255, 0), "durability": 2},      # Strong block (green)
    3: {"color": (255, 0, 0), "durability": 1, "effect": "explosive"},  # Explosive block (red)
    4: {"color": (0, 0, 255), "durability": 1, "effect": "paddle_enlarge"},  # Paddle enlarger block (blue)
    5: {"color": (255, 255, 0), "durability": 1, "effect": "spawn_ball"},  # Ball spawner block (yellow)
}

# Map template where:
#  0 = Empty space
#  1 = Regular block
#  2 = Strong block
#  3 = Explosive block
#  4 = paddle enlarger
#  5 = ball spawner
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