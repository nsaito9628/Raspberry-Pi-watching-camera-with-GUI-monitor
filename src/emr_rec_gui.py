#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import os
import datetime
from emr_gen_gui import Emr_gen
import subprocess
import parameters as para

#time.sleep(20)

#出力先パス設定

ACCESS_KEY = para.ACCESS_KEY
SECRET_KEY = para.SECRET_KEY
REGION = para.REGION
CAM_NO = para.CAM_NO
S3BUCKET = para.S3BUCKET

resos_webcam = [[176, 144, 135, 20, 0.7], [320, 240, 230, 16, 1.3], [640, 480, 470, 12, 2], [800, 600, 585, 8, 2.2], [1280, 960, 900, 5, 3.5]]
resos_periscope = [[640, 480, 470, 12, 2], [1280, 960, 900, 5, 3.5]]

gen = Emr_gen()


class Emr_rec:

    def __init__(self):
        self.res = para.res
        self.thd = para.thd
        self.ratio = para.ratio
        self.output_dirpath = './tmp/'
        self.emr_dirpath = './emr/'
        self.cam_No = 'emr_' + CAM_NO + '_'
        self.s3_prefix = 'video/' + CAM_NO + '/emr/'
        self.s3_bucket_name = S3BUCKET
        self.filepath_timesorted = []
        self.local_dirpath = './emr/'

        # 保存用ディレクトリを作成する。
        os.makedirs(self.output_dirpath, exist_ok=True)
        os.makedirs(self.emr_dirpath, exist_ok=True)

        if para.cam_type == 0:
            self.resos = resos_webcam
        elif para.cam_type == 1:
            self.resos = resos_periscope
        
        for i in range(5):#
            if self.res == i: 
                self.width = self.resos[i][0]
                self.heigth = self.resos[i][1]
                self.label_pos = self.resos[i][2]
                self.fps = self.resos[i][3]
                self.f_size = self.resos[i][4]
                self.chd_pix = self.resos[i][0] * self.resos[i][1] * self.ratio
                break


    @classmethod
    def exec(cls):

        emr = Emr_rec()
        rec_flag = emr.emergency_capture()

        return rec_flag


    def emergency_capture(self):

        #映像入力用のvideoCapture 作成
        device_id = -1
        self.cap = cv2.VideoCapture(device_id)

        #Cameraをオープンできなかったらreboot
        if True==self.cap.isOpened(): 
            ret = self.cap.set(3, self.width)
            ret = self.cap.set(4, self.heigth)
            ret = self.cap.set(5, self.fps)
        else:
            subprocess.call(["sudo","reboot"])

        while True:
            self.set_loop()
        
            if cv2.waitKey(1) == 13:
                self.cap.release()
                cv2.destroyAllWindows()
                return True  # q キーを押したら終了する。
        #return True


    def set_loop(self): #長さ4秒の動画を01.aviから05.aviまで5本録画してたら01.aviから順に上書きするループ
        emr_trigger = 0

        for loop_count in (0,1,2,3,4):
            file_name = '0' + str(loop_count+1)

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')#('M','J','P','G')#(*'mp4v')
            writer = cv2.VideoWriter(self.output_dirpath + file_name + '.mp4', fourcc, self.fps, (self.width, self.heigth))

            emr_trigger = self.video_writer(emr_trigger, writer)
            if emr_trigger ==1: #直前の録画ループ中にセンサーが検知してたら、録画後にtmpフォルダーの動画を結合する
                if loop_count == 4: file_name = '01'
                else: file_name = '0' + str(loop_count+2)

                fourcc = cv2.VideoWriter_fourcc(*'mp4v')#('M','J','P','G')#(*'mp4v')
                writer = cv2.VideoWriter(self.output_dirpath + file_name + '.mp4', fourcc, self.fps, (self.width, self.heigth))

                emr_trigger = self.video_writer(emr_trigger, writer)
                emr_filename = self.cam_No + datetime.datetime.now().strftime('%Y%m%d%H%M')
                gen.combine_file(emr_filename, self.width, self.heigth, self.fps)
                emr_trigger = 0
                writer.release()
                return

            if cv2.waitKey(1) == (13):
                self.cap.release()
                cv2.destroyAllWindows()
                return True  # q キーを押したら終了する。


    def video_writer(self, emr_trigger, writer): #録画ルーチン
        trigger_change = 0
        
        t0=datetime.datetime.now()
        t1=datetime.datetime.now()
        delta = t1 - t0
        
        if emr_trigger == 1: interval = 12 #直前の録画ループ中にセンサーが検知してたら13秒録画する
        else: interval = 3 #直前の録画ループ中にセンサーが検知してなかったら4秒録画する

        while delta.seconds <= interval:

            ret, frame = self.cap.read() # 1フレームずつ取得する            
            ret2, frame2 = self.cap.read()
            ret3, frame3 = self.cap.read()
            if not ret:
                return  # 映像取得に失敗


            cv2.putText(frame, t1.strftime('%Y/%m/%d/%H:%M:%S'), (0, self.label_pos), cv2.FONT_HERSHEY_COMPLEX_SMALL, self.f_size, (255, 255, 255), 1, cv2.LINE_AA) #self.label_pos
            cv2.putText(frame2, t1.strftime('%Y/%m/%d/%H:%M:%S'), (0, self.label_pos), cv2.FONT_HERSHEY_COMPLEX_SMALL, self.f_size, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame3, t1.strftime('%Y/%m/%d/%H:%M:%S'), (0, self.label_pos), cv2.FONT_HERSHEY_COMPLEX_SMALL, self.f_size, (255, 255, 255), 1, cv2.LINE_AA)

            if ret and ret2 and ret3:
                #グレースケールに変換
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                gray3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)
        
                diff1 = cv2.absdiff(gray2,gray)
                diff2 = cv2.absdiff(gray3,gray2)
    
                diff_and = cv2.bitwise_and(diff1, diff2)
    
                th = cv2.threshold(diff_and, self.thd, 255, cv2.THRESH_BINARY)[1]

            if cv2.countNonZero(th) > self.chd_pix:
                trigger_change = 1

            writer.write(frame)
            writer.write(frame2)
            writer.write(frame3)  # フレームを書き込む。
            t1=datetime.datetime.now()
            delta = t1 - t0

            #cv2.imshow('frame', frame)
            #cv2.imshow('gray', gray)
            #cv2.imshow('binary', diff_and)

        if trigger_change == 1: emr_trigger = 1

        writer.release()

        return emr_trigger

