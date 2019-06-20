# Initiating the task by using BeautifulSoup, Pandas, and Requests/Splinter to scrap NASA Mars news site
# import Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
import time


# #### Part I. NASA Mars News
# 
# First, scrape the lastest News (Title and Text content) from NASA Mars News Site

# Define scrape function
def scrape():
    # Create a library that holds all the Mars' Data
    mars_library = {}

    # Execute Chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)

    # URL of NASA Mars News to be scraped
    url_1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    #Visit the page using the browser
    browser.visit(url_1)
    # assign html content
    html = browser.html
    # Create a Beautiful Soup object
    soup_1 = bs(html, "html.parser")


    # Assign the title to variables
    news_title = soup_1.find_all('div', class_='content_title')[0].find('a').text.strip()
    # Assign the text content to variables
    news_p = soup_1.find_all('div', class_='rollover_description_inner')[0].text.strip()
    # assign scrapped objects into Lib
    mars_library['news_title'] = news_title
    mars_library['news_p'] = news_p


    # #### Part II. PL Mars Space Images - Featured Image
    # URL of JPL Mars pictures to be scraped
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #Visit the JPL website
    browser.visit(url_2)
    # assign html content
    html = browser.html
    # Create a new Beautiful Soup object
    soup_2 = bs(html, 'html.parser')
    # Find and execute the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find more picture objects by clicking on "more info" button
    browser.is_element_present_by_text('more info', wait_time=10)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # retrieve image's url address
    img_url_partial = soup_2.find_all('a', class_='fancybox')[0].get('data-fancybox-href').strip()
    # combine image url and JPL url
    image_url = "https://www.jpl.nasa.gov"+img_url_partial

    mars_library['image_url'] = image_url


    # #### Part III. Mars Weather
    # 
    # Load URL of Mars Weather twitter account
    url_3 = 'https://twitter.com/marswxreport?lang=en'

    #Visit the Mars Weather twitter account
    browser.visit(url_3)
   # assign html content
    html = browser.html
    # Create a Beautiful Soup object
    soup_3 = bs(html, 'html.parser')

    #scrap latest Mars weather tweet
    mars_weather = soup_3.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text
    mars_library['mars_weather'] = mars_weather


    # #### Part IV. Mars Facts
    #
    # URL of Mars Facts webpage to be scraped
    url_4 = 'https://space-facts.com/mars/'

    profile_table = pd.read_html(url_4)
    # convert table info into dataframe
    df = profile_table[0]
    # rename the columns
    df.columns=['description','value']

    #Set the index to the description column
    df.set_index('description', inplace=True)
    # Deploy the DataFrame to HTML
    mars_facts = df.to_html('MarsFactsTable.html')
    mars_library['mars_facts'] = mars_facts


    # #### Part V. Mars Hemisperes
    # 
    # URL of USGS Astrogeology site
    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #Visit USGS Astrogeology site
    browser.visit(url_5)
    # # assign html content
    # html = browser.html
    # # Create a new Beautiful Soup object
    # soup_5 = bs(html, 'html.parser')
    # # get all the title
    # results = soup_5.find_all('h3')

    # assign image objects to a new list
    hemisphere_images = []

    # Get a list of all of the hemisphere images
    links = browser.find_by_css("a.product-item h3")

    # Loop through all the links, find the anchor and return the "href"
    for i in range(len(links)):
        hemisphere = {}
        
        # Find the elements on each loop
        browser.find_by_css("a.product-item h3")[i].click()
        # locate image anchor tag and extract the href
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']

        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
        # Append hemisphere image objects to the list
        hemisphere_images.append(hemisphere)
        
        # navigate back
        browser.back()

    # review saved images List
    hemisphere_images

    mars_library['hemisphere_images'] = hemisphere_images

    # Return Library
    return mars_library
    