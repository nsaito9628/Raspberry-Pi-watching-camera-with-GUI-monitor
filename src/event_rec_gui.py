#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import os
from datetime import datetime
import subprocess
import boto3
import parameters as para


ACCESS_KEY = para.ACCESS_KEY
SECRET_KEY = para.SECRET_KEY
REGION = para.REGION
CAM_NO = para.CAM_NO
S3BUCKET = para.S3BUCKET

resos_webcam = [[176, 144, 135, 24, 0.7], [320, 240, 230, 20, 1.3], [640, 480, 470, 15, 2], [800, 600, 585, 10, 2.2], [1280, 960, 900, 5, 3.5]]
resos_periscope = [[640, 480, 470, 15, 2], [1280, 960, 900, 5, 3.5]]


class Cont_rec:

    def __init__(self):
        self.file_name = datetime.now().strftime('%Y%m%d%H%M')
        self.local_dirpath = './event/'
        self.s3_prefix = 'video/' + CAM_NO + '/cont/'
        self.cam_No = CAM_NO + '_'
        self.s3_bucket_name = S3BUCKET
        self.screen = [800, 480]


    @classmethod
    def exec(cls):
        cont_rec = Cont_rec()
        rec_flag = cont_rec.event_record()
        return rec_flag


    def event_record(self):
        os.makedirs(self.local_dirpath, exist_ok=True)

        res = para.res 
        st_hr = para.st_hr
        st_min = para.st_min 
        end_hr = para.end_hr
        end_min = para.end_min

        
        if para.cam_type == 0:
            resos = resos_webcam
        elif para.cam_type == 1:
            resos = resos_periscope
        
        for i in range(5):
            print(i)
            if res == i: 
                width = resos[i][0]
                heigth = resos[i][1]
                label_pos = resos[i][2]
                fps = resos[i][3]
                f_size = resos[i][4]
                print(width, heigth, label_pos, fps, f_size)
                break

        device_id = -1
        cap = cv2.VideoCapture(device_id)

        if True==cap.isOpened(): #Cameraをオープンできなかったらreboot
            ret = cap.set(3,width)
            ret = cap.set(4,heigth)
            ret = cap.set(5,fps)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')#('M','J','P','G')#(*'mp4v')
            writer = cv2.VideoWriter(self.local_dirpath + self.cam_No + self.file_name + '.mp4', fourcc, fps, (width, heigth))
            print(width, heigth, label_pos, fps, f_size)
        else:
            subprocess.call(["sudo","reboot"])
        
        while True:
            print(width, heigth, label_pos, fps, f_size)
            t = datetime.now()
            if t.hour>=st_hr and t.minute>=st_min:
                while True:
                    t = datetime.now()
                    ret, frame = cap.read() # 1フレームずつ取得する
                    if not ret:
                        return False  # 映像取得に失敗
                    cv2.putText(frame, t.strftime('%Y/%m/%d/%H:%M:%S'), (0, label_pos), cv2.FONT_HERSHEY_COMPLEX_SMALL, f_size, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.imshow('frame', frame) #モニターに接続している場合はコメント解除すると画面が表示される
                    cv2.moveWindow('frame', int(self.screen[0]/2)-int(width/2), int(self.screen[1]/2)-int(heigth/2))
                    #cv2.moveWindow('frame', 0, 0)
                    writer.write(frame)  # フレームを書き込む。

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break  # q キーを押したら終了する。
                    elif t.hour==end_hr and t.minute==end_min:
                        writer.release()
                        subprocess.call(["ffmpeg","-i", self.local_dirpath + self.cam_No +  self.file_name + '.mp4',"-r", str(fps), self.local_dirpath + self.cam_No + self.file_name + '-1.mp4'])
                        subprocess.call(["sudo","rm", self.local_dirpath + self.cam_No +  self.file_name + '.mp4']) #元のaviファイルを削除する
                        self.upload_awsS3()
                        cap.release()
                        cv2.destroyAllWindows()
                        #subprocess.call(["sudo","reboot"])
                        return True


    def upload_awsS3(self):
        
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key= SECRET_KEY, region_name=REGION)

        s3.upload_file(self.local_dirpath + self.cam_No + self.file_name + "-1.mp4", self.s3_bucket_name, self.s3_prefix + self.cam_No + self.file_name + ".mp4")
        print("uploaded {0}".format(self.file_name+".mp4"))
        subprocess.call(["sudo","rm", self.local_dirpath + self.cam_No + self.file_name + '-1.mp4']) #mp4ファイルを削除する
