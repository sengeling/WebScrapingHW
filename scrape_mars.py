# Import dependencies
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests
import pymongo
import os
from time import sleep


# # NASA Mars News

# Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.


# Splinter/chromedriver
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Define the url and visit the url via splinter
    article_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(article_url)

    # Sleep to let page load
    sleep(1)

    # Navigate into the first article
    browser.find_link_by_text("Curiosity Tastes First Sample in 'Clay-Bearing Unit'").first.click()

    # Html and BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html)

    # Pull the news title
    news_title = soup.find('h1', class_="article_title").text

    # Clean the line breaks from the title
    news_title = news_title.replace('\n', '')

    # ID the div where the paragraphs (p) are
    all_p = soup.find('div', class_='wysiwyg_content')

    # Get the 1st paragraph
    news_p = all_p.find('p').text


    # # JPL Mars Space Images - Featured Image

    # * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    # * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
    # * Make sure to find the image url to the full size `.jpg` image.
    # * Make sure to save a complete url string for this image.

    # Define the url and visit the url via splinter
    feat_image_url = 'https://www.jpl.nasa.gov'
    browser.visit(feat_image_url)

    # Sleep to let page load
    sleep(1)

    # Select the images link on the page to reveal and images button
    browser.click_link_by_partial_text('Images')

    # Sleep to let the page load
    sleep(2)

    # Click to the images section
    browser.click_link_by_href('/images')

    # Sleep to let the page load
    sleep(1)

    # Click to show the full image
    browser.click_link_by_partial_text('FULL IMAGE')

    # Sleep to let the page load
    sleep(2)

    # click more info to get to the biggest version of the image
    browser.find_link_by_text('more info     ').first.click()

    # Sleep to let the page load
    sleep(1)

    # Html and BeautifulSoup again since you changed pages
    html = browser.html
    soup = BeautifulSoup(html)

    # Sleep to let the page load
    sleep(1)

    # Find where the image is kept in the code
    fig_img = soup.find('figure', class_='lede')

    # Find the relative image path
    relative_image_path = fig_img.find('a')["href"]

    # Combine the base and relative url to get the image url
    featured_image_url = feat_image_url + relative_image_path


    # # Mars Weather

    # * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.

    # Define the url and visit the url via splinter
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Sleep to let page load
    sleep(1)

    # Html and BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html)

    # Find the div of the first tweet
    first_tweet_div = soup.find('div', class_='js-tweet-text-container')

    # Pull the text from the tweet
    mars_weather = first_tweet_div.find('p').text

    # Remove the last 26 characters from the text, which is a pic
    mars_weather = mars_weather[:-26]

    # Clean up the breaks and replace them with commas
    mars_weather = mars_weather.replace('\n', ', ')


    # # Mars Facts

    # * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # * Use Pandas to convert the data to a HTML table string.

    # Define the url
    url = 'https://space-facts.com/mars/'

    # Pandas reads the tables on the site
    tables = pd.read_html(url)

    # Define the table wanted as df
    df = tables[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description', inplace=True)

    # Transform the df to an html table
    mars_html_table = df.to_html()

    # Clean the breaks out of the html table
    mars_html_table = mars_html_table.replace('\n', '')


    # # Mars Hemispheres

    # * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    # * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    # Define the url and visit the url via splinter
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Sleep to let page load
    sleep(1)

    #Html and BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html)

    # Loop the page to get the hemisphere titles
    hemispheres = []
    for h3 in soup.find_all('h3'):
        hemispheres.append(h3.get_text())

    # Define an empty list to store the 4 dictionaries of titles and image urls
    hemisphere_image_urls = []

    # Loop the hemispher titles and get the image urls for each
    for hemisphere in hemispheres:

        browser.click_link_by_partial_text(hemisphere)

        sleep(2)

        html = browser.html
        soup = BeautifulSoup(html)

        div = soup.find('div', class_='downloads')

        list_1 = div.find('li')

        pic_url = list_1.a['href']

        hemisphere_image_urls.append({'title': hemisphere, 'img_url': pic_url})

        sleep(2)

        browser.back()

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser
    browser.quit()
    
    # Return results
    return mars_data