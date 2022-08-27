import os
import random
from PIL import Image

def gen_anchor(dname:str) -> None:
    '''
    Function for generating anchor data in the present directory
    -------------------
    dname : path or name of the source data directory
    ''' 
    for entry in os.scandir(dname):
        if entry.is_file():
            name = entry.path
            img = Image.open(name)

            os.makedirs(os.path.join('anchor', name[4:9]))
            for i in range(1, 11):
                img.save(f"anchor/{name[4:9]}/{name[4:9]}_{i}.png", quality=95)


def gen_negative(dname:str) -> None:
    '''
    Function for generating negative training data in the present directory
    -------------------
    dname : path or name of the source data directory
    '''
    qlist = [50, 25, 75, 30, 40]
    for entry in os.scandir(dname):
        if entry.is_file():
            name = entry.path
            img = Image.open(name)

            os.makedirs(os.path.join('negative', name[4:9]))
            for i in range(1, 11):
                img.save(f"negative/{name[4:9]}/{name[4:9]}_{i}.png", quality = random.choice(qlist))


def gen_positive(dname:str) -> None:
    '''
    Function for generating positive training data in the present directory
    -------------------
    dname : path or name of the source data directory
    '''
    files = 0
    for file in os.scandir(dname):
        if file.is_file():
            files += 1
    
    no_of_copies = files - 3
    for entry in os.scandir(dname):
        if entry.is_file():
            name = entry.path
            img = Image.open(name)

            for dno in range(0, no_of_copies + 1):
                d_name = f"{name[4:9]}_{dno}"
                os.makedirs(os.path.join('positive', d_name))
                for i in range(1, 11):
                    img.save(f"positive/{d_name}/{name[4:9]}_{i}.png", quality = random.randrange(10, 95))


if __name__ == "__main__":
    d_name = "090-00"
    gen_anchor(d_name)
    gen_negative(d_name)
    gen_positive(d_name)