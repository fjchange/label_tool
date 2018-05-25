import os
import sys
import shutil


res_path='D:/MyDownloads/cow_head/res'

def mv_img(path):
    for i in os.walk(path):
        if len(i[1])==0:
            for img_name in i[2]:
                img_path=os.path.join(i[0],img_name)
                shutil.move(img_path,path)


if __name__=='__main__':
    for i in os.walk(res_path):
        if len(i[1])!=0:
            for j in i[1]:
                print(j)
                mv_img(os.path.join(res_path,j))