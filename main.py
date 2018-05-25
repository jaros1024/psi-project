import os
import pandas

def processPerson(path):
    print(next(os.walk('.'))[1]);

#rootPath = input("Enter root path of the data: ")
rootPath = "C:\\Users\Jarek\Desktop\PSI\projekt\PSI 2018 - projekt - analiza danych"
print("Starting data processing")
print(f"Root directory is {rootPath}")

dirs = next(os.walk(rootPath+"/2018-afcai-spring"))[1]

for directory in dirs:
    processPerson(rootPath+directory+"/"+directory)
    break
