#coding:utf-8

#import-liblist
import os
import sys
import time
import shutil as st
import urllib as ul
import requests as re
from selenium import webdriver as webd

#define-set

#define-list
url_list=[]
lis_link=[]
#define-class

#define-function
def fun_dir_make(crea_path):#函数-创建路径，如存在则不重复创建.
    if not os.path.exists(crea_path):
        os.mkdir(crea_path)

def fun_ope_chwp(open_link):#创建Chrome项目，准备无界面打开网页.
    chr_opti=webd.ChromeOptions()
    chr_opti.add_argument(cfg_head)
    chr_opti.add_argument(cfg_ugpu)
    chr_opti.add_experimental_option('prefs',dic_cfg_pref)
    get_chwp=webd.Chrome(options=chr_opti)
    get_chwp.get(open_link)
    get_chwp.implicitly_wait(5)
    return get_chwp
    
def fun_get_titl(open_chwp,inpt_link):#获得作品标题，总页码，并根据网站区分标题行写法.
    who_titl=open_chwp.title
    sep_link=inpt_link.split('.')[1]
    if sep_link == 'iimanhua':
        rel_titl=who_titl.split(' ')[0].replace('漫画','')
        tit_list=who_titl.split(' ')
        if len(tit_list) > 4:
            chp_name=who_title.replace(tit_list[0],'').replace(tit_list[-1],'').replace(tit_list[-2],'').replace(' ','-')
            chp_page=0
        else:
            chp_name=str(tit_list[1])
            chp_page=int((open_chwp.find_element_by_class_name('manga-page').text).split('/')[1].replace('P',''))
    elif sep_link == 'manhuaju':
        jdg_link=inpt_link.split('/')[-1]
        if jdg_link == '':
            rel_titl=who.titl.split('-')[0].replace('免费漫画','')
            chp_name=''
            chp_page=0
        else:
            rel_titl=who.title.split('-')[1].replace(' ','')
            chp_name=who.title.split('-')[0].replace(' ','-')
            chp_page=int(get_driv.find_element_by_xpath('//span[@id="k_total"]').text)
    dic_com_name=dict(titl=rel_titl,chap=chp_name,page=chp_page)
    return dic_com_name
        
def fun_get_link(open_chwp,inpt_link):#获取全部章节连接，并记录在列表内，同时返回两个列表用于统计数据.
    chp_list=open_chwp.find_elements_by_tag_name('li')
    for unit in chp_list:
        chp_link=unit.find_elements_by_tag_name('a')
        for link in chp_link:
            url_true=link.get_attribute('href')
            url_list.append(url_true)
            open_chwp.close()
    off_none=list(filter(None,url_list))
    for link in off_none:
        if inpt_link in link:
            lis_link.append(link)
    dic_chp_link=dict(befo=off_none,afte=lis_link)
    return dic_chp_link

def fun_get_urls(inpt_link):#整理全部章节连接，显示章节数目以及爬虫记录.
    get_chwp=fun_ope_chwp(inpt_link)
    dic_com_name=fun_get_titl(get_chwp,inpt_link)
    dic_chp_link=fun_get_link(get_chwp,inpt_link)
    com_titl=dic_com_name['titl']
    num_urls=len(dic_chp_link['befo'])
    num_link=len(dic_chp_link['afte'])
    str_coti='漫画名:《'+str(com_titl)+'》'
    str_urls='共发现:'+num_urls+'个链接.'
    str_link='经筛选有:'+num_link+'个链接符合要求.'
    print(str_coti+'\n'+str_urls+'\n'+str_link)
    dic_com_link=dict(name=com_titl,link=dic_chp_link['afte'])
    return dic_com_link

def fun_pic_deco(para_urls):
    url_gain=para_urls.split('=')[1]
    url_cont=url_gain.replace('&wapif','')
    url_deco=ul.parse.unquote(url_cont)
    return url_deco

def fun_img_info(open_chwp,comi_link):
    jdg_link=comi_link.split('.')[1]
    if jdg_link == 'iimanhua':
        pic_link=open_chwp.find_element_by_xpath('//div[@id="manga"]/img').get_attribute('src')
    elif jdg_link == 'manhuaju':
        url_enco=open_chwp.find_element_by_id('qTcms_pic').get_attribute('src')
        pic_link=fun_pic_deco(url_enco)
    return pic_link

def fun_cra_path(file_path,dict_name):
    pic_fold=file_path+dict_name['chap']
    fun_dir_make(pic_fold)
    return pic_fold

def fun_get_chp(dict_link):
    com_name=dict_link['name']
    lst_link=dict_link['link']
    doc_path=sto_path+com_name+'/'
    fun_dir_make(doc_path)
    num_chap=len(lst_link)
    for link in lst_link:
        dig_para += 1
        get_driv=fun_ope_chwp(link)
        sst_time=time.time()
        dic_com_name=fun_get_titl(get_driv,link)
        pic_fold=fun_cra_path(doc_path,dic_com_name)
        chp_titl,num_page=dic_com_name['chap'],dic_com_name['page']
        str_chip='当前章节:'+chp_titl+',共:'+str(num_page)+'页.'
        print(str_chip)
        for crnt in range(1,num_page+1):
            pst_time=time.time()
            pic_link=fun_img_info(get_driv,link)
            fun_pic_save(pic_link,pic_fold,str(crnt))
            ped_time=time.time()
            ptt_time=format(ped_time-pst_time,'.3f')
            str_pict='当前章节已下载'+str(crnt)+'/'+str(num_page)+',用时:'+ptt_time+'秒.'
            print(str_pict)
            if crnt < num_page+1:
                ord_link=crnt+1
                url_para=link.split('.')[1]
                nex_link=link+dic_jdg_link[url_para]+str(ord_link)
                get_driv.get(nex_link)
            else:
                break
        get_driv.close()
        sed_time=time.time()
        stt_time=format(set_time-sst_time,'.3f')
        str_page=str(dig_para)+'/'+str(num_chap)
        str_chap='当前章节下载完毕.'+str_page+',用时:'+stt_time+'秒.'
        print(str_chap)
    get_driv.quit()
def fun_pic_save(imag_link,para_path,numb_page):
    pic_data=re.get(imag_link).content
    pic_path=para_path+'/'+numb_page+'.jpg'
    pic_file=open(pic_path,'wb+')
    pic_file.write(pic_data)
    pic_file.close()

def fun_spe_func():
    ''
def fun_prg_main():
    cst_time=time.time()
    print('开始爬取.')
    dic_com_link=fun_get_urls(com_link)
    fun_get_imag(dic_com_link)
    ced_time=time.time()
    ctt_time=format(ced_time-cst_time,'.3f')
    str_summ='所有章节下载完毕,总共用时:'+ctt_time+'秒.'
    print(str_summ)

#define-variable
dig_para=0
cfg_head='--headless'
cfg_ugpu='--disable-gpu'
com_link='http://m.iimanhua.com/comic/497/'
sto_path='C:/ⅠComprehensive/01.项目/Program/Comic/'

#define-dictionary
dic_cfg_pref={'profile.managed_default_content_settings.images':2}
dic_jdg_link={'manhuaju':'?p=','iimanhua':'?af='}

#main

if __name__ == '__main__':
    fun_prg_main()
