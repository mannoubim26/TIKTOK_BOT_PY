import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time 
import openai
from glob import glob
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bot.Constants import API_KEY , DOWNLOAD_PATH , PROMPT
from bot.Items import ShortItem
from bot.Waits import wait_to_be_located , wait_to_be_located_and_clickable , wait_all_to_be_located 
class Shorts (webdriver.Chrome) :
    Shorts=[]
    def __init__(self,  Email , Link , options: Options = None, service: Service = None, keep_alive: bool = True) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1920x1480')
        options.add_argument('--headless')
       
        options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_PATH,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})
        self.Email=Email 
        self.Link=Link
        super().__init__(options, service, keep_alive)

    def login(self) :
        print(' -------------------- Attempting to Log in')
        try :
            self.get('https://app.vidyo.ai/auth/login')
            wait_to_be_located_and_clickable(self , 120 , (By.XPATH ,'/html/body/div[1]/div[1]/main/div/div/section/div/div[2]/div/p/span')).click()
            wait_to_be_located(self , 120 , (By.ID,'email')).send_keys(f'{self.Email}')
            wait_to_be_located(self , 120 , (By.ID,'password')).send_keys('generatedpassword123')
            wait_to_be_located_and_clickable(self , 120 , (By.ID,'sign-in-button')).click()
        except  :
            print(' -------------------- Error Occured while logging in , Trying Again ...')
            try : 
                self.refresh()
                wait_to_be_located_and_clickable(self , 120 , (By.XPATH ,'/html/body/div[1]/div[1]/main/div/div/section/div/div[2]/div/p/span')).click()
                wait_to_be_located(self , 120 , (By.ID,'email')).send_keys(f'{self.Email}')
                wait_to_be_located(self , 120 , (By.ID,'password')).send_keys('generatedpassword123')
                wait_to_be_located_and_clickable(self , 120 , (By.ID,'sign-in-button')).click()
            except : 
                    raise Exception(' -------------------- Failed to Login')
        
    def upload(self , username) :
        try :
            wait_to_be_located_and_clickable(self , 120 , (By.ID,'welcome-upload-file-modal-button')).click()
            print(' -------------------- Success Logging in')
        except : 
            try : 
                wait_to_be_located_and_clickable(self , 120 , (By.ID ,'home-top-upload-file-modal-button-social')).click()
                print(' -------------------- Success Logging in')
            except :
                 print(' -------------------- Error Occured , Trying Again ...')
                 self.login()
        wait_to_be_located(self , 120 , (By.CLASS_NAME , 'block')).send_keys(f'{self.Link}')
        try :
            print(' -------------------- Attempting Upload')
            wait_to_be_located_and_clickable(self , 120 , (By.ID ,'generate-clip-continue')).click()
        except : 
            try : 
                print(' -------------------- Error while Uploading, Trying again...')
                tryelem = wait_to_be_located(self , 120 , (By.ID ,'generate-clip-continue'))
                self.execute_script("arguments[0].click();",tryelem)
            except : 
                try :
                    time.sleep(180)
                    self.find_element(By.TAG_NAME ,'article').click()
                except :
                    raise Exception('Could not upload ')
        try :
            try :
                wait_to_be_located_and_clickable(self , 60 , (By.ID ,'9:16:1')).click()
            except :
                try :
                    tryelem = wait_to_be_located(self , 120 , (By.ID ,'9:16:1'))
                    self.execute_script("arguments[0].click();",tryelem)
                except :
                    try :
                        self.refresh()
                        self.upload()
                    except :
                        raise Exception('Could not upload ')
            wait_to_be_located_and_clickable(self , 60, (By.ID ,'continue-button-layout-preference')).click()
            list =wait_all_to_be_located(self , 60 , (By.TAG_NAME,'canvas'))
            for i in range(1,4) :
                list[i].click()
                time.sleep(1)
            try :
                wait_to_be_located_and_clickable(self , 60 , (By.ID ,'continue-button-template-selection')).click()
            except : 
                tryelem = wait_to_be_located(self , 120 , (By.ID ,'ontinue-button-template-selection'))
                self.execute_script("arguments[0].click();",tryelem)
        except : 
            raise Exception ('Could not Upload')
        try :
            wait_to_be_located(self,120,(By.ID ,'social_tiktok')).send_keys(f'@{username}')
        except : 
            try :
                self.find_element(By.ID,'social_tiktok').send_keys(f'@{username}')
            except : 
                pass
        wait_to_be_located_and_clickable(self , 120 , (By.ID,'done-button-personalize-video-form')).click()
        wait_to_be_located_and_clickable(self , 120 , (By.ID,'go-to-dashboard-onboarding-completed')).click()
        print(' -------------------- Success Uploading video ')


    def OpenAi_API(self,prompt,model="gpt-4" ) :
        openai.api_key = API_KEY
        print(' -------------------- OpenAI API endpoint ')
        try :
            messages = [{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,

    )       
            print('-------------- API endpoint success')
            return response.choices[0].message["content"]
        except :
            try :
                print('Error occuring with the API , trying again in 1 minute ... ')
                time.sleep(60)
                response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0,
    )       
                print('-------------- API endpoint success')
            except :
                print('waiting for the API endpoint , retrying in 3 minutes ...' )
                time.sleep(180)
                self.OpenAi_API(prompt)

    def get_tags (self,Caption):
        tags=list()
        tags.append("fyp")
        tags.append("foryou")
        words=Caption.split()
        for elem in words :
            if elem.startswith('#') :
                elem=elem.replace('#','')
                tags.append(elem)
        return tags
    
        
    def num_downloads(self) :
        os.chdir(DOWNLOAD_PATH)
        return sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime)

    def download (self ,user ) :
        self.Shorts.clear()
        try : 
            print('-------------- Catching Failed Generation')
            wait_to_be_located_and_clickable(self , 80 , (By.ID,'retry-project-card')).click()
        except : 
            print(' -------------------- No Failed Generations Found')

            
        try :
            print(' -------------------- Waititng For Generation')
            wait_to_be_located(self,600 , (By.ID,'review-clips-project-card'))
            self.find_element(By.TAG_NAME,'article').click()
            print(' -------------------- Generation Completed')
        except :
            print (' -------------------- Generation not found retrying ...')
            try : 
                self.refresh()
                self.download(user)
            except : 
                raise Exception('Could not get Generation')

            
        try :
            wait_to_be_located_and_clickable(self , 10 , (By.ID,'lets-go')).click()
        except : 
            pass

        
        print(' -------------------- Preparing Short For Download ')
        downloads=self.num_downloads()
        list =wait_all_to_be_located(self , 180 ,(By.CLASS_NAME ,'pt-1') )
        if len(list) >= 5:
            c =5 
        else :
            c=len(list)
        for i in range(c) :
            title=list[i].find_element(By.CLASS_NAME ,'tex-sm').text
            time.sleep(5)
            try :
                list[i].click()
            except :
                try:
                    self.execute_script("arguments[0].click();",list[i])
                except : 
                    self.refresh()
                    time.sleep(10)
                    self.execute_script("arguments[0].click();",list[i])

                    
            time.sleep(5)
            try :
                wait_to_be_located_and_clickable(self,120,(By.ID , 'make-changes-to-clip-button-new')).click()
            except :
                try : 
                    tryelem=wait_to_be_located(self,120,(By.ID , 'make-changes-to-clip-button-new'))
                    self.execute_script("arguments[0].click();",tryelem)
                except : 
                    self.refresh()
                    time.sleep(10)
                    tryelem=wait_to_be_located(self,120,(By.ID , 'make-changes-to-clip-button-new'))
                    self.execute_script("arguments[0].click();",tryelem)

                    
            try :
                wait_to_be_located_and_clickable(self,120,(By.ID , 'editor-render-video-button')).click()
            except :
                try :
                    tryelem=wait_to_be_located(self,120,(By.ID ,'editor-render-video-button'))
                    self.execute_script("arguments[0].click();",tryelem)
                except : 
                    try :
                        time.sleep(10)
                        tryelem=wait_to_be_located(self,120,(By.ID ,'editor-render-video-button'))
                        self.execute_script("arguments[0].click();",tryelem) 
                    except : 
                        self.refresh()
                        time.sleep(10)
                        tryelem=wait_to_be_located(self,120,(By.ID ,'editor-render-video-button'))
                        self.execute_script("arguments[0].click();",tryelem)
                        
            try :
                wait_to_be_located_and_clickable(self,120,(By.ID , 'download-confirm-btn')).click()
            except :
                try :
                    tryelem=wait_to_be_located(self,120,(By.ID , 'download-confirm-btn'))
                    self.execute_script("arguments[0].click();",tryelem)
                except :
                    time.sleep(10)
                    tryelem=wait_to_be_located(self,120,(By.ID , 'download-confirm-btn'))
                    self.execute_script("arguments[0].click();",tryelem)

                    
            try :
                wait_to_be_located_and_clickable(self,120,(By.ID , 'done-download-preference')).click()
            except :
                try :
                    tryelem=wait_to_be_located(self,120,(By.ID , 'done-download-preference'))
                    self.execute_script("arguments[0].click();",tryelem)
                except : 
                    time.sleep(10)
                    tryelem=wait_to_be_located(self,120,(By.ID , 'done-download-preference'))
                    self.execute_script("arguments[0].click();",tryelem)

                    
            while True :
                if len(downloads) < len(self.num_downloads()) :
                    print(' -------------------- Short Downloaded Succesfully ')
                    File=self.num_downloads()[len(self.num_downloads())-1]
                    File=str(File)
                    File=File.replace('.crdownload','')
                    prompt=f'{PROMPT}{title}'
                    Caption=self.OpenAi_API(prompt)
                    tags=self.get_tags(Caption)
                    Caption=Caption.replace('"','')
                    words=Caption.split()
                    for elem in words :
                        if elem.startswith('#') :
                            Caption = Caption.replace(elem,'')
                    short=ShortItem(File,Caption,tags,user)
                    exist=False
                    for s in self.Shorts :
                        if short.File == s.File :
                            exist=True
                            break
                    if exist == False :
                        self.Shorts.append(short)            
                    break
            
            try :
                wait_to_be_located_and_clickable(self,120,(By.CLASS_NAME,'ml-1')).click()
                print(' -------------------- Moving on the the next Short ')
            except :
                    try :
                        tryelem=wait_to_be_located(self,120,(By.CLASS_NAME,'ml-1'))
                        self.execute_script("arguments[0].click();",tryelem)
                    except : 
                        self.refresh()
                        time.sleep(10)
                        tryelem=wait_to_be_located(self,120,(By.CLASS_NAME,'ml-1'))
                        self.execute_script("arguments[0].click();",tryelem)

            updated_list=wait_all_to_be_located(self , 180 ,(By.CLASS_NAME ,'pt-1') )
            for x in range(c) :
                list[x]=updated_list[x]

    def return_Shorts(self) :
        print("Successfully downloaded ", len(self.Shorts) , " shorts : ")
        for elem in self.Shorts :
            print(elem)
        return self.Shorts
            
    

            
