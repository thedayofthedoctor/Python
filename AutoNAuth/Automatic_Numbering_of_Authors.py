#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
THIS FILE IS PART OF NETWORK FOR MWAFU LIBRARY LOVE BOOK STORE BY MATT BELFAST BROWN
Automatic numbering of authors.py - The core part of the Author Number Creation.

Author: Matt Belfast Brown 
Creat Date:2021-05-29
Version:1.0.0-official

THIS PROGRAM IS FREE FOR EVERYONE,IS LICENSED UNDER GPL-3.0
YOU SHOULD HAVE RECEIVED A COPY OF GPL-3.0 LICENSE.

Copyright (C) 2021  Matt Belfast Brown
Copyright (C) 2021  MWAFU LIBRARY LOVE BOOK STORE

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


'''
import pypinyin as pn
import auto_AUTHNumber as aan
import PySimpleGUI as sg
#define-var
sg.theme('SystemDefaultForReal')
layprinta=[
    [sg.Text('本工具针对自动著者号生成开发\n使用时输入著者姓名即可获得双向对照信息。\n初版日期：2021-05-29，\n版本日期：2021-05-31，版本号：1.0.0-official\nAutomatic Numbering of Authors  Copyright (C) 2021  Matt Belfast Brown')],
    [sg.Text('请输入责任者姓名：'),sg.Input(key='serch'),sg.Btn('提交查询',key='handin')]
    ]
fun_make_pron=aan.make_pronouncation
fun_fetc_code=aan.fetchcode

def fun_take_resl(auth_name):
    list_resl=fun_make_pron(auth_name)
    surn_name=list_resl[2]
    last_name=list_resl[3]
    if len(list_resl[0][0]) ==1:
        if len(list_resl[1][0])==1:
            last_code=fun_fetc_code(surn_name,list_resl[1][0][0].upper())
        else:
            layprintc=[
                [sg.Text('您所输入的姓名含有多音字请您选择读音首字母。')],
                [sg.Text('著者姓氏：'+surn_name),sg.Text('著者名字：'+last_name+'，读音首字母为：'),sg.Combo (list_resl[1][0],key='FC'),sg.Btn('提交查询',key='handon')]
                ]
            windowb=sg.Window('请选择读音',layout=layprintc,finalize=True,font=("华文中宋", 15),icon='ANA.ico')
            eventb,valueb=windowb.Read()
            if eventb == 'handon':
                pron_fscr=valueb['FC'].upper()
                if pron_fscr =='':
                    last_code='请重新输入'
                else:
                    last_code=fun_fetc_code(surn_name,pron_fscr)
                windowb.close()
        fist_char=list_resl[0][0][0].upper()
    else:
        if len(list_resl[1][0])==1:
            layprintc=[
                [sg.Text('您所输入的姓名含有多音字请您选择读音首字母。')],
                [sg.Text('著者姓氏：'+surn_name+'，读音首字母为：'),sg.Combo (list_resl[0][0],key='FCF'),sg.Text('著者名字：'+last_name),sg.Btn('提交查询',key='handon')]
                ]
            windowb=sg.Window('请选择读音',layout=layprintc,finalize=True,font=("华文中宋", 15),icon='ANA.ico')
            pron_fscr=list_resl[1][0][0].upper()
            eventb,valueb=windowb.Read()
            if eventb == 'handon':
                pron_surn=valueb['FCF']
                if surn_name not in ['曾','查']:
                    last_code=fun_fetc_code(surn_name,pron_fscr)
                else:
                    if surn_name =='曾':
                        if pron_surn=='c':
                            last_code=fun_fetc_code('曾c',pron_fscr)
                        else:
                            last_code=fun_fetc_code(surn_name,pron_fscr)
                    else:
                        if pron_surn=='c':
                            last_code=fun_fetc_code('查c',pron_fscr)
                        else:
                            last_code=fun_fetc_code(surn_name,pron_fscr)
                windowb.close()
        else:
            layprintc=[
                [sg.Text('您所输入的姓名含有多音字请您选择读音首字母。')],
                [sg.Text('著者姓氏：'+surn_name+'，读音首字母为：'),sg.Combo (list_resl[0][0],key='FCF'),sg.Text('著者名字：'+last_name+'，读音首字母为：'),sg.Combo (list_resl[1][0],key='FCL'),sg.Btn('提交查询',key='handon')]
                ]
            windowb=sg.Window('请选择读音',layout=layprintc,finalize=True,font=("华文中宋", 15),icon='ANA.ico')
            eventb,valueb=windowb.Read()
            if eventb == 'handon':
                pron_surn=valueb['FCF']
                pron_fscr=valueb['FCL'].upper()
                if surn_name not in ['曾','查']:
                    last_code=fun_fetc_code(surn_name,pron_fscr)
                else:
                    if surn_name =='曾':
                        if pron_surn=='c':
                            last_code=fun_fetc_code('曾c',pron_fscr)
                        else:
                            last_code=fun_fetc_code(surn_name,pron_fscr)
                    else:
                        if pron_surn=='c':
                            last_code=fun_fetc_code('查c',pron_fscr)
                        else:
                            last_code=fun_fetc_code(surn_name,pron_fscr)
                windowb.close()
        fist_char=pron_surn.upper()
    auth_code=fist_char+last_code
    return [auth_name,auth_code,surn_name,last_name]

windowa=sg.Window('著者号自动生成工具',layout=layprinta,finalize=True,font=("华文中宋", 15),icon='ANA.ico')
while True:
    event,value=windowa.Read()
    if event == 'handin':
        auth_name=value['serch']
        result=fun_take_resl(auth_name)
        layprintb='您输入的著者全名为：'+result[0]+'。\n经搜索拆分为，姓氏（或代姓氏）：'+result[2]+'，名字（或代名字）：'+result[3]+'。\n得到著者号为：'+result[1]+'。'
        sg.popup(layprintb,title='结果',font=('华文中宋',15),icon='ANA.ico')
    if event == sg.WIN_CLOSED:
        break
