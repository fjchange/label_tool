#coding=utf-8
from tkinter import *
from PIL import Image,ImageTk
import csv

def csv_solver(path):
    '''

    :param path:
    :return: path_dict: key是类序号，value是对应类下面的路径list
    '''
    with open(path)as c:
        path_dict={}
        lines=c.readlines()
        for line in lines:
            line_list=line.split(',')
            line_list[-1]=line_list[-1].split('\n')[0]
            if line_list[-1]=='' or int(line_list[-1])==-1:
                continue
            if int(line_list[-1])in path_dict.keys():
                path_dict[int(line_list[-1])].append(line_list[2])
            else:
                path_dict[int(line_list[-1])]=[line_list[2]]
    return path_dict

#弹窗类，用于显示截图的源视频图片
class PopupDialog():
    def __init__(self,parent,src_img_path):
        self.parent = parent
        self.top=Toplevel(self.parent)

        self.src_img_label=Label(self.top)
        self.src_img_label.pack(side='top')
        src_img=Image.open(src_img_path)
        self.jpg=ImageTk.PhotoImage(src_img)
        self.src_img_label.configure(image=self.jpg)
        #关闭键
        self.but_ok=Button(self.top,text='OK',command=self.ok)
        self.but_ok.pack(side='bottom')
        self.top.bind("<Key>",self.ok)
    #按键即关闭窗口，需关闭才能够在主窗口继续操作
    def ok(self,event=None):
        self.top.destroy()

#主窗口
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
    #5个候选按键的实现部分
    def click(self,i):
        #显示的对应图片替换为我们新的图片
        self.showing_list[i][0]=self.csv_list[self.labeling_row_num][2]
        self.csv_list[self.labeling_row_num].append(self.showing_list[i][1])
        self.dict[self.showing_list[i][1]].append(self.showing_list[i][0])
        #当前检测的行数加一
        self.labeling_row_num+=1
        #更新图片
        self.image_set()
        #用于回退使用的更新判断bool
        self.if_add_new=False

    def click1(self,event=None):
        self.click(0)
    def click2(self,event=None):
        self.click(1)
    def click3(self,event=None):
        self.click(2)
    def click4(self,event=None):
        self.click(3)
    def click5(self,event=None):
        self.click(4)

    #初始化，读取csv，产生分类dict，如果是重新开始的话会设置reset
    def init(self):
        self.csv_reader()
        self.dict=csv_solver(self.csv_path+'/'+self.video_num+'.csv')
        self.reset()
        #self.image_set()

    #按击新类型
    def click_new(self,event=None):
        #判断当前展示的图片有多少张，若为五张
        self.if_add_new = True
        self.labeled_kind+=1
        if len(self.showing_list)==5:
            self.replaced=self.showing_list.pop(0)
            self.showing_list.append([self.csv_list[self.labeling_row_num][2],self.labeled_kind])
            self.csv_list[self.labeling_row_num].append(self.labeled_kind)
        else:
            self.csv_list[self.labeling_row_num].append(self.labeled_kind)
            self.showing_list.append([self.csv_list[self.labeling_row_num][2],self.labeled_kind])
        self.dict[self.labeled_kind]=[self.showing_list[-1][0]]
        self.labeling_row_num+=1
        self.image_set()

    def click_absnormal(self,event=None):
        self.csv_list[self.labeling_row_num].append(-1)

        self.labeling_row_num+=1
        self.image_set()

    #重标上一张按钮的功能实现
    def  click_re(self,event=None):
        #当前标记的行号回退，行号指示的是为标记的
        self.labeling_row_num-=1
        #删除上一个错误标记，并返回其标记的类号
        item=self.csv_list[self.labeling_row_num].pop()
        self.dict[item].pop()
        #如果新增的类，并且待选择有5个
        if self.if_add_new and self.labeled_kind>5:
            #总类数减一
            self.labeled_kind-=1
            #待选择的列表剔除错误新增的部分
            self.showing_list.pop()
            #然后将原来被踢出的图片重新插回
            self.showing_list.insert(0,self.replaced)
        elif self.if_add_new or self.dict[item]==[]:
            #如果棕待选择不足5个，那么需要显示为空
            self.labeled_kind-=1
            self.showing_list.pop()
            self.pic[item-1]=None
            self.pic_[item-1].configure(text='')
            self.but_[item-1].configure(image=self.pic[item-1])
        elif len(self.showing_list)==5:
            #如果是替换了某一个类的显示图片，那么提出该图片，并且更换一张
            self.showing_list[item-(self.labeled_kind-4)]=[self.dict[item][-1],item]
        else:
            #如果未足5张又更换了某一个类的图片
            for i in range(1,self.labeled_kind):
                self.showing_list[i]=[self.dict[i][-1],i]
        self.image_set()
        self.if_add_new=False
        self.replaced=None

    def image_set(self):

        if self.labeled_kind==0:
            pass
            '''
            self.csv_list[0].append(0)

            self.labeling_row_num+=1
            self.showing_list.append([self.csv_list[0][2].replace('\'',""),self.labeled_kind])
            self.labeled_kind+=1
            return self.image_set()
            '''
        elif self.labeled_kind<=4 and self.labeled_kind>0:
            for i in range(self.labeled_kind):
                jpg=Image.open(self.res_path+'/'+self.video_num+'/'+self.showing_list[i][0]+'.jpg')
                if i<len(self.pic):
                    self.pic[i]=ImageTk.PhotoImage(jpg)
                else:
                    self.pic.append(ImageTk.PhotoImage(jpg))
                self.but_[i].configure(image=self.pic[i])
                self.pic_[i].configure(text=self.showing_list[i][1].__str__())

        else :
            for i in range(5):
                jpg=Image.open(self.res_path+'/'+self.video_num+'/'+self.showing_list[i][0]+'.jpg')
                if i<len(self.pic):
                    self.pic[i]=ImageTk.PhotoImage(jpg)
                else:
                    self.pic.append(ImageTk.PhotoImage(jpg))
                self.but_[i].configure(image=self.pic[i])
                self.pic_[i].configure(text=self.showing_list[i][1].__str__())

        if self.labeling_row_num<len(self.csv_list):
            jpg=Image.open(self.res_path+'/'+self.video_num+'/'+self.csv_list[self.labeling_row_num][2].__str__()+'.jpg')
            self.pic_n = ImageTk.PhotoImage(jpg)
            self.pic_new.configure(image=self.pic_n)
            self.img_path.set('\t'+self.res_path+'/'+self.video_num+'/'+self.csv_list[self.labeling_row_num][2].__str__()+'.jpg')
            self.row_index.set('\t'+str(self.labeling_row_num)+'/'+str(len(self.csv_list)))
            self.windows.update()
        else:
            self.csv_writer()

        if self.labeling_row_num:
            self.csv_writer()
        percent=round(self.labeling_row_num/len(self.csv_list),4)
        self.percentage_bar.coords(self.fill_rec,(5,5,6+percent*100,25))
        self.percentage.set(str(percent*100)+'%')
        if percent==100.00:
            self.percentage.set('完成')
        self.windows.update()

    def __init__(self):
        self.windows = Tk()

        self.windows.title('label_cow_head')
        self.windows.geometry('1920x1080')

        self.root=Frame(self.windows).grid(row=0,column=0)

        # 默认路径
        self.csv_path = "/home/shikigan/kiwi_fung/csv_dir"
        self.res_path = '/home/shikigan/res'
        self.src_img_path='/home/shikigan/cowphoto'
        self.video_num = '03241051'


        # 默认显示参数
        self.pic_default_height = 180
        self.max_showing_pic_num = 5
        #当前标记的那一行记录
        self.labeling_row_num = 0
        #当前标记的那一类型
        self.labeled_kind = 0

        # 全局参数
        self.showing_list = list()
        self.csv_list = list()
        self.pic=list()
        self.dict={}

    def reset(self):
        #即初始化位置发生改变，那么将读入该整个csv，然后在那个位置开始更换原有的显示
        if self.labeling_row_num!=0:
            num=min(len(self.dict.keys()),self.max_showing_pic_num)
            dict_list=sorted(self.dict.items(),key=lambda d:d[0],reverse=False)
            self.showing_list=[]
            dict_list=dict_list[-1*num:]
            for i in range(0,num):
                self.showing_list.append([dict_list[i][-1][-1],self.labeled_kind-num+i+1])
        self.image_set()

    def more_detail(self,event=None):
        src_img_path=self.src_img_path+'/'+self.csv_list[self.labeling_row_num][0].split('\'')[-1]+'/'+self.csv_list[self.labeling_row_num][1].split('\'')[-1]+'.jpg'
        pw=PopupDialog(self.windows,src_img_path)
        #等待弹窗关闭
        self.windows.wait_window(pw)

    def build_window(self):
        self.pic_=list()
        self.pic_.append(Label(self.root,text=''))
        self.pic_.append(Label(self.root,text=''))
        self.pic_.append(Label(self.root,text=''))
        self.pic_.append(Label(self.root,text=''))
        self.pic_.append(Label(self.root,text=''))

        self.but_=list()
        self.but_.append(Button(self.root,text='',command=self.click1))
        self.but_.append(Button(self.root,text='',command=self.click2))
        self.but_.append(Button(self.root,text='',command=self.click3))
        self.but_.append(Button(self.root,text='',command=self.click4))
        self.but_.append(Button(self.root,text='',command=self.click5))

        self.percentage_bar=Canvas(self.root,width=120,height=30,bg='white')
        self.percentage_bar.grid(row=3,column=0,sticky=E)

        self.percentage=StringVar()
        self.out_rec=self.percentage_bar.create_rectangle(5,5,105,25,outline='blue',width=1)
        self.fill_rec=self.percentage_bar.create_rectangle(5,5,5,25,outline='',width=0,fill='blue')
        self.percentage_degree_label=Label(self.root,textvariable=self.percentage).grid(row=3,column=1,sticky=E)
        self.img_path=StringVar()
        self.path_label=Label(self.root,textvariable=self.img_path).grid(row=3,column=3,sticky=E)
        self.row_index=StringVar()
        self.num_label=Label(self.root,textvariable=self.row_index).grid(row=3,column=2,sticky=E)
        for i in range(self.max_showing_pic_num):
            self.pic_[i].grid(row=1,column=i)
            self.but_[i].grid(row=0,column=i)

        self.pic_new=Label(self.root,text='new pic')
        self.btn_wrong=Button(self.root,text='错误类型',command=self.click_absnormal,width=5,height=3)
        self.btn_new=Button(self.root,text='新类型',command=self.click_new,width=5,height=3)
        self.pic_new.grid(row=2,column=0,sticky=E)
        self.btn_new.grid(row=2,column=1,sticky=E)
        self.btn_wrong.grid(row=2,column=2)

        #self.but_save=Button(self.root,text='保存数据',command=self.csv_writer)
        #self.but_save.grid(row=2,column=3,sticky=E)

        self.but_more_detail=Button(self.root,text='more',command=self.more_detail,width=5,height=3)
        self.but_more_detail.grid(row=2,column=4,sticky=E)



        '''
        快捷键设置部分，可以按照自己需要设定
        '''
        self.windows.bind("1",self.click1)
        self.windows.bind("2",self.click2)
        self.windows.bind("3",self.click3)
        self.windows.bind("4",self.click4)
        self.windows.bind("5",self.click5)
        #关于快捷键的设置可以参考：https://blog.csdn.net/bnanoou/article/details/38434443
        self.windows.bind("<Return>",self.click_new)#回车新的类
        self.windows.bind("<space>",self.click_absnormal)#空格错误类
        self.windows.bind("<Escape>",self.click_re)#Esc重标上一个
        self.windows.bind("<Tab>",self.more_detail)#Tab更多信息

        self.if_add_new=False

        self.but_re=Button(self.root,text='重标上一个',command=self.click_re,width=5,height=3)
        self.but_re.grid(row=2,column=3,sticky=E)

        self.init()

        mainloop()

if __name__=='__main__':
    visual_label=visual_label()
    visual_label.build_window()
