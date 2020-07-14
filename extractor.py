"""
Extraction system for cleaned MS Celeb Dataset
"""
import base64
import os
from concurrent.futures import ThreadPoolExecutor
from os import path

from tqdm import tqdm

OUTPUT_DIR = "./testing/"


def combine_label_files(first_file, second_file, output_file):
    """Given the paths of the clean_list_128Vec_WT051_P010 and
    relabel_list_128Vec_T058.txt, generate a 3rd file that is
    the combination of both. It simply appends one file on to the next.

    Args:
        first_file ([str]): path of clean list
        second_file ([str]): path of relabel listk
        output_file ([str]): path of output file 
    """

    file_names = [first_file, second_file]
    with open(output_file, 'w') as outfile:
        for fname in file_names:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)


def read_last_n_lines(file_name, starting_byte):
    """Read the last N lines of a file. This function truncates the file
    after reading the bytes from starting_byte till the end of the file.

    Args:
        file_name ([string]): [path of the file to read]
        starting_byte ([int]): [number of bytes to jump to]

    Returns:
        A list of the lines read in the tsv
    """

    last_n_lines = []
    with open(file_name, "r+") as file:
        file_size = os.fstat(file.fileno()).st_size
        file.seek(0, os.SEEK_END)
        file.seek(file.tell() - min(starting_byte, file_size), os.SEEK_SET)
        file.readline()
        first_line_bytes = file.tell()

        counter = 0

        while True:
            line = file.readline()[:-1]  # remove the trailing endline
            if line:
                counter += 1
                last_n_lines.append(line.split("\t"))
            else:
                break

        file.seek(first_line_bytes)
        file.truncate()

        return [(line[0], line[1], line[4], line[-1]) for line in last_n_lines]


def construct_dictionary(combined_file_path):
    dictionary = {}

    with open(combined_file_path, "r") as f:
        lines = f.readlines()
        print(len(lines))
        for line in lines:

            left, right = line.strip().split(" ")
            dictionary[right] = left

    return dictionary


dic = construct_dictionary("./combined.txt")


# last_n_lines = read_last_n_lines(
#     "/home/harsh/Downloads/MS-Celeb-1M/data/aligned_face_images/FaceImageCroppedWithAlignment.tsv", 1000000, 100000000000)


# combine_label_files("./clean_list_128Vec_WT051_P010.txt",
# "relabel_list_128Vec_T058.txt", "./combined.txt")


def decode_and_save(dir_name, file_name, wrong_face_id, base64Image):
    """Take values from each line in the tsv and save it to 
    the directory with the name of the face id. 


    Args:
        dir_name (str): [path of the root directory to save to]
        file_name ([type]): [this is the first column's value in the tsv]
        wrong_face_id ([type]): [incorrectly labeled face id from the tsv]
        base64Image ([type]): [last column's value from the tsv]
    """
    key = f"{dir_name}/{file_name}-{wrong_face_id}.jpg"
    if key not in dic:
        return

    class_name = dic[key]
    full_path = path.join(OUTPUT_DIR, class_name)

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    img_name = os.path.join(full_path, f"{file_name}.jpg")
    with open(img_name, 'wb') as f:
        imgdata = base64.b64decode(base64Image)
        f.write(imgdata)


def run():

    with ThreadPoolExecutor(max_workers=16) as executor:
        with tqdm() as pbar:

            while True:
                values = read_last_n_lines(
                    "./head.tsv", 5000000)

                if not values:
                    break

                executor.map(decode_and_save, *list(zip(*values)))
                pbar.update()


do()
