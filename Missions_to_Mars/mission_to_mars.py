from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import time

def scrape_mars():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)
    soup = BeautifulSoup(browser.html, 'html.parser')

    results = soup.find('li',class_='slide')

    # scraping the title
    # article_title = results.find('div',class_='content_title').find("a").text
    article_title = results.find('div',class_='content_title').find("a").get_text()

    # scrape p text
    p_text = results.find('div', class_='article_teaser_body').text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # browser.quit()
    browser.visit(url)

    browser.links.find_by_partial_href('/images').click()

    soup = BeautifulSoup(browser.html,'html.parser')

    featured_img = soup.find('img',class_='BaseImage')['src']

    url = 'https://space-facts.com/mars/'
    # browser.quit()
    browser.visit(url)

    mars_facts = pd.read_html(url)
    mars_facts[0]

    mars_df = mars_facts[0]
    mars_df.columns = ['attributes','content']
    mars_df

    mars_html_string = mars_df.to_html(index=False, classes="table table-striped")
    mars_html_string

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # browser.quit()
    browser.visit(url)

    soup = BeautifulSoup(browser.html,'html.parser')

    results = soup.find_all('div', class_='item')

    hemi_image_url = []
    for result in results:
        hemi_dict={}
        title = result.find('h3').text
        word = title.split(" ",1)[0]
        browser.click_link_by_partial_text(word)
        time.sleep(3)
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        img_url = soup.find('div',class_='downloads').find('a')['href']
        hemi_dict["title"] = title
        hemi_dict["img_url"] = img_url
        hemi_image_url.append(hemi_dict)
        browser.back()
        time.sleep(2)

    browser.quit()

    output = {"news_title":article_title,"featured_img":featured_img,"news_p":p_text,"mars_facts":mars_html_string,"hemisphere_imgs_url":hemi_image_url}

    return output
