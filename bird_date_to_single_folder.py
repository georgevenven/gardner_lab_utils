import os
import shutil
from tqdm import tqdm
from multiprocessing import Pool

src = "/media/george-vengrovski/disk2/zebra_finch/RachelYuan_zebra_finch_data"
dst = "/media/george-vengrovski/disk2/zebra_finch/combined_wav"

if not os.path.exists(dst):
    os.makedirs(dst)

def copy_file(args):
    song_src_path, song_dst_path = args
    if not os.path.exists(song_dst_path):
        shutil.copy(song_src_path, song_dst_path)
    else:
        print(f"File {song_dst_path} already exists. Skipping.")

def process_bird(bird):
    bird_path = os.path.join(src, bird)
    if not os.path.isdir(bird_path):
        return []

    file_pairs = []
    for day in os.listdir(bird_path):
        day_path = os.path.join(bird_path, day)
        if not os.path.isdir(day_path):
            continue

        for song in os.listdir(day_path):
            song_src_path = os.path.join(day_path, song)
            song_dst_path = os.path.join(dst, song)
            file_pairs.append((song_src_path, song_dst_path))

    return file_pairs

if __name__ == "__main__":
    with Pool() as pool:
        file_pairs = []
        for bird in os.listdir(src):
            file_pairs.extend(process_bird(bird))

        with tqdm(total=len(file_pairs), desc="Copying files") as pbar:
            for _ in pool.imap_unordered(copy_file, file_pairs):
                pbar.update()