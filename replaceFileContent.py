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
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)

rootdir = "./"
if len(sys.argv) > 1:
    rootdir = sys.argv[1]
lists = os.listdir(rootdir) #列出文件夹下所有的目录与文件
print(lists)
for list in lists:
    path = os.path.join(rootdir, list)
    if os.path.isfile(path) and os.path.splitext(path)[1] == ".txt":
        print(path)
        alter(path,"through:65535","through:0")
