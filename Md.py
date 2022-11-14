from ast import arg
from cmath import log
from importlib.resources import path
from multiprocessing.spawn import import_main_path
from re import A
import sys 
import os
from os import listdir
from enum import Enum
from datetime import datetime
from filehash import FileHash
#from dirhash import dirhash 
import json
import dominate
from dominate.tags import *
from checksumdir import dirhash

class Mode (Enum): 
    SCRIPT_PATH = 1                              
    RUN_PATH = 2                           
    DEFINED_PATH = 3                      

class TimeMode(Enum):
    UNIX = 1
    UTC = 2

class LS:
    def get_path(self, mode: Mode) -> str:                          
        if mode == Mode.SCRIPT_PATH: 
            return '/home/al/Desktop/mod1/' 
        elif mode == Mode.RUN_PATH:
            return './'                          
        elif mode == Mode.DEFINED_PATH:
            return sys.argv[2]                   
        
    def get_content_list(self, path: str) -> list:
        return listdir(path)
    
    def get_file_list(self, path: str) -> list:
        connect = listdir(path)
        file_list = []                          
        for i in connect:                     
            if os.path.isfile(os.path.join(path, i)): file_list.append(i)
        return file_list
  
    def get_directory_list(self, path: str) -> list:
        connect = listdir(path)
        folder_list = []
        for i in connect:
            if not os.path.isfile(os.path.join(path, i)): folder_list.append(i)
        return folder_list

    def get_file_info(self, path: str, time_mode: TimeMode) -> dict:                   
        unix_time = os.path.getmtime(path)
        utc_time = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
        time = unix_time if time_mode == TimeMode.UNIX else utc_time
        size = os.path.getsize(path)
        #owner = (subprocess.check_output(f"stat -c %G {file}", shell=True).rstrip()).decode("utf-8").strip("b'")
        md5hasher = FileHash('md5')
        file_hash = md5hasher.hash_file(path)
        return {
            'name': path,
            'time': time,
            'size': size,
            'hash': file_hash,
        }
 
    def get_directory_info(self, path: str, time_mode:TimeMode) -> dict:
        unix_time = os.path.getmtime(path)
        utc_time = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
        time = unix_time if time_mode == TimeMode.UNIX else utc_time
        size = os.path.getsize(path)
        md5hash = dirhash(path, 'md5')
        return {
            'name': path,
            'time': time,
            'size': size,
            'hash': md5hash,
        }
    
    def save_as(self, type: str, path: str, content: str):
        with open(path, 'w') as f:
            if type == 'json':
                temp_dict = {'j': content}
                json.dump(temp_dict, f)
            else:
                f.write(content)

    def save_as_txt(self,  path: str, content: str) -> None:                 
        self.save_as('txt', path, content)
  
    def save_as_csv(self, path: str, content: str) -> None:                 
        self.save_as('csv', path, content)
  
    def save_as_json(self,  path: str, content: str) -> None:                 
        self.save_as('json', path, content)
            
    def save_as_html(self, path: str, content) -> None:
        doc = dominate.document(title='LS')
        
        list = ul()
        for item in content:
            list += li(item)
            #list = list + li(item)
            for key, val in item.items():
                list.add(p(span(key), span(val)))
        doc.add(list)
        
        data = f'{doc}' #эkрaнровние
        self.save_as('txt', path, data)
               
    def run(self) -> None:
        mode_arg = sys.argv[1]
        if mode_arg == '-r':
            mode = Mode.RUN_PATH
        elif mode_arg == '-s':
            mode = Mode.SCRIPT_PATH
        else:
            mode= Mode.DEFINED_PATH
        
        path = self.get_path(mode)

        output_type = sys.argv[2] if mode != Mode.DEFINED_PATH else sys.argv[3]
        output_mode = sys.argv[3] if mode != Mode.DEFINED_PATH else sys.argv[4]
        time_arg = sys.argv[4] if mode != Mode.DEFINED_PATH else sys.argv[5]
        save_mode = sys.argv[5] if mode != Mode.DEFINED_PATH else sys.argv[6]
        
        if time_arg == '--unix':
            time_mode= TimeMode.UNIX
        else:
            time_mode= TimeMode.UTC
    
        print('All content', self.get_content_list(path))
        if output_type == '-f':
            if output_mode == '-l':
                content = self.get_file_list(path)
            else:
                content = []
                for file in self.get_file_list(path):
                    file_path=os.path.join(path,file)
                    content.append(self.get_file_info(file_path, time_mode))
        else:
            if output_mode == '-l':
                content = self.get_directory_list(path)
            else:
                content = []
                for file in self.get_directory_list(path):
                    dir_path=os.path.join(path,file)
                    content.append(self.get_directory_info(dir_path, time_mode))
        print(content)        
         
        if save_mode == '-t':
            print('txt')
            self.save_as_txt('report.txt', str(content))
        elif save_mode == '-j':
            print('json')
            self.save_as_json('report.json', str(content))
        elif save_mode == '-c':
            print('csv')
            self.save_as_csv('report.csv', str(content))                    
        else:
            print('html')
            self.save_as_html('report.html', content)        
        print('finish')
if __name__ == "__main__":
    LS().run() 