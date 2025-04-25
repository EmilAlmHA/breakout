# Block types and their properties
BLOCK_TYPES = {
    1: {
        "color": (255, 255, 255),  # Regular block (white)
        "durability": 1,
        "score": 10
    },
    2: {
        "color": (0, 255, 0),      # Strong block (green)
        "durability": 2,
        "score": 20
    },
    3: {
        "color": (255, 0, 0),      # Explosive block (red)
        "durability": 1,
        "effect": "explosive",
        "score": 40
    },
    4: {
        "color": (0, 0, 255),      # Paddle enlarger block (blue)
        "durability": 1,
        "effect": "paddle_enlarge",
        "score": 30
    },
    5: {
        "color": (255, 255, 0),    # Ball spawner block (yellow)
        "durability": 1,
        "effect": "spawn_ball",
        "score": 25
    }
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