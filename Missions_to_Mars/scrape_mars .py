#!/usr/bin/env python
# coding: utf-8

# ## Mission to Mars


get_ipython().system('pip install pymongo')


# Dependencies
from bs4 import BeautifulSoup as soup
import requests
import pymongo
from splinter import Browser 
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests


# ## Find the latest news title

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit site
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)

html = browser.html

# Convert browser to soup object
new_soup = soup(html, 'html.parser')

slide_element = new_soup.select_one("ul.item_list li.slide")

# Find the features news title
news_title = slide_element.find("div", class_="content_title").get_text()
print(news_title)

new_paragraph = slide_element.find("div", class_="list_text",).get_text()
print(new_paragraph)


# ## Find the Featured Image



# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit site
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)
browser.links.find_by_partial_text('FULL IMAGE').click()

html = browser.html
new_soup = soup(html, 'html.parser')

# find the full image
image_url = new_soup.find('img',attrs={'class':'fancybox-image'})['src']


# In[36]:


main_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'


# In[37]:


featured_image_url = main_url + image_url
print(featured_image_url)


# ## Mars Facts

# In[44]:


# Create url
mars_url = 'https://space-facts.com/mars/'

# Create dataframe
mars_df = pd.read_html(mars_url)[0]
mars_df


# In[45]:


mars_df.columns = ['Description', 'Value']
mars_df


# In[46]:


mars_df.set_index('Description', inplace=True)
mars_df


# In[47]:


mars_df.to_html()


# ## Mars Hemispheres

# In[57]:


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

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
    #Find the image tag and extrat
    sample_element = browser.links.find_by_text("Sample").first
    title = browser.find_by_css("h2.title").text
    link = sample_element["href"]
    
    hemisphere["Title"] = title
    hemisphere["Link"] = link
    
    hemisphere_image_urls.append(hemisphere)
    browser.back()
    
print(hemisphere_image_urls)


# In[58]:


browser.quit()


# In[ ]:



