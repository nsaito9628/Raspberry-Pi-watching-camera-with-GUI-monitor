#!/bin/bash

# update&upgrade
sudo apt install jq -y
sudo apt update -y
sudo apt upgrade -y

# creating cron_mod.conf
echo >> cron_mod.conf
echo ACCESS_KEY=$(cat ./.aws/credentials | grep aws_access_key_id | awk -F'= ' '{print $2}') >> cron_mod.conf
echo SECRET_KEY=$(cat ./.aws/credentials | grep aws_secret_access_key | awk -F'= ' '{print $2}') >> cron_mod.conf
echo REGION=$(cat ./.aws/config | grep region | awk -F'= ' '{print $2}') >> cron_mod.conf
echo CAM_NO=$(cat env_const_config | grep CAM_NO | awk -F'=' '{print $2}') >> cron_mod.conf
echo S3BUCKET=$(cat env_const_config | grep S3BUCKET | awk -F'=' '{print $2}') >> cron_mod.conf
echo >> cron_mod.conf
echo @reboot . ~/.profile >> cron_mod.conf

# adding .profile
echo >> ./.profile
echo export ACCESS_KEY=$(cat ./.aws/credentials | grep aws_access_key_id | awk -F'= ' '{print $2}') >> ./.profile
echo export SECRET_KEY=$(cat ./.aws/credentials | grep aws_secret_access_key | awk -F'= ' '{print $2}') >> ./.profile
echo export REGION=$(cat ./.aws/config | grep region | awk -F'= ' '{print $2}') >> ./.profile
echo export CAM_NO=$(cat env_const_config | grep CAM_NO | awk -F'=' '{print $2}') >> ./.profile
echo export S3BUCKET=$(cat env_const_config | grep S3BUCKET | awk -F'=' '{print $2}') >> ./.profile
echo >> ./.profile

cat cron_mod.conf

crontab cron_mod.conf

sudo cp /home/pi/windowspy.desktop  /etc/xdg/autostart/