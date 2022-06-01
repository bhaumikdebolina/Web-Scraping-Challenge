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
    soup = BeautifulSoup(html, 'html.parser')
    
    #Retrieve the latest News Title and Paragraph Text
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    #Mars Space Images—Featured
    url_2 = 'https://spaceimages-mars.com'
    
    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    
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

    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    
    browser.visit(hemi_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #all_mars_hemispheres = soup.find('div', class_='collapsible results')
    #mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')
    #mars_hemispheres= soup.find_all("div", class_="item")
    #hemisphere_image_urls = []
    #for i in mars_hemispheres:
        #image_dict = {}
        #titles = i.find('h3').text
        #end_link = i.find("a")["href"]
        #image_link = "https://marshemispheres.com/" + end_link
        #browser.visit(image_link)
        #html = browser.html
        #soup= bs(html, "html.parser")
        #downloads = soup.find("div", class_="downloads")
        #image_url = downloads.find("a")["href"]
        #image_dict['title']= titles
        #image_dict['image_url']= image_url
        #hemisphere_image_urls.append(image_dict)


    # Iterate through each hemisphere data
    #for i in mars_hemispheres:
        #hemisphere = i.find('div', class_="description")
        #title = hemisphere.h3.text        
        # Collect image link by browsing to hemisphere page
        #hemisphere_link = hemisphere.a["href"]    
        #browser.visit(hemi_url + hemisphere_link)        
        #image_html = browser.html
        #image_soup = BeautifulSoup(image_html, 'html.parser')        
        #image_link = image_soup.find('div', class_='downloads')
        #image_url = image_link.find('li').a['href']
        # Create Dictionary to store title and url info
        
        #image_dict = {}
        #image_dict['title'] = title
        #image_dict['img_url'] = image_url        
        #hemisphere_image_urls.append(image_dict)

    #hemisphere_image_url = []

    # Iterate through each hemisphere data
    
    hemisphere_dict = {}
    hemisphere = i.find('div', class_="description")
    title = hemisphere.h3.text

    img_link = i.find("div", class_ = "description").a["href"]
    base_url = 'https://marshemispheres.com/'
    visit_link = base_url + img_link
    browser.visit(visit_link)


    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')
    image_url = image_soup.find("img", class_ = "wide-image")["src"]
    img_url = base_url + image_url


    # Create Dictionary to store title and url info
    hemisphere_dict['title'] = title
    hemisphere_dict['image_url'] = img_url

    #hemisphere_image_url.append(hemisphere_dict)
                

    # Mars 
    mars_dict = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "fact_table": str(mars_html_table),
            "hemisphere_images": hemisphere_image_url,
            "last_modified": dt.datetime.now()
            
    }
    return mars_dict
print(scrape())
  
    
    
    
    
    