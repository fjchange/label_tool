#coding=utf-8
'''
本程序的目标在于将多个标记文件中的标记进行差异找出来，然后进行额外的标记处理
主要涉及的问题有：
1. 本应同一类的，被误标为其他类
2. 错误新增了一类
3. 错误的将不是同一类的合并在一起
4. 图片是否真的为异常（一般如果一个判定为异常，就把它记作异常
5. 如果依旧存在无法辨别的，将会移到hard范畴内
'''
import random
from tkinter import *
from PIL import Image,ImageTk
import os

#-------------------------参数配置---------------------------------------------
img_path_pre='/home/shikigan/res/'
csv_src_path_pre='/home/shikigan/kiwi_fung/csv_dir/'
csv_tar_path_pre=''
csv_name=''
csv_paths=[csv_src_path_pre+csv_name+'.csv',csv_tar_path_pre+csv_name+'.csv']
#-----------------------------------------------------------------------------

#首先获取两个csv文件，并将之以list的形式存放
#并产生以图片序号作为key的字典
def csv_solver(path):
    with open(path)as c:
        labels_lists=[]
        label_dict={}
        fault_list=[]
        lines=c.readlines()
        row_max_index=0
        for line in lines:
            line_list=line.split(',')
            line_list[-1]=line_list[-1].split('\n')[0]
            if int(line_list[-1])==-1:fault_list.append(line_list[-1])
            elif int(line_list[-1])>row_max_index:
                row_max_index+=1
                labels_lists.append([line_list[-2]])
            else:
                labels_lists[int(line_list[-1])].append(line_list[-2])
            label_dict[line_list[-2]]=[line_list[-1]]
    return labels_lists,label_dict

def match(csv_paths):
    '''

    :param csv_paths: a pair of csv_path
    :return: the output results after human interception
    '''
    #获得的是 以标记为顺序的list，标记为错误的图片list，
    src_lists,src_label_dict=csv_solver(csv_paths[0])
    target_list,tar_label_dict=csv_solver(csv_paths[1])

    src_row_ind,tar_row_ind=0,0

    real_output_dict={}
    real_label_dict={}
    real_index=0
    #为[4,x]的大小，搜索上下四次是否为对应的标记
    waitting_lists=[]

    hard_set=[]

    while(1):
        interception,differ_src,differ_tar=get_interception(src_lists[src_row_ind],target_list[tar_row_ind])

        if interception!=None:
            #当交集不为空的时候，就是存在公共承认的部分，从interception中选取一个图片当作common_acknowledge_img
            #然后对于differ的图片与common进行比较
            real_output_dict[real_index]=interception
            for item in interception:
                real_label_dict[item]=real_index
            common_ack_img=img_path_pre+csv_name+'/'+get_random_item(interception)+'.jpg'
            #differ_src and differ_tar generate two results
            real_output_dict, real_label_dict, temp_waitting_list=matching_process(differ_src,tar_label_dict,real_output_dict,real_index,real_label_dict,common_ack_img)
            real_output_dict, real_label_dict,_waitting_list=matching_process(differ_tar,src_label_dict,real_output_dict,real_index,real_label_dict,common_ack_img)

            temp_waitting_list=temp_waitting_list+_waitting_list

            if len(waitting_lists)!=4 or (src_row_ind==len(src_lists) and tar_row_ind==len(target_list)):
                _waitting_list=waitting_lists.pop(0)
                real_output_dict,real_label_dict,_=matching_process(_waitting_list,tar_label_dict,real_output_dict,real_index,real_label_dict)
                hard_set = hard_set + _
            #如果还不是的话，将会对_放入hard里面
            waitting_lists.append(temp_waitting_list)

            tar_row_ind+=1
            src_row_ind+=1
            real_index += 1
            real_output_dict[real_index] = []

        #如果a交b为空，那么意味着其中有错标新增类，或者是两者的序号没有合理的增长
        #那么就需要对a-&b a+&b ,b-&a,b+&a进行判断，按照交集的数量多少进行排序
        else:
            #如果两个index都不是0的话
            max_len,max_index=0,0
            inters=[]
            bias=[[-1,0],
                  #[1,0],
                  [0,-1],
                  #[0,1]
                  ]
            if src_row_ind and tar_row_ind:
                for i in range(len(bias)):
                    inters.append([get_interception(src_lists[src_row_ind+bias[i][0]],target_list[tar_row_ind+bias[i][1]])])
                    if len(inters[i][0])>=max_len:
                        max_len=len(inters[i][0])
                        max_index=i
                #如果为0,3意味着src标记多一类，1,2意味着tar多标记一类
                if max_len==0:
                    print("标记文件存在严重错误！为src中的%d类与tar中的%d类"%(src_row_ind,tar_row_ind))
                    exit()

                #对于过多位置情况难以覆盖的问题






def matching_process(differ_set,other_dict,real_dict,real_index,real_label_dict,common_ack_img=None):
    #status 用来避免递归的发生
    temp_waitting_list=[]
    for item in differ_set:
        #避免多余的交互
        if item in real_label_dict.keys():
            continue
        elif other_dict[item] == -1:
            # 如果不同的标记的图片被标记为错误，目前操作是直接置之为错误
            if -1 in real_dict.keys():
                real_dict[-1].append(item)
            else:
                real_dict[-1] = [item]
            real_label_dict[item]=-1
        else:
            result=human_interaction(item,real_dict,real_index,common_ack_img)
            real_dict, real_label_dict, temp_waitting_list=result_processing(result,real_dict,item,real_label_dict,real_index,temp_waitting_list)
        return real_dict,real_label_dict,temp_waitting_list

def result_processing(result,real_dict,item,real_label_dict,real_index,temp_waitting_list):
    if result == -1:
        if -1 in real_dict.keys():
            real_dict[-1].append(item)
        else:
            real_dict[-1] = [item]
        real_label_dict[item] = -1
    elif result == -2:
        temp_waitting_list.append(item)
    elif result == 0:
        real_dict[real_index].append(item)
        real_label_dict[item] = real_index
    else:
        real_dict[real_index - 5 + result].append(item)
        real_label_dict[item] = real_index - 5 + result
    return real_dict,real_label_dict,temp_waitting_list

def get_common_ack_img(interception):
    return interception[int(random.random()*len(interception))]
#获取交集与差集
def get_interception(source_set,target_set):
    '''
    :param source_set:
    :param target_set:
    :return: the inception and two differences
    '''

    source_set=set(source_set)
    target_set=set(target_set)

    inter=source_set&target_set
    differ_s=source_set-target_set
    differ_t=target_set-source_set

    union=source_set|target_set
    print('the Jaccard Distance of two set is :%f'%(len(inter)/len(union)))

    return list(inter),list(differ_s),list(differ_t)

def human_interaction(wrong_img,real_dict,real_index,common_ack_img=None):
    wrong_img=img_path_pre + csv_name + '/' + wrong_img + '.jpg'

    interface=interaction(wrong_img,real_dict,real_index,common_ack_img)
    return interface.get_state()

def get_random_item(list):
    return list[int(random.random()*len(list))]

class interaction():
    def __init__(self,wrong_img,real_dict,real_index,common_ack_img=None):
        self.root=Tk()
        self.root.geometry('1920x1080')
        self.root.title("label_wash.v0.1")

        self.but_common=Button(self.root,text='Common_acknowledged_img',command=self.click_right)
        self.but_common.grid(row=0,column=0,sticky=E)
        if common_ack_img!=None:
            jpg=Image.open(common_ack_img)
            self.com_jpg=ImageTk.PhotoImage(jpg)
            self.but_common.configure(image=self.com_jpg)
        self.but_cate_=[]
        self.but_cate_.append(Button(self.root,text='',command=self.click_1))
        self.but_cate_.append(Button(self.root,text='',command=self.click_2))
        self.but_cate_.append(Button(self.root,text='',command=self.click_3))
        self.but_cate_.append(Button(self.root,text='',command=self.click_4))

        for i in range(4):
            self.but_cate_[i].grid(row=0,column=i+1,sticky=E)

        self.but_wrong=Button(self.root,text='错误类型',command=self.click_wrong)
        self.but_wrong.grid(row=1, column=1, sticky=E)
        self.but_not=Button(self.root,text='不在以上类别',command=self.click_not)
        self.but_not.grid(row=1, column=2, sticky=E)

        self.pic_differ=Label(self.root,text='')
        self.pic_differ.grid(row=1,column=0,sticky=E)
        jpg=Image.open(wrong_img)
        self.pic_dif=ImageTk.PhotoImage(jpg)
        self.pic_differ.configure(image=self.pic_dif)
        #如果不在前后两个，那么会被自动标记为难以辨别类型

        self.pic_=[]
        if real_index<4:
            for i in range(real_index):
                jpg_name = get_random_item(real_dict[i])
                jpg = Image.open(img_path_pre + csv_name + '/' + jpg_name + '.jpg')
                self.pic_.append(ImageTk.PhotoImage(image=jpg))
                self.but_cate_[i].configure(image=self.pic_[i])
        else:
            for i in range(4):
                jpg_name = get_random_item(real_dict[real_index-4+i])
                jpg = Image.open(img_path_pre + csv_name + '/' + jpg_name + '.jpg')
                self.pic_.append(ImageTk.PhotoImage(image=jpg))
                self.but_cate_[i].configure(image=self.pic_[i])

        self.state=None

    def click_wrong(self):
        self.state=-1
        self.root.destroy()

    def click_not(self):
        self.state=-2
        self.root.destroy()

    def click_right(self):
        self.state=0
        self.root.destroy()

    def click_1(self):
        self.state=1
        self.root.destroy()

    def click_2(self):
        self.state=2
        self.root.destroy()

    def click_3(self):
        self.state=3
        self.root.destroy()

    def click_4(self):
        self.state=4
        self.root.destroy()

    def get_state(self):
        return self.state
