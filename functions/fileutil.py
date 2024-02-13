from tkinter import filedialog
import os
import shutil

def upload_file() -> str:
    os.makedirs(os.getcwd() + "\\files", exist_ok=True)
    file_path = filedialog.askopenfilename()
    if(file_path):
        print(file_path)
        if(check_file(file_path)):
            new_path=create_path_name_unique(os.getcwd() + "\\files", os.path.basename(file_path))
            copy_file(file_path, new_path)
            return new_path
    else:
        return("")

def check_file(path, delim=",") -> bool:
    with open(path, "r", encoding="UTF-8") as f:
        for line in f.readlines():
            if(len(line.split(delim)) != 2):
                return False
        return True


def copy_file(src, dst) -> None:
    shutil.copyfile(src, dst)

def create_path_name_unique(folder:str, filename:str)->str:
    path=f"{folder}\\{filename}"
    if(os.path.exists(path)):
        name_ext=filename.split(".")
        if(len(name_ext)==1):
            name=filename
            ext=""
        else:
            name=name_ext[0]
            ext=name_ext[1]
        i=1
        while os.path.exists(f"{folder}\\{name}({i}).{ext}"):
            i+=1
        path=f"{folder}\\{name}({i}).{ext}"

    print(path)
    return path

def delete_files(filenames: list[str])->None:
    for path in filenames:
        delete_file(path)

def delete_file(filename):
    try:
        os.remove(filename)
    except:
        pass