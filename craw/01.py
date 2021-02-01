import requests
from selenium import webdriver as webd
import os


def fun_ope_chwp(inpt_link):
    chr_opti=webd.ChromeOptions()
    chr_opti.add_experimental_option('prefs',set_pref)
    chr_opti.add_argument(set_hdle)
    chr_opti.add_argument(set_hdgp)
    ope_chro=webd.Chrome(options=chr_opti)
    ope_chro.get(inpt_link)
    ope_chro.implicitly_wait(1)
    ope_chro.close()


def fun_get_urls(inpt_urls):
    url_list=[]
    url_fina=[]
    get_driv=webd.Chrome()
    get_driv.get(inpt_urls)
    num_page=int((get_driv.find_element_by_class_name('manga-page').text).split('/')[1].replace('P',''))
    pic_urls=get_driv.find_element_by_xpath('//div[@id="manga"]/img')
    pig_runs=pic_urls.get_attribute('src')
    print(num_page,pic_urls,pig_runs)
    get_driv.close()
set_pref={'profile.managed_default_content_settings.images':2}
set_hdle='--headless'
set_hdgp='--disable-gpu'
ipt_urls='http://m.iimanhua.com/comic/497/623778.html'
#fun_get_urls(ipt_urls)
fun_ope_chwp(ipt_urls)

