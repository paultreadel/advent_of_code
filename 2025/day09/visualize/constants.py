import os

MEDIA_DIR = "./media"
PART1_EXAMPLE_FRAMES = MEDIA_DIR + "/part1_example"
PART1_PUZZLE_FRAMES = MEDIA_DIR + "/part1_puzzle"
os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(PART1_EXAMPLE_FRAMES, exist_ok=True)
os.makedirs(PART1_PUZZLE_FRAMES, exist_ok=True)
