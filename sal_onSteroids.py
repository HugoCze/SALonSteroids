from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, ElementNotInteractableException, StaleElementReferenceException, TimeoutException,ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time 
import datetime
import os
date_time = datetime.datetime.now()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-features=DefaultPassthroughCommandDecoder")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--ignore-ssl-errors=yes")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")

chrome_options.headless = True

edge_options = webdriver.EdgeOptions()
edge_options.add_argument("--disable-features=DefaultPassthroughCommandDecoder")
edge_options.add_argument("--disable-web-security")
edge_options.add_argument("--allow-running-insecure-content")
edge_options.add_argument("--ignore-ssl-errors=yes")
edge_options.add_argument("--ignore-certificate-errors")
edge_options.add_argument("--allow-insecure-localhost")

edge_options.headless = True

Chrome_driver = webdriver.Chrome(options=chrome_options)
Chrome_driver.set_page_load_timeout(5)
Edge_driver = webdriver.Edge(options=edge_options)
Edge_driver.set_page_load_timeout(5)

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException,\
     TimeoutException, ElementClickInterceptedException, InvalidSessionIdException)

Chrome_wait = WebDriverWait(Chrome_driver, 10, ignored_exceptions=ignored_exceptions)
Edge_wait = WebDriverWait(Edge_driver, 10, ignored_exceptions=ignored_exceptions)



class Search_And_Like:

    CURRENT_DRIVER = ""
    PROCCESS_COUNTER = 0
    COMMENT_BUCKET = []
    BUCKET_STATUS = False
    FIRST_FIRST_PAGE_COMMENT = ""
    CURRENT_PAGE = 1


    def choose_driver(self, path, comment):
        if self.CURRENT_DRIVER == "":   
            print(f"choose_driver - driver == empty string - going with Chrome", file=open('SAL_Logs.txt','a'))
            driver_type = Chrome_driver
            self.CURRENT_DRIVER = Chrome_driver
        elif self.CURRENT_DRIVER == Chrome_driver: 
            print(f"choose_driver - driver == Chrome - going with Edge", file=open('SAL_Logs.txt','a'))
            driver_type = Edge_driver
            self.CURRENT_DRIVER = Edge_driver
        elif self.CURRENT_DRIVER == Edge_driver: 
            print(f"choose_driver - driver == Edge - going with Chrome", file=open('SAL_Logs.txt','a'))
            driver_type = Chrome_driver
            self.CURRENT_DRIVER = Chrome_driver
        ## ENDING
        self.get_homePage(path, comment, driver_type)
    
    def get_homePage(self, path, comment, driver):
        homepage = "https://www.pudelek.pl/" + path
        try:
            driver.get(homepage)
            print("got home page")
            self.terms(path, comment, driver)
        except ignored_exceptions:
            print(f"Search_And_Like - failed to get homePage - refresh and terms", file=open('SAL_Logs.txt','a'))
            self.terms(path, comment, driver)
    
    def terms(self, path, comment, driver):
        print("Terms and conditions starting...", file=open('SAL_Logs.txt','a'))
        try:
            self.click("/html/body/div[3]/div/div[2]/div[3]/div/button[2]", "clicked accept terms button", driver)
            self.search_comment(path, comment, driver)
        except ignored_exceptions:
            print(f"terms - Terms and conditions not found - searching comment", file=open('SAL_Logs.txt','a'))
            self.search_comment(path, comment, driver)
    
    def click(self, xpath, call_indication, driver):
        button_location = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button_location)
        print(f"click - clicking given xpath: {xpath} - {call_indication}", file=open('SAL_Logs.txt','a'))

    def search_comment(self, path, comment, driver):
        print(f"search_comment - searching for comment - CURRENT PAGE IS: {self.CURRENT_PAGE}", file=open('SAL_Logs.txt','a'))
        fc_XPATH = '//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[3]/div/div[2]'
        fc_location = driver.find_element(By.XPATH, fc_XPATH)
        fc_XP_text = fc_location.get_attribute('innerHTML')
        if self.CURRENT_PAGE == 1:
            print(f"search_comment - CURRENT PAGE IS: {self.CURRENT_PAGE} assining {fc_XP_text} as a FIRST_FIRST_PAGE_COMMENT", file=open('SAL_Logs.txt','a'))
            self.FIRST_FIRST_PAGE_COMMENT = fc_XP_text
        if self.CURRENT_PAGE != 1 and self.FIRST_FIRST_PAGE_COMMENT == fc_XP_text:
            print(f"search_comment - CURRENT PAGE IS: {self.CURRENT_PAGE}, first comment on the page is: {fc_XP_text} and FIRST_FIRST_PAGE_COMMENT is {self.FIRST_FIRST_PAGE_COMMENT} \n running sal 2", file=open('SAL_Logs.txt','a'))
            self.FIRST_FIRST_PAGE_COMMENT = ""
            self.CURRENT_PAGE = 1
            # self.choose_driver(path, comment)
            os.system("python3 /Users/czerniah/Search_And_Like/sal_onSteroids1.py")
        for i in range(0, 34):
            try:
                possible_comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[2]'
                comment_location = driver.find_element(By.XPATH, possible_comment_xp)
                comment_text = comment_location.get_attribute('innerHTML')
                print(comment_text, file=open('SAL_Logs.txt','a'))
                if comment_text.strip() == comment.strip():
                    print(f"Did find the comment: {comment_text}", file=open('SAL_Logs.txt','a'))
                    like_button = possible_comment_xp[:-6]
                    like_button_xp = like_button + "div[1]/div[2]/div/button[1]"
                    print("got the like butt xpath", file=open('SAL_Logs.txt','a'))
                    self.click(like_button_xp, "search_comment - called click like button from comment searching", driver)
                    self.CURRENT_PAGE = 1
                    self.COMMENT_BUCKET = []
                    # break
                    return
            except ignored_exceptions:
                pass
        else:
            self.search_next(path, comment, driver)
    
    def search_next(self, path, comment, driver):
        print("search_next - searching the next button", file=open('SAL_Logs.txt','a'))
        for i in range(19, 36):
            for j in range(2,4):
                try:
                    next_button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div'
                    button_action = driver.find_element(By.XPATH, next_button_xp)
                    button_possible_text = button_action.get_attribute('innerHTML')
                    if button_possible_text == "Nast??pna strona":
                        print("search_next - got the next button", file=open('SAL_Logs.txt','a'))
                        self.click(next_button_xp, "search_next - clicked the next button", driver)
                        self.CURRENT_PAGE += 1
                        self.search_comment(path, comment, driver)
                        return
                except ignored_exceptions:
                    pass
    
    def main(self, path, comment):
        print(" \n \n main - here we are at main. Calling get_homePage", file=open('SAL_Logs.txt','a'))
        # self.get_homePage(path, comment)
        self.choose_driver(path, comment)

SAL = Search_And_Like()

while True:
    SAL.PROCCESS_COUNTER += 1 
    start_time = time.time()
    SAL.main("jacek-kopczynski-ma-nowa-partnerke-nastepczyni-patrycji-markowskiej-potwierdza-ich-zwiazek-raczej-juz-tego-nie-ukryjemy-6859714963409600a", "Pi??kna dziewczyna .Markowska nie umie ??piewa?? , istnieje tylko dzi??ki znanemu ojcu.")
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Time of looking the comment is equal to: {total_time} ",  file=open('SAL_Logs.txt','a'))
    print(f"Counter: {SAL.PROCCESS_COUNTER} ",  file=open('SAL_Logs.txt','a'))