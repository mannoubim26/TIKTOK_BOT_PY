from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time 
from selenium.webdriver.common.by import By
from mailtm import Email
import re
from bot.Waits import  wait_to_be_located_and_clickable , wait_to_be_located
from bot.Constants import GENERATED_USERNAME , GENERATED_PASSWORD
class Account (webdriver.Chrome) :
    Domain=None
    Message=None
    Url=None
    Emails=list()
    def __init__(self, options: Options = None, service: Service = None, keep_alive: bool = True) -> None:
        options=webdriver.ChromeOptions()
        options.add_argument('--headless')
        super().__init__(options, service, keep_alive)
        
    def findurl (self ,string):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, string)
        return [x[0] for x in url]
    
    def config(self): 
        self.domain=None
        self.Message=None
        self.Domain = Email()
        self.Domain.register()
        
    def listener(self ,message):
        self.Message=message['text'] if message['text'] else message['html']

    def catch(self) :
        while self.Message is None :
            self.Domain.start(self.listener)
        self.Url=self.findurl(self.Message)[0]
        self.Domain.stop()

    def create_account(self) :
        print('Creating Account With Email : ', self.Domain.address)
        self.get('https://app.vidyo.ai/auth/login')
        time.sleep(5)
        try :
            wait_to_be_located_and_clickable(self , 120 ,(By.XPATH ,'/html/body/div[1]/div[1]/main/div/div/section/div/div[2]/div/div[2]/button[2]') ).click()
        except :
            wait_to_be_located_and_clickable(self , 120 , (By.CLASS_NAME,'text-right')).click()
            #wait_to_be_located_and_clickable(self , 120 ,(By.CSS_SELECTOR ,'#root > div.App.font-inter > main > div > div > section > div > div.px-6.lg\:w-\[35vw\].md\:w-\[50vw\].md\:space-y-10.xl\:max-w-md.relative > div > div:nth-child(2) > button.focus\:\!ring-2.group.flex.h-min.items-center.justify-center.p-0\.5.text-center.font-medium.focus\:z-10.rounded-lg.border-black\/60.inline-flex.w-full.items-center.justify-center.rounded-md.border.text-sm.font-medium.text-gray-900.focus\:z-10.focus\:outline-none.focus\:ring-4.focus\:ring-gray-200.dark\:border-gray-600.dark\:bg-gray-800.dark\:text-gray-400.dark\:focus\:ring-gray-700.bg-\[fff\].hover\:bg-\[\#f2f2f2\]')).click()
        wait_to_be_located(self,120,(By.ID ,'fullName')).send_keys(GENERATED_USERNAME)
        wait_to_be_located(self,120,(By.ID ,'email')).send_keys(f'{self.Domain.address}')
        wait_to_be_located(self,120,(By.ID ,'password')).send_keys(GENERATED_PASSWORD)
        wait_to_be_located_and_clickable(self , 120 , (By.ID,'sign-up-button')).click()
        time.sleep(10)
        print(' ------------------------- Account created Successfully ')


    def verify_account(self) :
        print(' ------------------------------ Account Verification')
        try :
            self.get(str(self.Url))
            time.sleep(5)
            self.Emails.append(self.Domain.address)
            print(' ------------------------------ Account Verified Succesfully')
        except :
            print('Something Is wrong , Retrying in a moment ....')
            time.sleep()
            self.config()
            self.catch()
            self.create_account()
            self.verify_account()


