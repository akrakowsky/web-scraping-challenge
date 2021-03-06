#!/usr/bin/env python
# coding: utf-8

# ## Mission to Mars


# Dependencies
from bs4 import BeautifulSoup as soup
import requests
from splinter import Browser 
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

def scrape_all():
    #executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, new_paragraph = mars_news(browser)
    
    data = {
        "news_title": news_title,
        "new_paragraph": new_paragraph,
        "featured_image": featured_image(browser),
        "mars_facts": mars_facts(),
        "hemispheres": hemispheres(browser)
    }
    browser.quit()
    return data

# Find the latest news title
def mars_news(browser):
    #executable path
    #executable_path = {'executable_path': ChromeDriverManager().install()}
    #browser = Browser('chrome', **executable_path, headless=False)
    # Visit site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    
    # Convert browser to soup object
    new_soup = soup(html, 'html.parser')

    try:
        slide_element = new_soup.select_one("ul.item_list li.slide")
        # Find the features news title
        news_title = slide_element.find("div", class_="content_title").get_text()
        print(news_title)

        new_paragraph = slide_element.find("div", class_="list_text",).get_text()
        print(new_paragraph)
        
    except:
        return None, None
    
    # browser.quit()
    return news_title, new_paragraph
    

# Find the Featured Image
def featured_image(browser):
    #executable path
    #executable_path = {'executable_path': ChromeDriverManager().install()}
    #browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    
    # Convert browser to soup object
    new_soup = soup(html, 'html.parser')

    try:
        
        # find the full image
        image_url = new_soup.find('img',attrs={'class':'fancybox-image'})['src']
    except:
        return None        
    main_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    featured_image_url = main_url + image_url
    
    # browser.quit()
    return featured_image_url


# Find Mars facts
def mars_facts():
    # Create dataframe
    mars_url = 'https://space-facts.com/mars/'
    mars_df = pd.read_html(mars_url)[0]
    mars_df.columns = ['Description', 'Value']
    mars_df.set_index('Description', inplace=True)
    
    return mars_df.to_html(classes="table table-striped")

# Find Mars Hemispheres
def hemispheres(browser):
    # Setup splinter
    #executable_path = {'executable_path': ChromeDriverManager().install()}
    #browser = Browser('chrome', **executable_path, headless=False)

    # List url
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    # Create html
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    # Make a list for the hemispheres
    hemisphere_image_urls = []

    # Find all of the hemispheres
    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        #Find the image tag and extract
        try:
            sample_element = browser.links.find_by_text("Sample").first
            title = browser.find_by_css("h2.title").text
            link = sample_element["href"]

            hemisphere["Title"] = title
            hemisphere["Link"] = link

            hemisphere_image_urls.append(hemisphere)
            browser.back()
        except:
            return None
        

    return hemisphere_image_urls

    #browser.quit()









