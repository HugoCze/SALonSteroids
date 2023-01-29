
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
date_time = datetime.datetime.now()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-features=DefaultPassthroughCommandDecoder")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--ignore-ssl-errors=yes")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")

chrome_options.headless = True
# Test
# chrome_options.headless = False

driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(5)

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException,\
     TimeoutException, ElementClickInterceptedException, InvalidSessionIdException, RecursionError)
wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)



class Search_And_Like:

    counter = 0
    CURRENT_PAGE = 1
    FIRST_FIRST_PAGE_COMMENT = ""
    
    def get_homePage(self, path, comment):
        homepage = "https://www.pudelek.pl/" + path
        try:
            driver.get(homepage)
            print("got home page")
            self.terms(path, comment)
        except ignored_exceptions:
            print(f"Search_And_Like - failed to get homePage - refresh and terms", file=open('SAL_Logs.txt','a'))
            self.terms(path, comment)
            
    def terms(self, path, comment):
        print("Terms and conditions starting...", file=open('SAL_Logs.txt','a'))
        try:
            self.click("/html/body/div[3]/div/div[2]/div[3]/div/button[2]", "clicked accept terms button")
            self.first_comment(path, comment)
        except ignored_exceptions:
            print(f"terms - Terms and conditions not found - checking first comment", file=open('SAL_Logs.txt','a'))
            self.first_comment(path, comment)

            # previous solution - directing to SEARCH_COMMENT func
            # print(f"terms - Terms and conditions not found - searching comment", file=open('SAL_Logs.txt','a'))
            # self.search_comment(path, comment)

    def search_comment(self, path, comment):
        print("search_comment - searching for comment", file=open('SAL_Logs.txt','a'))
        time.sleep(1)
        comment_bucket = []
        for i in range(0, 34):
            try:
                possible_comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[2]'
                comment_location = driver.find_element(By.XPATH, possible_comment_xp)
                comment_text = comment_location.get_attribute('innerHTML')
                comment_bucket.append(comment_text)
                # deep test 1
                # print(comment_text, file=open('SAL_Logs.txt','a'))
                
                # test 1
                if len(comment_text) >= 15:
                    print(comment_text[:15], file=open('SAL_Logs.txt','a'))
                else:    
                    print(comment_text, file=open('SAL_Logs.txt','a'))
                

                if comment_text.strip() == comment.strip():
                    print(f"\n Did find the comment: {comment_text} \n", file=open('SAL_Logs.txt','a'))
                    like_button = possible_comment_xp[:-6]
                    like_button_xp = like_button + "div[1]/div[2]/div/button[1]"
                    print("got the like butt xpath", file=open('SAL_Logs.txt','a'))
                    time.sleep(1)
                    self.click(like_button_xp, "search_comment - called click like button from comment searching")
                    print(f"loggin from search comment: Clicked Like. The CURRENT PAGE IS: {self.CURRENT_PAGE}", file=open('SAL_Logs.txt','a'))
                    self.CURRENT_PAGE = 1
                    print(f"Reduceing page counter to 1 IS: {self.CURRENT_PAGE}", file=open('SAL_Logs.txt','a'))
                    self.FIRST_FIRST_PAGE_COMMENT = ""
                    # break
                    return

            except ignored_exceptions:
                pass
        if len(comment_bucket) <= 2:
            print(f"directing to homepage COMMENT BUCKET is almost empty", file=open('SAL_Logs.txt','a'))
            # previous
            # self.get_homePage(path, comment)
            self.main(path, comment)
        else:
            self.search_next(path, comment)
            
    def search_next(self, path, comment):
        print(f"search_next - searching the next button. We are at {self.CURRENT_PAGE} page.", file=open('SAL_Logs.txt','a'))
        for i in range(19, 36):
            for j in range(2,4):
                try:
                    # classic
                    next_button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div'
                    # one div out
                    # next_button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div'
                    button_action = driver.find_element(By.XPATH, next_button_xp)
                    button_possible_text = button_action.get_attribute('innerHTML')
                    if button_possible_text == "Następna strona":
                        # check_article_range = self.check_range(next_button_xp)
                        # print(f"Checking article page range. The page range is: {check_article_range} pages", file=open('SAL_Logs.txt','a'))
                        print("search_next - got the next button", file=open('SAL_Logs.txt','a'))
                        wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xp)))
                        self.click(next_button_xp, "search_next - clicked the next button")
                        self.CURRENT_PAGE += 1
                        print(f"search_next - added 1 to PAGE COUNTER - Page counter now: {self.CURRENT_PAGE} pages.", file=open('SAL_Logs.txt','a'))
                        self.first_comment(path, comment)
                        # previously
                        # self.search_comment(path, comment)
                        # self.CURRENT_PAGE += 1
                        return
                except ignored_exceptions:
                    pass
                    # print(f"search_next - Exception while looping through possbile Next page buttons. We are at {self.CURRENT_PAGE} page.", file=open('SAL_Logs.txt','a'))

    def check_range(self, next_button_XP):
        l_next_button_XP = list(next_button_XP)
        l_next_button_XP[-10] = '2'
        s_next_button_XP = ''.join(str(i) for i in l_next_button_XP)
        range_button_XP = s_next_button_XP + '/button'
        print(f"Logging from self.check_range. The range button XP is: {range_button_XP} pages", file=open('SAL_Logs.txt','a'))
        range_button_XP_action = driver.find_element(By.XPATH, range_button_XP)
        try:
            range_button_XP_text = range_button_XP_action.get_attribute('innerHTML')
            return range_button_XP_text
        except ignored_exceptions:
            return "Failed reading."
        

    def click(self, xpath, call_indication):
        button_location = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button_location)
        print(f"click - clicking given xpath: {xpath} - {call_indication}", file=open('SAL_Logs.txt','a'))

    def main(self, path, comment):
        print("\n main - here we are at main. Calling get_homePage", file=open('SAL_Logs.txt','a'))
        self.get_homePage(path, comment)

    def first_comment(self, path, comment):
        fc_XPATH = '//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[3]/div/div[2]'
        fc_location = driver.find_element(By.XPATH, fc_XPATH)
        fc_XP_text = fc_location.get_attribute('innerHTML')
        if self.CURRENT_PAGE == 1 and self.FIRST_FIRST_PAGE_COMMENT == "":
            print(f"CURRENT PAGE == {self.CURRENT_PAGE}, fc becomes: {fc_XP_text}", file=open('SAL_Logs.txt','a'))
            self.FIRST_FIRST_PAGE_COMMENT = fc_XP_text
            self.search_comment(path, comment)
        elif self.CURRENT_PAGE != 1:
            print(f"Current page != 1, Comparing first comment with first comment from the first page", file=open('SAL_Logs.txt','a'))
            if fc_XP_text != self.FIRST_FIRST_PAGE_COMMENT and self.FIRST_FIRST_PAGE_COMMENT != "":
                # directing to search comment after checking the first comment on the first page
                print(f"directing to search comment after checking the first comment on the first page", file=open('SAL_Logs.txt','a'))
                print(f"first comment on this page is: {fc_XP_text} and the saved comment is: {self.FIRST_FIRST_PAGE_COMMENT}",  file=open('SAL_Logs.txt','a'))
                self.search_comment(path, comment)
            elif fc_XP_text == self.FIRST_FIRST_PAGE_COMMENT:
                print(f"directing to homepage after first comment on the page equals saved comment but the page is not none", file=open('SAL_Logs.txt','a'))
                self.FIRST_FIRST_PAGE_COMMENT = ""
                self.get_homePage(path, comment)
        elif self.CURRENT_PAGE != 1 and self.FIRST_FIRST_PAGE_COMMENT == "":
            print(f"directing to homepage - page is not 1 and comment is still null", file=open('SAL_Logs.txt','a'))
            self.get_homePage(path, comment)
    
    def engine(self, path, comment):
        while True:
            self.counter += 1 
            start_time = time.time()
            self.main(path, comment)
            end_time = time.time()
            total_time = end_time - start_time
            print(f"Time of looking the comment is equal to: {total_time} ",  file=open('SAL_Logs.txt','a'))
            print(f"Counter: {self.counter} ",  file=open('SAL_Logs.txt','a'))
        

SAL = Search_And_Like()

SAL.engine("jacek-kopczynski-ma-nowa-partnerke-nastepczyni-patrycji-markowskiej-potwierdza-ich-zwiazek-raczej-juz-tego-nie-ukryjemy-6859714963409600a", "Piękna dziewczyna .Markowska nie umie śpiewać , istnieje tylko dzięki znanemu ojcu.")
# while True:
#     counter += 1 
#     start_time = time.time()
#     SAL.main("jacek-kopczynski-ma-nowa-partnerke-nastepczyni-patrycji-markowskiej-potwierdza-ich-zwiazek-raczej-juz-tego-nie-ukryjemy-6859714963409600a", "Piękna dziewczyna .Markowska nie umie śpiewać , istnieje tylko dzięki znanemu ojcu.")
#     end_time = time.time()
#     total_time = end_time - start_time
#     print(f"Time of looking the comment is equal to: {total_time} ",  file=open('SAL_Logs.txt','a'))
#     print(f"Counter: {counter} ",  file=open('SAL_Logs.txt','a'))