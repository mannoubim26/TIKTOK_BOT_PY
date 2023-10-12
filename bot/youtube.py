from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time 
from selenium.webdriver.common.by import By
from bot.Items import videoItem , KeywordItem
import fileinput
from bot.Constants import USERS_LIST
class youtube (webdriver.Chrome) :

    keywords=list()
    videos=list()
    User=None
    
    def __init__(self, options: Options = None, service: Service = None, keep_alive: bool = True) -> None:
        options=webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('window-size=1920x1480')
        super().__init__(options, service, keep_alive)

    def select_user (self) :
        print('These are your current Accounts : ')
        for elem in USERS_LIST:
            print(elem.Username)
        while True:
            i = input("Choose a Username From the List : ")
            for elem in USERS_LIST:
                if elem.Username.upper() == i.upper():
                    print(f'User {elem.Username} selected')
                    self.User=elem
                    return None
            else:
                print('Invalid Username. Please choose a valid one From The List : ')
 
    def get_input(self) :
        while True : 
            i= input('Type a Keyword , Type FILE to input a File , Type STOP to end\n')
            if i.upper()== 'file'.upper() : 
                f=input(' Type The File path : \n')
                for line in fileinput.input(files=f):
                    print("Keyword Added Succesfully : " , line)
                    self.select_user()
                    keyword=KeywordItem(line, self.User)
                    self.keywords.append(keyword)
            elif i.upper() == 'stop'.upper() :
                break
            else :
                self.select_user()
                keyword=KeywordItem(i,self.User)
                self.keywords.append(keyword)


    def Format_Keywords(self ) :
        for elem in self.keywords : 
            elem.Keyword.strip()
            elem.Keyword=elem.Keyword.replace(' ' , '+')
            if elem.Keyword.upper() == "file".upper() or elem.Keyword.upper() == "stop".upper() :
                self.keywords.remove(elem)

    def check_length(self ,elem) : 
        T = [int(i) for i in str(elem).split() if i.isdigit()]
        if elem is None :
            return True
        if str(elem) == "Shorts" :
            return True
        elif str(elem).__contains__("houres") :
            return True
        elif str(elem).__contains__('1 hour') :
            if str(elem).__contains__('minutes') :
                if T[1] > 14 :
                    return True
        elif not str(elem).__contains__('1 hour') :
            if not str(elem).__contains__('minutes') :
                return True
            elif T[0] <3 : 
                return True
        return False
                
    def search(self) :
        timeout = 900   # [seconds]
        try :
            for root in self.keywords :
                start_time = time.time()
                print(' -------------------- Getting Youtube Videos for Keyword : ' , root.Keyword)
                self.get(f'https://www.youtube.com/results?search_query={root.Keyword}&sp=CAMSAhAB')
                time.sleep(5)
                while True :
                    self.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
                    time.sleep(2)
                    try :
                        self.find_element(By.ID ,'message')
                        print(f'---------- Captured all results for {root.Keyword}, Filtering now...')
                        break 
                    except : 
                        if time.time()> start_time + timeout :
                            print(f'--------- Scrolling time exceeded limit,Capturing results for {root.Keyword}, Filtering now...')
                            break
                        
                list=self.find_elements(By.TAG_NAME,'ytd-video-renderer')
                print('Storing info for ',len(list) , 'videos')
 
                for elem in list : 
                        Title = elem.find_element(By.ID ,'video-title').get_attribute('title')
                        Link = elem.find_element(By.CLASS_NAME,'yt-simple-endpoint').get_attribute('href')
                        Length = elem.find_element(By.ID,'text').get_attribute('aria-label')
                        if self.check_length(Length) :
                            continue
                        video=videoItem(Title,Length,Link,root)
                        self.videos.append(video)
        except :
            print('Something is wrong , Retrying again .... ')
            self.refresh()
            self.search()

    def return_Videos(self) :
        print('Youtube search  successfully Finished , Number of results : ', len(self.videos))
        return self.videos


                        
                       
        

            
