# TIKTOK_BOT_PY

## Description

this project is a python bot for automating searching youtube videos , generating shorts from thoese videos and uploading them to tiktok  .

## requirements :

pip install requests
pip install Selenium
pip install open ai

you will also need to install chromedriver on your machine (verion must be compatible with your chrome version )

## Features

the bot takes a keyword (or multiple) / text file and the tiktok user account as input .
the bot will crawl youtube for all videos matching the keyword(s) given in the input , then it will generate a fake email , create an account in the vidyo website (ai tools that generates shorts from youtube links ) , confirm the account , upload the youtube video , simulate the proccess , then download 5 (dynamic) shorts to a local folder (view DOWNLOAD_PATH in constants.py) , it will then generate a tiktok caption and 3 tags for each short using open ai API service (you need to buy a membership) (add the API_KEY constant to constants.py)
and then upload the short to tiktok (tiktok login is automated using session id cookie) (check constants.py) .
the bot will upload a short every 2 houres for each tiktok user (limitted by tiktok algorithms)
