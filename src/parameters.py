#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
REGION = os.environ['REGION']
CAM_NO = os.environ['CAM_NO']
S3BUCKET = os.environ['S3BUCKET']

cam_type = 0

res = 1

total_hr = 0
total_min = 0

st_hr = 0
st_min = 0 
end_hr = 0
end_min = 0

thd = 0
ratio = 0

event = ""

rec_flag = False