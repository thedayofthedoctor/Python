#coding: utf-8

#lib-list
import os
import time
import requests as re
import urllib as ul
from selenium import webdriver as webd

#drfine-vari

#define-function
def fun_dir_make(para_path):
    if not os.path.exists(para_path):
        os.mkdir(para_path)

def fun_pic_deco(para_urls):
    url_gain=para_urls.split('=')[1]
    url_cont=url_gain.replace('&wapif','')
    url_deco=ul.parse.unquote(url_cont)
    return url_deco

def fun_pic_save(urls_deco,para_path,numb_page):
    pic_data=re.get(urls_deco).content
    pic_path=para_path+'/'+numb_page+'.jpg'
    pic_file=open(pic_path,'wb+')
    pic_file.write(pic_data)
    pic_file.close()

def fun_get_urls(inpt_urls):
    url_list=[]
    url_fina=[]
    get_driv=webd.Chrome()
    get_driv.get(inpt_urls)
    who_titl=get_driv.title
    com_titl=who_titl.split('-')[0].replace('免费漫画','')
    com_list=get_driv.find_elements_by_tag_name('li')
    print(str('漫画名:《'+str(com_titl)+'》'))
    print(str('共发现:'+str(len(com_list))+'个链接.'))
    for unit in com_list:
        com_link=unit.find_elements_by_tag_name('a');
        for link in com_link:
            url_list.append(link.get_attribute('href'))
    get_driv.quit()
    pro_comi=dict(name=com_titl,urls=url_list)
    off_none=list(filter(None,pro_comi['urls']))
    for urls in off_none:
        if inpt_urls in urls:
            url_fina.append(urls)
    pro_comi['urls']=url_fina
    print(str('经过筛选共有:'+str(len(pro_comi['urls']))+'个链接.'))
    return pro_comi

def fun_get_pict(proc_comi):
    lst_link=proc_comi['urls']
    lst_name=proc_comi['name']
    chr_opti=webd.ChromeOptions()
    prefs={'profile.managed_default_content_settings.images':2}
    chr_opti.add_experimental_option('prefs', prefs)
    get_driv=webd.Chrome(options=chr_opti)
    chp_numb=len(lst_link)
    num_link=0
    stt_time=time.time()
    for link in lst_link:
        num_link+=1
        get_driv.get(link)
        get_driv.implicitly_wait(5)
        chp_titl=get_driv.title.split('-')[0]
        par_titl=chp_titl.replace(' ','')
        num_page=int(get_driv.find_element_by_xpath('//span[@id="k_total"]').text)
        fil_path='C:/ⅠComprehensive/01.项目/Program/Comic/'+lst_name
        pic_path=fil_path+'/'+par_titl
        fun_dir_make(fil_path)
        fun_dir_make(pic_path)
        sta_time=time.time()
        str_chip=str('当前章节:'+str(par_titl)+'，共:'+str(num_page)+'页.')
        print(str_chip)
        for crnt in range(1,num_page+1):
            pic_urls=get_driv.find_element_by_id('qTcms_pic').get_attribute('src')
            str_time=time.time()
            url_deco=fun_pic_deco(pic_urls)
            fun_pic_save(url_deco,pic_path,str(crnt))
            end_time=time.time()
            fll_time=str(format(end_time-str_time,'.3f'))+'秒.'
            str_cipe=str('当前章节已下载'+str(crnt)+'/'+str(num_page)+',用时:'+fll_time)
            print(str_cipe)
            if crnt < num_page:
                ord_link=crnt+1
                nex_link=link+'?p='+str(ord_link)
                get_driv.get(nex_link)
            else:
                break
        enn_time=time.time()
        fia_time='用时:'+str(format(enn_time-sta_time,'.3f'))+'秒.'
        now_numb=str(num_link)+'/'+str(chp_numb)+','
        str_prno='当前章节下载完毕，目前进度:'+now_numb+fia_time
        print(str_prno)
    get_driv.quit()
    enm_time=time.time()
    fil_time=str(format(enm_time-stt_time,'.3f'))+'秒.'
    print(str('所有章节下载完毕,总共用时:'+fil_time))


def main():
    print('开始爬取.')
    url_comi='http://m.manhuaju.com/xiaoyuan/zuoyugongcun/'
    pic_comi=fun_get_urls(url_comi)
    fun_get_pict(pic_comi)

#main
if __name__ == '__main__':
    main()
