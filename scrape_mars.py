#Dependencies
from splinter import Browser
import time
# Parses the HTML
from bs4 import BeautifulSoup
import pandas as pd
import pymongo

# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Setup splinter
    url = 'https://redplanetscience.com/'
    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    #Retrieve the latest News Title and Paragraph Text
    news_title = news_soup.find('div', class_='content_title').text
    news_p = news_soup.find('div', class_='article_teaser_body').text
    
    #Mars Space Images—Featured
    url_2 = 'https://spaceimages-mars.com'
    
    # executable_path = {'executable_path' : ChromeDriverManager().install()}
    # browser = Browser("chrome", **executable_path, headless=False)
    
    browser.visit(url_2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    images = soup.find("img", class_="headerimage fade-in")["src"]
    featured_image_url =  "https://spaceimages-mars.com/" + images
    
    #Mars fact
    url_3 = "https://galaxyfacts-mars.com"
    table = pd.read_html(url_3)
    mars_df = table[0]
    mars_df.rename(columns={0: "Description", 1: "Mars_info", 2: "Earth_info"}, inplace=True)
    
    mars_html_table = mars_df.to_html(header=True)
    
    #Mars Hemisphere
    hemi_url = 'https://marshemispheres.com/'

    # executable_path = {'executable_path' : ChromeDriverManager().install()}
    # browser = Browser("chrome", **executable_path, headless=False)

    browser.visit(hemi_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Mars hemispheres products data
    all_mars_hemispheres = soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

    hemisphere_image_urls = []

    # Iterate through each hemisphere data
    for i in mars_hemispheres:
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(hemi_url + hemisphere_link)
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')

        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = hemi_url + image_url

        hemisphere_image_urls.append(image_dict)

    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
    }
   
    browser.quit()

    # Return results
    return mars_dict

