#!/usr/bin/env python
# coding: utf-8



import os
import base64 
from PIL import Image
import tqdm

from os import path
from concurrent.futures import ThreadPoolExecutor
output_dir = "./testing/"


def combine_label_files(first_file,second_file,output_file):
    
    file_names = [first_file,second_file]
    with open(output_file, 'w') as outfile:
        for fname in file_names:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
    
    
def read_last_n_lines(file_name,starting_byte,should_truncate=False):
    last_n_lines = []
    with open(file_name, "r+") as file:
        file_size = os.fstat(file.fileno()).st_size

        file.seek(0, os.SEEK_END)              
        file.seek(file.tell() - min(starting_byte,file_size), os.SEEK_SET) 
        file.readline()
        first_line_bytes = file.tell() 

        counter = 0

        while True:
            line = file.readline()[:-1] # remove the trailing endline
            if line:
                counter += 1
                last_n_lines.append(line.split("\t"))
            else:
                break

                
        file.seek(first_line_bytes)
        if should_truncate:
            file.truncate()
            
        
        return  [(line[0],line[1],line[4],line[-1]) for line in last_n_lines]

    

    
def construct_dictionary(combined_file_path):
    dictionary = {}

    with open(combined_file_path,"r") as f:
        lines = f.readlines()
        print(len(lines))
        for line in lines:
            
            left,right = line.strip().split(" ")
            dictionary[right] = left
    
    return dictionary



dic = construct_dictionary("./combined.txt")


last_n_lines = read_last_n_lines("/home/harsh/Downloads/MS-Celeb-1M/data/aligned_face_images/FaceImageCroppedWithAlignment.tsv",1000000,100000000000) 


combine_label_files("./clean_list_128Vec_WT051_P010.txt","relabel_list_128Vec_T058.txt","./combined.txt")



def decode_and_save(dir_name,file_name,wrong_face_id,base64Image):
    key = f"{dir_name}/{file_name}-{wrong_face_id}.jpg"
    if key not in dic:
        return
    
    class_name = dic[key]
    full_path = path.join(output_dir,class_name)
        
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        
    img_name = os.path.join(full_path,f"{file_name}.jpg")  
    with open(img_name, 'wb') as f:
        imgdata = base64.b64decode(base64Image)
        f.write(imgdata)
    
    




def do():

    with ThreadPoolExecutor(max_workers = 16) as executor:
        with tqdm() as pbar:


            while True:
                values = read_last_n_lines("./head.tsv",5000000,should_truncate=False)

                if not values:
                    break

                executor.map(decode_and_save, *list(zip(*values)))
                pbar.update()
            




do()

