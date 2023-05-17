from selenium import webdriver
import re
import os
from datetime import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup


def get_title_url(search_forum,post_html):
    title_tag = post_html.find('a',class_='search-link')
    url = search_forum + title_tag.get('href')
    for tag in title_tag.find('span',class_='ember-view'):
        title = tag.get_text() 
         
    return title,url

def get_author(search_forum,post_html):
    for tag_a in post_html.find_all('a'):
        a = tag_a.get('href')
        if "member" in a:
            return search_forum + a

def get_date(post_html):
    date = post_html.find('span',class_='relative-date').get('title')
    day_numerics = re.findall('[0-9]+', str(date))
    date = day_numerics[0] + '/' + day_numerics[1] + '/' + day_numerics[2][-2:]
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

def _run_247(search_kw,start_day,end_day):
    domain = "f247"
    search_forum = f"https://{domain}.com/"
    # search_kw = "dragon+capital"
    driver = webdriver.Chrome()
    post_url_list = []
    post_title_list = []
    date_list = []

    search_query = search_forum + f'search?q={search_kw}%20order%3Alatest'
    driver.get(search_query)
    time.sleep(3)
    scroll_to_bottom(driver)
    soup = None

    if soup is None:
        soup = BeautifulSoup(driver.page_source,'html.parser')
    posts = soup.find_all('div',class_= 'fps-topic')

    # print(len(posts))
    for post in posts:
        post_day = datetime.strptime(get_date(post),'%d/%m/%y').date()
        if post_day > start_day and post_day < end_day:
            post_title_list.append(get_title_url(search_forum,post)[0])
            post_url_list.append(get_title_url(search_forum,post)[1])
            date_list.append(str(post_day))

    ############# save to excel
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
        gg_df.to_excel(f"result/forums_{search_kw}.xlsx")

    driver.close()