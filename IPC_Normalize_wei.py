import json, re, os, datetime
from tqdm import tqdm_notebook as tqdm
# from tqdm import tqdm
from os.path import isfile
from os import listdir

def ipc45_process(ipc_p):
    string2 = ipc_p.split('/')
    level4 = string2[0]
    level5 = string2[1]
        
    # process Level 4
    level4 = level4.lstrip('0')
    
    # process Level 5    
    level5 = level5.lstrip('0')
    
    if(len(level5) == 1 or len(level5) == 3):
        level5 = '0' + level5
    if(level5 == ''):
        level5 = '00'
        
    return level4 + '/' + level5

def ipc_format(ipc):
    if ' ' in ipc:
        string1 = ipc.split(' ')
        result = ipc45_process(string1[1])           
        return string1[0] + ' ' + result
    
    else:
        string1 = ipc[0:4]
        result = ipc45_process(ipc[4:])
        return string1 + ' ' + result
        
def ipc_check(ipc):
    if '.' not in ipc:
        ipc_regex = r'^[A-H][0-9]{2}[A-Z][\s]{0,1}[0-9]{1,3}/[0-9]{1,4}$'    
        return bool(re.match(ipc_regex, ipc))
    else:
        return False


if __name__ == '__main__':
    while(True):
        IPC = input('請輸入IPC分類碼：')
        if ipc_check(IPC):
            print(ipc_format(IPC))
        else:
            print('錯誤的IPC分類碼！')

