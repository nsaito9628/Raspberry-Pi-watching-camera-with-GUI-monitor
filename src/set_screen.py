#!/usr/bin/python
# -*- coding: utf-8 -*-
from typing import DefaultDict
import PySimpleGUI as sg
from datetime import datetime
import parameters as para


t_hour = [16, 10, 8, 6, 4]
st_hour = [0, 1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
mins = [0,1,2,3,4,5,6,7,8,9,10,11,12, 30,14, 30,16,17,18,19,20,21,
        22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
        41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59]

cam_type = ['webカメラ', '潜望鏡カメラ']
resols_webcam = ['176×144', '320×240', '640×480', '800×600', '1280×720']
resols_periscope = ['640×480', '1280×720']


class Gui:

    total_hr = para.total_hr
    total_min = para.total_min

    st_hr = para.st_hr
    st_min = para.st_min 
    end_hr = para.end_hr
    end_min = para.end_min

    thd = para.thd
    ratio = para.ratio

    EVENT = para.event   

    @classmethod
    def select_cam(cls):
        layout = [#[sg.MenuBar([['ファイル',['終了']]], key='menu1')],
                [sg.Text('カメラの選択', font=('HGｺﾞｼｯｸE', 35), background_color='#1F4F7B', pad=((250, 200),(0, 10)))],
                [sg.Listbox(cam_type, size=(15, len(cam_type)), default_values=cam_type[0], font=('HGｺﾞｼｯｸE', 25), pad=((0, 0),(0, 0)))],
                [sg.Button('次へ', key='next', font=('HGｺﾞｼｯｸE', 25)), sg.Button('中止', key='Quit', font=('HGｺﾞｼｯｸE', 25))]]

        window = sg.Window('カメラの選択', layout=layout, size=(800, 410), font=('HGｺﾞｼｯｸE', 30))#.Finalize()
        #window.Maximize()

        while True:
            event, values = window.read()
            print(event, values)

            if values[0][0] == cam_type[0]:
                para.cam_type = 0
                #print(str(values[0][0]), resols[i], para.res)
                para.event = event
                break
            elif values[0][0] == cam_type[1]:
                para.cam_type = 1
                #print(str(values[0][0]), resols[i], para.res)
                para.event = event
                break
            
            if (event in [None, 'Cancel']) or event == "Quit":# or event == sg.WIN_CLOSED or values['menu1']=='終了':
                para.event = event
                window.close()
                break

        window.close()  


    @classmethod
    def set_resolution(cls):
        
        if para.cam_type == 0:
            resols = resols_webcam
            default_val = 1
        elif para.cam_type == 1:
            resols = resols_periscope
            default_val = 0

        layout = [#[sg.MenuBar([['ファイル',['終了']]], key='menu1')],
                    [sg.Text('解像度設定', font=('HGｺﾞｼｯｸE', 35), background_color='#1F4F7B', pad=((265, 200),(0, 10)))],
                    [sg.Listbox(resols, size=(10, len(resols)), default_values=resols[default_val], font=('HGｺﾞｼｯｸE', 25), pad=((0, 0),(0, 0)))],
                    [sg.Button('次へ', key='next', font=('HGｺﾞｼｯｸE', 25)), sg.Button('中止', key='Quit', font=('HGｺﾞｼｯｸE', 25))]]

        window = sg.Window('解像度設定', layout=layout, size=(800, 410), font=('HGｺﾞｼｯｸE', 30))#.Finalize()
        #window.Maximize()

        while True:
            event, values = window.read()
            #print(event, values)

            for i in range(5):
                #print(i, str(values[0][0]), resols[i])            
                if values[0][0] == resols[i]:
                    para.res = i
                    #print(str(values[0][0]), resols[i], para.res)
                    break
            if (event in [None, 'Cancel']) or event == "Quit" or event == 'next':# or event == sg.WIN_CLOSED or values['menu1']=='終了':
                para.event = event
                window.close()
                break

        window.close()



    @classmethod
    def mode_select(cls):

        layout = [#[sg.MenuBar([['ファイル',['終了']]], key='menu1')],
                [sg.Text('録画方法選択', font=('HGｺﾞｼｯｸE', 35), background_color='#1F4F7B', pad=((250, 200),(0, 10)))],
                [sg.Button('連続録画', key='cont'), sg.Text('録画開始・終了時刻を入力', font=('HGｺﾞｼｯｸE', 30))],
                [sg.Button('ピンポイント録画', key='emr'), sg.Text('イベント前後を保存', font=('HGｺﾞｼｯｸE', 30))],
                [sg.Button('初期メニュー', key='init', font=('HGｺﾞｼｯｸE', 25)), sg.Button('中止', key='Quit', font=('HGｺﾞｼｯｸE', 25))]]

        window = sg.Window('録画方法選択', layout=layout, size=(800, 410), font=('HGｺﾞｼｯｸE', 30))#.Finalize()
        #window.Maximize()

        while True:
            event, values = window.read()

            #print(event, values)
            if (event in [None, 'Cancel']) or event == "Quit":# or event == sg.WIN_CLOSED or values['menu1']=='終了':
                window.close()
                break
            elif event == "cont" or event == "emr" or event == "init":
                window.close()
                para.event = event
                break

        window.close()


    @classmethod
    def input_totaltime(cls):

        for i in range(5):
            if i == para.res:
                tot_hour = t_hour[i]
                break

        layout = [#[sg.MenuBar([['ファイル',['終了']]], key='menu1')],
                [sg.Text('録画時間入力', font=('HGｺﾞｼｯｸE', 35), background_color='#1F4F7B', pad=((250, 200),(0, 10)))],
                [sg.Text('時間：', font=('HGｺﾞｼｯｸE', 30)), sg.Slider(range=(0, tot_hour), default_value=0, orientation='h')],
                [sg.Text('分　：', font=('HGｺﾞｼｯｸE', 30)), sg.Slider(range=(0, 59), default_value=2, orientation='h')], 
                [sg.Button('次へ', key='next', font=('HGｺﾞｼｯｸE', 25)),
                    sg.Button('初期メニュー', key='init', font=('HGｺﾞｼｯｸE', 25)),
                    sg.Button('中止', key='Quit', font=('HGｺﾞｼｯｸE', 25))]]

        window = sg.Window('連続録画時間入力', layout=layout, size=(800, 410), font=('HGｺﾞｼｯｸE', 30))#.Finalize()
        #window.Maximize()

        while True:
            event, values = window.read()

            #print(event, values)
            if (event in [None, 'Cancel']) or event == "Quit":# or event == sg.WIN_CLOSED or values['menu1']=='終了':
                window.close()
                break
            elif event == "init":
                window.close()
                para.event = event
                break
            elif event == 'next':
                para.total_hr = int(values[0])
                para.total_min = int(values[1])
                #print(para.total_hr, para.total_min)
                window.close()
                para.event = event
                break

        window.close()


    @classmethod
    def select_startmethod(cls):

        layout1 = [#[sg.MenuBar([['ファイル',['終了']]], key='menu1')],
                [sg.Text('録画方法', font=('HGｺﾞｼｯｸE', 35), background_color='#1F4F7B', pad=((295, 200),(0, 10)))],
                [sg.Button('今すぐスタート', key='rapid', font=('HGｺﾞｼｯｸE', 25)),
                    sg.Button('開始時刻指定', key='spec', font=('HGｺﾞｼｯｸE', 25))],
                [sg.Button('初期メニュー', key='init', font=('HGｺﾞｼｯｸE', 25)),
                    sg.Button('中止', key='Quit', font=('HGｺﾞｼｯｸE', 25))]]

        window = sg.Window('スタート方法選択', layout=layout1, size=(800, 410), font=('HGｺﾞｼｯｸE', 30))#.Finalize()
        #window.Maximize()

        while True:
            event, values = window.read()

            #print(event, values)
            if (event in [None, 'Cancel']) or event == "Quit":# or event == sg.WIN_CLOSED or values['menu1']=='終了':
                window.close()
                break
            elif event == "init" or event == 'rapid' or event == 'spec':
                #window.close()
                para.event = event
                break

        window.close()


    @classmethod
    def set_rapid_start(cls):

        now = datetime.now()
        para.st_hr = now.hour
        para.st_min = now.minute 
        para.end_hr = now.hour + para.total_hr
        para.end_min = now.minute + para.total_min
        if para.end_min >= 60:
            para.end_min = para.end_min - 60
            para.end_hr +=1
        if para.end_hr >= 24:
            para.end_hr = para.end_hr -24
        
        para.event = "next"


    @classmethod
    def set_spec_start(cls):

        now = datetime.now()
        layout2 = [#[sg.MenuBar([['ファイル',['終了']]], key='menu1')],
                [sg.Text('録画タイミング', font=('HGｺﾞｼｯｸE', 35), background_color='#1F4F7B', pad=((215, 200),(0, 10)))],
                [sg.Text('時間：', font=('HGｺﾞｼｯｸE', 30)), sg.Slider(range=(0, 23), default_value=now.hour, orientation='h')],
                [sg.Text('分　：', font=('HGｺﾞｼｯｸE', 30)), sg.Slider(range=(0, 59), default_value=now.minute, orientation='h')], 
                [sg.Button('次へ', key='next', font=('HGｺﾞｼｯｸE', 25)),
                    sg.Button('初期メニュー', key='init', font=('HGｺﾞｼｯｸE', 25)),
                    sg.Button('中止', key='Quit', font=('HGｺﾞｼｯｸE', 25))]]
        window = sg.Window('スタート時間入力', layout=layout2, size=(800, 410), font=('HGｺﾞｼｯｸE', 30))#.Finalize()
        #window.Maximize()

        while True:
            event, values = window.read()
            if (event in [None, 'Cancel']) or event == "Quit":# or event == sg.WIN_CLOSED or values['menu1']=='終了':
                window.close()
                break
            elif event == "init":
                window.close()
                para.event = event
                break
            para.st_hr = int(values[0])
            para.st_min = int(values[1])
            if para.st_min >= 60:
                para.st_min = para.st_min - 60
                para.st_hr +=1
            if para.st_hr >= 24:
                para.st_hr = para.st_hr -24
            para.end_hr = para.total_hr + int(values[0])
            para.end_min = para.total_min + int(values[1])
            if para.end_min >= 60:
                para.end_min = para.end_min - 60
                para.end_hr +=1
            if para.end_hr >= 24:
                para.end_hr = para.end_hr -24
            window.close()
            para.event = event
            break

        window.close()


    @classmethod
    def start_eventrec(cls):

        end_time = "録画終了時刻は" + str(para.end_hr) + "時" + str(para.end_min) + "分頃です" 
        layout = [#[sg.MenuBar([['ファイル',['終了']]], key='menu1')],
                [sg.Text(end_time)],
                [sg.Text('録画しますか', key='start', font=('HGｺﾞｼｯｸE', 25)),
                    sg.Button('開始', key='next', font=('HGｺﾞｼｯｸE', 25)),
                    sg.Button('初期メニュー', key='init', font=('HGｺﾞｼｯｸE', 25)), 
                    sg.Button('中止', key='Quit', font=('HGｺﾞｼｯｸE', 25))]]

        window = sg.Window('録画', layout=layout, size=(800, 410), font=('HGｺﾞｼｯｸE', 30))#.Finalize()
        #window.Maximize()

        while True:
            event, values = window.read()

            if (event in [None, 'Cancel']) or event == "Quit":# or event == sg.WIN_CLOSED or values['menu1']=='終了':
                window.close()
                break
            elif event == "init":
                window.close()
                para.event = event
                break
            elif event == 'next':
                window['start'].update('連続録画中')
                #event, values = window.read()
                #window['start'].update('録画中です')
                window.close()
                para.event = event
                break

        #window.close()


    @classmethod
    def set_sesitivity(cls):

        layout = [#[sg.MenuBar([['ファイル',['終了']]], key='menu1')],
                [sg.Text('トリガー感度', font=('HGｺﾞｼｯｸE', 35), background_color='#1F4F7B', pad=((250, 200),(0, 10)))],
                [sg.Text('閾値　　：', font=('HGｺﾞｼｯｸE', 30)), sg.Slider(range=(0, 255), default_value=70, orientation='h')],
                [sg.Text('変化率％：', font=('HGｺﾞｼｯｸE', 30)), sg.Slider(range=(0, 0.2), resolution=0.0001, default_value=0.002, orientation='h')], 
                [sg.Button('次へ', key='next', font=('HGｺﾞｼｯｸE', 25)),
                    sg.Button('初期メニュー', key='init', font=('HGｺﾞｼｯｸE', 25)),
                    sg.Button('中止', key='Quit', font=('HGｺﾞｼｯｸE', 25))]]

        window = sg.Window('トリガー感度設定', layout=layout, size=(800, 410), font=('HGｺﾞｼｯｸE', 30))#.Finalize()
        #window.Maximize()

        while True:
            event, values = window.read()

            #print(event, values)
            if (event in [None, 'Cancel']) or event == "Quit":# or event == sg.WIN_CLOSED or values['menu1']=='終了':
                window.close()
                break
            elif event == "init":
                window.close()
                para.event = event
                break
            elif event == 'next':
                para.thd = int(values[0])
                para.ratio = values[1]
                #print(para.thd, para.ratio)
                window.close()
                para.event = event
                break

        window.close()

    @classmethod
    def start_ermrec(cls):

        layout = [#[sg.MenuBar([['ファイル',['終了']]], key='menu1')],
                [sg.Text('録画しますか', key='start', font=('HGｺﾞｼｯｸE', 25)),
                    sg.Button('開始', key='next', font=('HGｺﾞｼｯｸE', 25)),
                    sg.Button('初期メニュー', key='init', font=('HGｺﾞｼｯｸE', 25)),
                    sg.Button('中止', key='Quit', font=('HGｺﾞｼｯｸE', 25))]]

        window = sg.Window('録画', layout=layout, size=(800, 410), font=('HGｺﾞｼｯｸE', 30))#.Finalize()
        #window.Maximize()

        while True:
            event, values = window.read()

            #print(event, values)
            if (event in [None, 'Cancel']) or event == "Quit":# or event == sg.WIN_CLOSED or values['menu1']=='終了':
                window.close()
                break
            elif event == "init":
                window.close()
                para.event = event
                break
            elif event == 'next':
                window['start'].update('トリガー前後15秒録画中')
                #event, _ = window.read()
                window.close()
                para.event = event
                break
           
        #window.close()
