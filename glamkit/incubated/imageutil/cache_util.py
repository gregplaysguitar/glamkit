import os

def file_hash(file_path):
    #returns a hash of the file path plus its modification date
    
    datehash = hash(os.path.getmtime(file_path))
    namehash = hash(file_path)
    
    return datehash+namehash