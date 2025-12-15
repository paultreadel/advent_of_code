import os

MEDIA_DIR = "./media"
PART1_EXAMPLE_FRAMES = MEDIA_DIR + "/part1_example"
PART1_PUZZLE_FRAMES = MEDIA_DIR + "/part1_puzzle"
PART2_EXAMPLE_FRAMES = MEDIA_DIR + "/part2_example"
os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(PART1_EXAMPLE_FRAMES, exist_ok=True)
os.makedirs(PART1_PUZZLE_FRAMES, exist_ok=True)
os.makedirs(PART2_EXAMPLE_FRAMES, exist_ok=True)
