import os,sys
#遍历文件夹中的txt文件，替换字符串

def alter(file,old_str,new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:
    """
    toFile = file[:-4]+"_back.txt";
    with open(file, "r", encoding="utf-8") as fread, open(toFile, "w", encoding="utf-8") as fwrite:
        for line in fread:
            line = line.replace(old_str,new_str)
            fwrite.write(line)
    os.remove(file)
    os.rename(toFile,file)


sourceDir = "."

if len(sys.argv) > 1:
    sourceDir = sys.argv[1]

list = os.listdir(sourceDir)
fileTimePairs = [(os.path.join(sourceDir, i), os.stat(os.path.join(sourceDir, i)).st_mtime) for i in list]  #文件名-时间

for i in sorted(fileTimePairs, key=lambda x: x[1]): #按时间顺序处理文件
    pathFile = i[0]
    if os.path.isfile(pathFile) and os.path.splitext(pathFile)[1] == ".txt":
        print(pathFile)
        alter(pathFile,"ulPL:65535","ulPL:0")

