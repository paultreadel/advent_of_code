from pathlib import Path

import cv2
from constants import MEDIA_DIR, PART1_EXAMPLE_FRAMES, PART1_PUZZLE_FRAMES
from tqdm import tqdm


def get_ordered_png_files(frames_dir):
    return sorted(list(map(str, Path(frames_dir).glob("*.png"))))


def generate_video(frames_dir, out_filename, fps=10):
    ordered_frames = get_ordered_png_files(frames_dir)

    # Read the first frame to get the size
    frame = cv2.imread(ordered_frames[0])
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(f"{MEDIA_DIR}/{out_filename}", fourcc, fps, (width, height))

    for img_path in tqdm(ordered_frames):
        img = cv2.imread(img_path)
        out.write(img)

    out.release()


generate_video(PART1_EXAMPLE_FRAMES, "part1_example.mp4", 2)
generate_video(PART1_PUZZLE_FRAMES, "part1_puzzle.mp4", 4000)
