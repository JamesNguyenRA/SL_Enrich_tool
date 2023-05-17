from selenium import webdriver
import re
import os
import time
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup


def get_date_id(driver,search_forum,search_kw):
    search_page = search_forum + 'search/?type=post'
    driver.get(search_page)
    time.sleep(2)
    kw_box = driver.find_element("xpath", '//*[@id="ctrl_keywords"]')
    kw_box.send_keys(search_kw.replace('+',' '))
    time.sleep(1)
    search_btn = driver.find_element("xpath", '//*[@id="content"]/div/div/form[1]/dl[4]/dd/input')
    search_btn.click() 
    time.sleep(2)
    page_url = driver.current_url
    date_id = str(re.findall('[0-9]+', str(page_url))[1])

    return date_id

def get_title_url(search_forum,post_html):
    title_tag = post_html.find('h3',class_='title')
    title = title_tag.get_text()# get('href')
    for tag in title_tag:
        url = search_forum + tag.get('href')   
         
    return title,url

def get_author(search_forum,post_html):
    for tag_a in post_html.find_all('a'):
        a = tag_a.get('href')
        if "member" in a:
            return search_forum + a

def get_date(post_html):
    try:
        date = post_html.find('abbr',class_='DateTime').get('data-datestring')
    except:
        date = post_html.find('span',class_='DateTime').get_text()
    ele = date.split("/")
    date = ele[0] + "/" + ele[1] + "/" + ele[2][-2:]
    return date
    
def scroll_to_bottom(driver):

    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))

def _run_319(search_kw,num_page,start_day,end_day):
    domain = "f319"
    search_forum = f"https://{domain}.com/"
    # search_kw = "dragon+capital"
    max_page = int(num_page) if num_page is not None else 1
    driver = webdriver.Chrome()
    date_id = get_date_id(driver,search_forum,search_kw)
    driver = webdriver.Chrome()
    # https://f319.com/search/368472957/?q=DC&t=post&o=date
    post_url_list = []
    post_title_list = []
    # author_list = []
    date_list = []
    for i in range(max_page):
        current_page = i+1
        search_query = search_forum + f'search/{date_id}/?page={current_page}&?q={search_kw}&t=post&o=date'
        # driver.get("https://www.google.com/search?q=" + query)
        driver.get(search_query)
        time.sleep(4)
        scroll_to_bottom(driver)
        soup = None
        
        if soup is None:
            soup = BeautifulSoup(driver.page_source,'html.parser')
        posts = soup.find_all('li',class_= 'searchResult')

        # print(len(posts))
        for post in posts:
            post_day = datetime.strptime(get_date(post),'%d/%m/%y').date()
            if post_day > start_day and post_day < end_day:
                post_title_list.append(get_title_url(search_forum,post)[0])
                post_url_list.append(get_title_url(search_forum,post)[1])
                date_list.append(get_date(post))

    ############# save to excel
    # keyword_list = [search_kw]*len(date_list)
    forums_list = [search_forum]*len(date_list)

    if not os.path.isfile(f"result/forums_{search_kw}.xlsx"):
        out_dict = {"forum":forums_list,"title":post_title_list,"url":post_url_list,"date":date_list}
        out_df = pd.DataFrame(out_dict)
        out_df.to_excel(f"result/forums_{search_kw}.xlsx")
    else:
        gg_df = pd.read_excel(f"result/forums_{search_kw}.xlsx",index_col=None)
        out_dict = {"forum":forums_list,"title":post_title_list,"url":post_url_list,"date":date_list}
        out_df = pd.DataFrame(out_dict)
        gg_df = pd.concat([gg_df,out_df],ignore_index=True)
        gg_df = gg_df.iloc[:,1:]
        # gg_df.drop()
        gg_df.to_excel(f"result/forums_{search_kw}.xlsx")


    driver.close()