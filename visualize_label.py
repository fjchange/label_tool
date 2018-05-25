#coding=utf-8
from tkinter import *
from PIL import Image,ImageTk
import csv
import os
import sys
class visual_label():
    #读取csv文件中对应的行数据，然后返回图片路径，以及对应的标记号
    def csv_reader(self):
        with open(self.csv_path+'/'+self.video_num+'.csv','r')as c:
            reader=csv.reader(c)
            #if labeled_kind>max_showing_pic_num:
            self.csv_list=[row for row in reader]

    #最终写原csv
    def csv_writer(self):
        with open(self.csv_path+'/'+self.video_num+'.csv','w',newline='')as c:
            writer=csv.writer(c)
            writer.writerows(self.csv_list)

    def click(self,i):
        self.showing_list[i][0]=self.csv_list[0][2].replace('\'',"")
        self.csv_list[self.labeling_row_num].append(self.showing_list[i][1])
        self.labeling_row_num+=1
        self.image_set()
        self.if_add_new=False

    def click1(self):
        self.click(0)
    def click2(self):
        self.click(1)
    def click3(self):
        self.click(2)
    def click4(self):
        self.click(3)
    def click5(self):
        self.click(4)

    def init(self):
        self.csv_reader()
        self.image_set()

    def click_new(self):
        if len(self.showing_list)==5:
            self.if_add_new = True
            self.replaced=self.showing_list.pop(0)
        self.showing_list.append([self.csv_list[self.labeling_row_num][2].replace('\'',""),self.labeled_kind])
        if len(self.csv_list[0]) < 4:
            self.csv_list[self.labeling_row_num].append(self.labeled_kind)
        else:
            self.csv_list[self.labeling_row_num][3]=self.labeled_kind

        self.labeling_row_num+=1
        self.labeled_kind+=1
        self.image_set()

    def click_absnormal(self):
        self.csv_list[self.labeling_row_num].append(-1)
        self.labeling_row_num+=1
        self.image_set()

    def  click_re(self):
        self.labeling_row_num-=1
        self.csv_list[self.labeling_row_num].pop()
        if self.if_add_new and len(self.showing_list)>=1:
            self.labeled_kind-=1
            self.showing_list.pop()
            self.showing_list.insert(0,self.replaced)
        self.image_set()
        self.if_add_new=False
        self.replaced=None

    def image_set(self):
        if self.labeled_kind==0:
            if len(self.csv_list[0])<4:
                self.csv_list[0].append(0)
            else:self.csv_list[0][3]=0

            self.labeling_row_num+=1
            self.showing_list.append([self.csv_list[0][2].replace('\'',""),self.labeled_kind])
            self.labeled_kind+=1
            return self.image_set()

        elif self.labeled_kind<=4 and self.labeled_kind>0:
            for i in range(self.labeled_kind):
                jpg=Image.open(self.res_path+'/'+self.video_num+'/'+self.showing_list[i][0]+'.jpg')
                if i<len(self.pic):
                    self.pic[i]=ImageTk.PhotoImage(jpg)
                else:
                    self.pic.append(ImageTk.PhotoImage(jpg))
                self.pic_[i].configure(image=self.pic[i])
                self.but_[i].configure(text=self.showing_list[i][1].__str__())

        else :
            for i in range(5):
                jpg=Image.open(self.res_path+'/'+self.video_num+'/'+self.showing_list[i][0]+'.jpg')
                if i<len(self.pic):
                    self.pic[i]=ImageTk.PhotoImage(jpg)
                else:
                    self.pic.append(ImageTk.PhotoImage(jpg))
                self.pic_[i].configure(image=self.pic[i])
                self.but_[i].configure(text=self.showing_list[i][1].__str__())

        if self.labeling_row_num<len(self.csv_list):
            jpg=Image.open(self.res_path+'/'+self.video_num+'/'+self.csv_list[self.labeling_row_num][2].__str__()+'.jpg')
            self.pic_n = ImageTk.PhotoImage(jpg)
            self.pic_new.configure(image=self.pic_n)
        else:
            self.csv_writer()

        if self.labeling_row_num%10:
            self.csv_writer()

    def __init__(self):
        self.root = Tk()
        self.root.title('label_cow_head')
        self.root.geometry('1920x1080')

        # 默认路径
        self.csv_path = "D:/MyDownloads/cow_head/cow_head_set/csv_dir"
        self.res_path = 'D:/MyDownloads/cow_head/res'
        self.video_num = '03271042'

        # 默认显示参数
        self.pic_default_height = 180
        self.max_showing_pic_num = 5
        self.labeling_row_num = 0
        self.labeled_kind = 0

        # 全局参数
        self.showing_list = list()
        self.csv_list = list()

    def build_window(self):
        self.pic_=list()
        self.pic_.append(Label(self.root,text=''))
        self.pic_.append(Label(self.root,text=''))
        self.pic_.append(Label(self.root,text=''))
        self.pic_.append(Label(self.root,text=''))
        self.pic_.append(Label(self.root,text=''))

        self.but_=list()
        self.pic=list()
        self.but_.append(Button(self.root,text='',command=self.click1))
        self.but_.append(Button(self.root,text='',command=self.click2))
        self.but_.append(Button(self.root,text='',command=self.click3))
        self.but_.append(Button(self.root,text='',command=self.click4))
        self.but_.append(Button(self.root,text='',command=self.click5))

        for i in range(self.max_showing_pic_num):
            self.pic_[i].grid(row=0,column=i)
            self.but_[i].grid(row=1,column=i)

        self.pic_new=Label(self.root,text='new pic')
        self.btn_wrong=Button(self.root,text='错误类型',command=self.click_absnormal)
        self.btn_new=Button(self.root,text='新类型',command=self.click_new)
        self.pic_new.grid(row=2,sticky=E)
        self.btn_new.grid(row=3,column=1,sticky=E)
        self.btn_wrong.grid(row=3,column=0)

        self.but_save=Button(self.root,text='保存数据',command=self.csv_writer)
        self.but_save.grid(row=3,column=2,sticky=E)

        self.if_add_new=False

        self.but_re=Button(self.root,text='重标上一个',command=self.click_re)
        self.but_re.grid(row=3,column=3,sticky=E)

        self.init()

        self.root.mainloop()

if __name__=='__main__':
    visual_label=visual_label()
    visual_label.build_window()