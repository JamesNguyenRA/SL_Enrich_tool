import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from time import sleep
import pyotp
import re
from bs4 import BeautifulSoup
from facebook_scraper import get_posts
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import json
import numpy as np
import dateparser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime,date


# Đoạn script này dùng để khởi tạo 1 chrome profile
def initDriverProfile():
    CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
    WINDOW_SIZE = "1000,2000"
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-gpu') if os.name == 'nt' else None  # Windows workaround
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-feature=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--ignore-certificate-error-spki-list")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControllered")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")  # open Browser in maximized mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_argument('disable-infobars')

    driver = webdriver.Chrome(executable_path='chromedriver',
                              options=chrome_options
                              )
    return driver


def checkLiveClone(driver):
    try:
        driver.get("https://mbasic.facebook.com/")
        time.sleep(2)
        # driver.get("https://mbasic.facebook.com/")
        # time.sleep(1)
        elementLive = driver.find_elements("name","view_post")
        if (len(elementLive) > 0):
            print("Live")
            return True

        return False
    except:
        print("view fb err")


def getCodeFrom2FA(code):
    totp = pyotp.TOTP(str(code).strip().replace(" ", "")[:32])
    time.sleep(random.randint(3,5))
    return totp.now()


def confirm2FA(driver):
    time.sleep(2)
    btnRadioClick = driver.find_element("css selector","section > section.x > div:nth-child(2) > div > div.y.ba > label > input[type=radio]").click()
    time.sleep(2)
    continueBntSubmit = driver.find_element("css selector","#checkpointSubmitButton-actual-button").click()


def loginBy2FA(driver, username, password, code):
    # changeMacAdrress()
    # changeIp4G()
    # readIp()
    driver.get("https://mbasic.facebook.com/login/?next&ref=dbl&fl&refid=8")
    sleep(5)
    userNameElement = driver.find_elements("css selector","#m_login_email")
    userNameElement[0].send_keys(username)
    time.sleep(2)
    passwordElement = driver.find_elements("css selector","#login_form > ul > li:nth-child(2) > section > input")
    passwordElement[0].send_keys(password)
    time.sleep(3)
    btnSubmit = driver.find_elements("css selector","#login_form > ul > li:nth-child(3) > input")
    btnSubmit[0].click()
    time.sleep(2)
    if len(code)>0 :
        faCodeElement = driver.find_elements("css selector","#approvals_code")
        faCodeElement[0].send_keys(str(getCodeFrom2FA(code)))
        time.sleep(random.randint(2,4))
        btn2fa = driver.find_elements("css selector","#checkpointSubmitButton-actual-button")
        btn2fa[0].click()
        confirm2FA(driver)
        btn2fa = driver.find_elements("css selector","#checkpointSubmitButton-actual-button")
        if (len(btn2fa) > 0):
            btn2fa[0].click()
            btn2faContinue = driver.find_elements("css selector","#checkpointSubmitButton-actual-button")
            if (len(btn2faContinue) > 0):
                btn2faContinue[0].click()
                confirm2FA(driver)
    # end login

# fileIds = 'post_ids.csv'
def readData(fileName):
    f = open(fileName, 'r', encoding='utf-8')
    # f.truncate(0)
    data = []
    for i, line in enumerate(f):
        try:
            line = repr(line)
            line = line[1:len(line) - 3]
            data.append(line)
        except:
            print("err")
    return data

def writeFileTxt(fileName, content, isNew):
    with open(fileName, 'a') as f1:
        if isNew:
            f1.truncate(0)
            f1.write("0000000000000000000000") ###### ignore first element
        f1.write(content + os.linesep)

def scroll_to_bottom(driver):
    old_position = 0
    new_position = 1
    while (new_position - old_position) > 0:
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # print("old: ",old_position)
        
        # time1 = time.time()
        # Sleep and Scroll
        time.sleep(random.randint(1,3))
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        time.sleep(random.randint(1,3))

        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        time.sleep(random.randint(1,3))

def scroll_dialog_to_bottom(driver):
    action1 = ActionChains(driver)

    # Get the list of share posts
    peopleWhoSharedThisTitle = driver.find_element(By.CSS_SELECTOR, '[aria-label="People who shared this"]')
    startOfList = peopleWhoSharedThisTitle.find_element(By.XPATH, './div[3]/div/div')
    pre_content_items = startOfList.find_elements(By.XPATH, "./div")
    endViewElement = pre_content_items[-3]
    pre_items_ct = len(pre_content_items[:-4])
    cur_items_ct = 0

    content_items = 0

    while True:
        action1.move_to_element(endViewElement)
        action1.pause(0)
        action1.perform()
        
        peopleWhoSharedThisTitle = driver.find_element(By.CSS_SELECTOR,'[aria-label="People who shared this"]')
        startOfList = peopleWhoSharedThisTitle.find_element(By.XPATH,'./div[3]/div/div')
        current_content_items = startOfList.find_elements(By.XPATH,"./div")
        print("current content: ",current_content_items)
        time.sleep(random.uniform(0.5, 1.5))  # Random sleep interval between 2.5 and 3.5 seconds
        cur_items_ct = len(current_content_items[:-4])
        print("Last posts count", pre_items_ct, "Current posts count", cur_items_ct)
        
        if pre_items_ct == cur_items_ct:
            print(pre_items_ct, cur_items_ct, "End")
            content_items = current_content_items
            break
        
        pre_items_ct = cur_items_ct
        
        lastCurrentItem = current_content_items[-3]
        action1.move_to_element(lastCurrentItem)
        action1.pause(0)
        action1.perform()
        
        time.sleep(3 + random.uniform(1, 3))  # Random sleep interval between 11 and 13 seconds
        
        endViewElement = current_content_items[:-4][-1]
    del action1
    return content_items
def get_crawling_infos(json_file):
    f = open(json_file,'r')
    info = json.load(f)
    return info

def convert_cookie(cookie):
    keys = []
    values = []
    # cookie_attr = str(cookie).split(': ')[-1].split('; ')
    cookie_attr = cookie.split('; ')

    for attr in cookie_attr:
        key,val = str(attr.split('=')[0]),str(attr.split('=')[-1])
        keys.append(key)
        values.append(val)
    cookie_out = str(dict(zip(keys,values)))
    cookie_out = cookie_out.replace("'",'"')
    # print(cookie_out)
    f = open("cookie.txt",'w+')
    f.write(cookie_out)
    # out = { "xs" : xs, "wd" : wd, "usida" : usida, "sb" : sb, "presence" : presence, "fr" : fr, "dpr" : dpr, "datr" : datr, "c_user" : c_user}

def save_to_excel(groupID,post_info,kw):
    if not os.path.isdir("result"):
        os.makedirs("result")
        
    username_list = post_info[0]
    userID_list = post_info[1]
    text_list = post_info[2]
    like_list = post_info[3]
    comment_list = post_info[4]
    share_list = post_info[5]
    post_url_list = post_info[6]
    date_list = post_info[7]

    groupID = "https://facebook.com/groups/" + groupID
    if not os.path.isfile(f"result/{kw}.xlsx"):
        out_dict = {"ID":groupID,"username":username_list,"user_id":userID_list,"text":text_list,"like":like_list,"comment":comment_list,"share":share_list,"post_url":post_url_list,"date":date_list}
        out_df = pd.DataFrame(out_dict)
        out_df.to_excel(f"result/{kw}.xlsx")
    else:
        gg_df = pd.read_excel(f"result/{kw}.xlsx",index_col=None)
        out_dict = {"ID":groupID,"username":username_list,"user_id":userID_list,"text":text_list,"like":like_list,"comment":comment_list,"share":share_list,"post_url":post_url_list,"date":date_list}
        out_df = pd.DataFrame(out_dict)
        gg_df = pd.concat([gg_df,out_df],ignore_index=True)
        gg_df = gg_df.iloc[:,1:]
        gg_df.to_excel(f"result/{kw}.xlsx")



def exclude_by_kw(ex_kws,content):
    if any([ex_kw in content.lower() for ex_kw in ex_kws]):
        return False
    else:
        return True

def crawl_post(post_id,start_d,end_d):
    time_sleep = random.randint(5,10)
    print(f"sleeping {time_sleep}s ...")
    time.sleep(time_sleep)
    post_info = [None,None,None,None,None,None,None,None]
    stop_crawl = False
    cookie = 'cookie.txt'
    POST_ID = np.array([post_id])
    post = get_posts(post_urls=POST_ID,cookies=cookie,options={"comments": 100, "progress": True})
    for post in post:
        time.sleep(random.randint(2,3))
        post_info[7] = post['time']
        if post['time'] > end_d:
            return None,None
        elif post['time']<=end_d and post['time']>=start_d:
            post_info[0] = post['username']
            post_info[1] = post['user_id']
            post_info[2] = post['text']
            post_info[3] = post['likes']
            post_info[4] = post['comments']
            post_info[5] = post['shares']
            post_url = "https://facebook.com/" + str(post['post_url']).split('/')[-1]
            post_info[6] = post_url
            post_info[7] = post['time'].date()
            return post_info,stop_crawl
        elif post['time']<start_d:
            # print("time: ",post['time'])
            stop_crawl = True
            return post_info,stop_crawl


def crawl_group(group_ID,kw,ex_kw1,ex_kw2,ex_kw3,filter_day_num):
    post_infos = [[],[],[],[],[],[],[],[]]
    ex_kws = [ex_kw1,ex_kw2,ex_kw3]
    group_ID = group_ID
    cookie = 'cookie.txt'
    posts = get_posts(group_ID,cookies=cookie,options={"comments": 100, "progress": True})
    for i,post in enumerate(posts):
        # if exclude_by_kw(ex_kws,post["text"]) and not exclude_by_date_range(filter_day_num,post):
        if kw in post['text'].lower():
            post_infos[0].append(post['username'])
            post_infos[1].append(post['user_id'])
            post_infos[2].append(post['text'])
            post_infos[3].append(post['likes'])
            post_infos[4].append(post['comments'])
            post_infos[5].append(post['shares'])
            post_url = "https://facebook.com/" + str(post['post_url']).split('/')[-1]
            post_infos[6].append(post_url)
            date = str(post['time']).split(' ')[0]
            post_infos[7].append(date)
            print(f"{len(post_infos[0])} posts crawled")

    return post_infos

def getPostsGroup(driver, groupids, search_kw,start_day,end_day):
    final_infos = [[],[],[],[],[],[],[],[]]
    post_collections = []
    for groupid in groupids:
        print("groupid: ",groupid)
        search_url = f'https://www.facebook.com/groups/{groupid}'
        driver.get(search_url)
        sleep(random.randint(2,4))
        search_btn = driver.find_element("css selector",'[aria-label="Search"]')
        search_btn.click()
        sleep(random.randint(2,3))
        enter_kw_btn = driver.find_element("css selector",'[aria-label="Search this group"]')
        enter_kw_btn.send_keys(f"{search_kw}" + Keys.RETURN)
        # enter_kw_btn.submit()
        sleep(2)
        mostRecent_btn = driver.find_element("css selector",'[aria-label="Most Recent"]')
        mostRecent_btn.click()
        sleep(2)

        scroll_to_bottom(driver)
        soup = BeautifulSoup(driver.page_source,"html.parser")
        
        for source in soup.find_all('a'):
            urls = source.get('href')
            if "set=pcb" in urls or "set=gm" in urls:
                post_id = str(re.findall('[0-9]+', str(urls))[1])
                if post_id not in post_collections:
                    post_collections.append(post_id)
                    post_mention,stop = crawl_post(post_id,start_day,end_day)
                    print(post_mention)
                    if stop is None:
                        continue
                    elif not stop:
                        for i in range(len(post_mention)):
                            final_infos[i].append(post_mention[i])
                    else:
                        print("stop!!!!!!!!!!!!!!! out of day range ")
                        break


    save_to_excel(groupid,final_infos,search_kw)

def get_post_share(driver,post_urls,start_day,end_day):
    final_infos = [[],[],[],[]]
    for url in post_urls:
        # print("groupid: ",groupid)
        driver.get(url)
        sleep(random.randint(3,5))
        share_btn = driver.find_element("xpath",'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[2]/div[3]')
        share_btn.click()
        sleep(random.randint(2,3))
        content_items = scroll_dialog_to_bottom(driver)
        print("READY TO CRAWL")
        sleep(1)
        for item in content_items[:-2]:
            # Retrieve the desired information for each content item
            username = item.find_element(By.CSS_SELECTOR, "span > a > strong > span").text
            
            # Get profile link
            raw_profile_link = item.find_element(By.CSS_SELECTOR, "span > a").get_attribute("href")
            profile_link = raw_profile_link.split("__cft__[0]")[0][:-1]
            
            # Get share post link
            temp = item.find_element(By.XPATH,"./div/div/div/div/div[2]/div/div[2]/div/div[2]/span/span/span[2]/span/a").get_attribute("outerHTML")
            soup = BeautifulSoup(temp)
            share_post_link = soup.find("a", href=True)["href"]
            share_post_link = share_post_link.split("__cft__[0]")[0][:-1]
            #share_post_url_elements = [i for i in share_post_link.replace("&amp","").split(";")[:2]]
            #share_post_url = "&".join(share_post_url_elements)
            
            
            datetime_str = item.find_element(By.CSS_SELECTOR, "span:nth-child(2) > span").text.strip().replace("\n", "")

            # Process the retrieved information as required
            print("Username:", username)
            print("Profile Link:", profile_link)
            print("Share Post Link:", share_post_link)
            shared_date = dateparser.parse(datetime_str)
            print("Share Time:", shared_date.strftime("%Y-%m-%d %H:%M:%S"))
        
            print("------------------------")
            if shared_date >= start_day and shared_date <= end_day:
                final_infos[0].append(username)
                final_infos[1].append(profile_link)
                final_infos[2].append(share_post_link)
                final_infos[3].append(shared_date.date())


    if not os.path.isdir("result"):
        os.makedirs("result")
        
    if not os.path.isfile(f"result/khainguyen_crisis.xlsx"):
        output_dict = {"username":final_infos[0],"profile_link":final_infos[1],"shared_link":final_infos[2],"shared_date":final_infos[3]}
        output_df = pd.DataFrame(output_dict)
        output_df.to_excel(f"result/khainguyen_crisis.xlsx")
    else:
        output_df = pd.read_excel(f"result/khainguyen_crisis.xlsx",index_col=None)
        output_dict = {"username":final_infos[0],"profile_link":final_infos[1],"shared_link":final_infos[2],"shared_date":final_infos[3]}
        out_df = pd.DataFrame(output_dict)
        output_df = pd.concat([output_df,out_df],ignore_index=True)
        output_df = output_df.iloc[:,1:]
        output_df.to_excel(f"result/khainguyen_crisis.xlsx")

def clonePostContent(driver, postId = "1902017913316274"):
    try:
        driver.get("https://m.facebook.com/" + str(postId))
        parrentImage = driver.find_element("xpath","//div[@data-gt='{\"tn\":\"E\"}']")
        if (len(parrentImage) == 0):
            parrentImage = driver.find_element("xpath","//div[@data-ft='{\"tn\":\"E\"}']")

        contentElement = driver.find_element("xpath","//div[@data-gt='{\"tn\":\"*s\"}']")
        if (len(contentElement) == 0):
            contentElement = driver.find_element("xpath","//div[@data-ft='{\"tn\":\"*s\"}']")

        #get Content if Have
        if (len(contentElement)):
            content = contentElement[0].text

        #get Image if have
        linksArr = []
        if (len(parrentImage)):
            childsImage = parrentImage[0].find_element("xpath",".//*")
            for childLink in childsImage:
                linkImage = childLink.get_attribute('href')
                if (linkImage != None):
                    linksArr.append(linkImage.replace("m.facebook", "mbasic.facebook"))
        linkImgsArr = []
        if (len(linksArr)):
            linkImgsArr = []
            for link in linksArr:
                driver.get(link)
                linkImg = driver.find_element("xpath",'//*[@id="MPhotoContent"]/div[1]/div[2]/span/div/span/a[1]')
                linkImgsArr.append(linkImg[0].get_attribute('href'))

        postData = {"post_id": postId, "content" : "", "images": []}

        if (len(linkImgsArr)):
            postData["images"] = linkImgsArr
        if (len(contentElement)):
            postData["content"] = content
        print(postData)
        return postData
    except:
        return False
        print("Fail clone Post")

def writeFileTxtPost(fileName, content, idPost, pathImg="/img/"):
    pathImage = os.getcwd() + pathImg + str(idPost)
    with open(os.path.join(pathImage, fileName), 'a') as f1:
        f1.write(content + os.linesep)

def download_file(url, localFileNameParam = "", idPost = "123456", pathName = "/data/"):
    try:
        if not os.path.exists(pathName.replace('/', '')):
            os.mkdir(pathName.replace('/', ''))

        local_filename = url.split('/')[-1]
        if local_filename:
            local_filename = localFileNameParam
        with requests.get(url, stream=True) as r:
            pathImage = os.getcwd() + pathName + str(idPost)

            if (os.path.exists(pathImage) == False):
                os.mkdir(pathImage)

            with open(os.path.join(pathImage, local_filename), 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    except:
        print("download file err")

import random
def joinGroup(driver, idGoup):
    try:
        driver.get("https://mbasic.facebook.com/groups/" + idGoup)
        sleep(random.randint(1,5))
        isJoined = driver.find_element("xpath",'//a[contains(@href, "cancelgroup")]')
        if (len(isJoined) == 0):
            sleep(1)
            driver.find_element("css selector","#root > div.bj > form > input.bu.bv.bw")[0].click()
            sleep(1)
            textea = driver.find_element("tag name","textarea")

            if (len(textea) > 0):
                for el in textea:
                    sleep(1)
                    el.send_keys("oki admin ")
            sleep(1)
            btnSubmit = driver.find_element("css selector","#group-membership-criteria-answer-form > div > div > input")

            if (len(btnSubmit)):
                btnSubmit[0].click()
                sleep(random.randint(3,8))
        else:
            print("joined")
    except:
        print("error join!")


def crawlPostData(driver, postIds, type = 'page'):
    folderPath = "/data_crawl/"
    for id in postIds:
        try:
            time.sleep(2)
            dataPost = clonePostContent(driver, id)
            dataImage = []
            if (dataPost != False and len(dataPost["images"])):
                if (type == 'group'):
                    for img in dataPost["images"]:
                        driver.get(img)
                        dataImage.append(driver.current_url)
                else:
                    dataImage = dataPost["images"]

                postId = str(dataPost['post_id'])
                postContent = str(dataPost['content'])
                stt = 0
                for img in dataImage:
                    stt += 1
                    download_file(img, str(stt), postId, folderPath)
                writeFileTxt('post_crawl.csv', str(id))
                writeFileTxtPost('content.csv', postContent, postId, folderPath)
        except:
            print("crawl fail")



