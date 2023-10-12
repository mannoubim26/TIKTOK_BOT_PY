from bot.youtube import youtube
from bot.Account import Account
from bot.Shorts import Shorts
from bot.tiktok import uploadVideo , delete_files_in_directory
from bot.Constants import DOWNLOAD_PATH , USERS_LIST
import requests
import time
			
start_time=time.time()
session_id_exp=4752000 #55 days
search=youtube()
search.get_input()
search.Format_Keywords()
try :
    search.search()
except :
      search.search()
results=search.videos
if len(results)==0 :
    raise Exception('ERROR WHILE CRAWLING YOUTUBE VIDEOS , TRY AGAIN PLEASE ')

for elem in results :
    Acc=Account() 
    Acc.config()
    Acc.create_account()
    Acc.catch()
    Acc.verify_account()
    print(Acc.Domain.address)
    Short=Shorts(Acc.Domain.address , elem.Link)
    Short.login()
    try :
        Short.upload(elem.Keyword.User.Username)
    except : 
          continue
    try :
        Short.download(elem.Keyword.User)
    except :
          continue
    shorts_list=Short.return_Shorts()
    if len(shorts_list)==0 :
        continue
    print(' ---------------------- Uploading',len(shorts_list),'shorts to Tiktok')
    for elem in shorts_list :
        if time.time()> start_time+session_id_exp :
                session=input("TYPE THE NEW SESSION ID OF ",elem.User.Username)
                for u in USERS_LIST :
                        if u.Username==elem.User.Username :
                                u.Session_ID=session
                                time_start=time.time()
                    
        try :
                uploadVideo(elem.User.Session_ID, f"{DOWNLOAD_PATH}\{elem.File}" ,elem.Caption ,elem.Tags)
                print('--------------- Sleeping for 2 houres , next upload should be around 2 houres')
                time.sleep(7000)
        except Exception as e :
                print(e)
                try :
                        print('Tiktok upload failed , retrying in 1 hour..')
                        time.sleep(3600)
                        uploadVideo(elem.User.Session_ID, f"{DOWNLOAD_PATH}\{elem.File}" ,elem.Caption ,elem.Tags)
                except Exception as e :
                        print(e)
                        print('could not upload short : ',elem.File ,' ignoring ..')
                        continue
    delete_files_in_directory()
print('FINISHED SUCCSSEFULLY')

