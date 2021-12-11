# import dependencies
import pandas as pd
from bs4 import BeautifulSoup
import pymongo
import requests
from splinter import Browser
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape_info():

    # Setup splinter
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL for the NASA news site
    url = "https://redplanetscience.com"
    browser.visit(url)

    time.sleep(1)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # news title loc and class
    news_title = soup.find_all('div', class_='content_title')

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # news paragraph location and class
    news_p = soup.find_all('div', class_='article_teaser_body')

    # URL for the featured space image site
    featured_url = "https://spaceimages-mars.com/"
    browser.visit(featured_url)

    time.sleep(1)

    # Create BeautifulSoup object; parse with 'html.parser'

    featured_html = browser.html
    featured_soup = BeautifulSoup(featured_html, 'html.parser')

    # featured image loc and class
    featured_image = featured_soup.find(
        'img', class_='headerimage fade-in')["src"]

    # featured image url variable to print out the image loc

    featured_image_url = featured_url + featured_image

    # URL for Mars facts
    mars_url = "https://galaxyfacts-mars.com"
    # Read in the html table
    table = pd.read_html(mars_url)

    table[1]
    # Set the column names and only display Mars Values
    df = table[1]
    df.columns = ["Description", "Value"]
    df.set_index("Description", inplace=True)

    # Save file as HTML table
    df.to_html("mars_table.html")

    # URL to get the high resolution images
    url_hemisphere = 'https://marshemispheres.com/'
    browser.visit(url_hemisphere)

    time.sleep(1)

    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')

    hemisphere = hemisphere_soup.find('div', class_='collapsible results')

    all_hemispheres = hemisphere.find_all('div', class_='item')

    images_titles = []

    for individual in all_hemispheres:
        img_title = individual.find('h3').text
#     h_image=individual.find('a',class_='downloads')['href']

        image_url = individual.find('img', class_='thumb')['src']
        image_src = url_hemisphere + image_url
    # Define the hemispehere dictionary and set the values
        hemisphere_dict = {}
        hemisphere_dict["title"] = img_title
        hemisphere_dict["img_url"] = image_src

        images_titles.append(hemisphere_dict)
# Define a dictionary that will hold all the data from info above
    everything_dict = {
        "News_Title": news_title,
        "News_Paragraphs": news_p,
        "Featured_Image": featured_image,
        "Facts_Table": table,
        "Image_title_link": images_titles
    }

# Quite the browser after scraping
    browser.quit()

# Return results
    return everything_dict
