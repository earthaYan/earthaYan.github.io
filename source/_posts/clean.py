import os
import shutil
# 获取当前文件夹下的所有文件和文件夹
import os
import shutil

# 获取当前目录下的所有文件和文件夹
files_and_folders = os.listdir()

# 遍历每个文件夹
for folder in files_and_folders:
    # 检查是否是文件夹
    if os.path.isdir(folder):
        # 检查是否没有同名的md文件或者是空文件夹
        if not os.path.exists(f"{folder}.md") or len(os.listdir(folder)) == 0:
            # 删除文件夹及其内容
            shutil.rmtree(folder)
