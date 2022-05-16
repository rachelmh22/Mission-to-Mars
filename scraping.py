
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

def scrape_all():
    
     # Initiate headless driver for deployment

    #Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now(),
          "hemispheres":hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    #url = 'https://redplanetscience.com'
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    #slide_elem = news_soup.select_one('div.list_text')

    #slide_elem.find('div', class_='content_title')

    # Use the parent element to find the first `a` tag and save it as `news_title`
    #news_title = slide_elem.find('div', class_='content_title').get_text()

    # Use the parent element to find the paragraph text
    #news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    return news_title, news_p
    
# ### Featured Images

def featured_image(browser):

    # Visit URL
    #url = 'https://spaceimages-mars.com'
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Find the relative image url
    #img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    #img_url_rel

    # Use the base URL to create an absolute URL
    #img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    #img_url

    return img_url

### Mars Facts

def mars_facts():

    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        #df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None


#df = pd.read_html('https://galaxyfacts-mars.com')[0]
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
#df
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

#browser.quit()

def hemispheres(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        
        hemispheres = {}
        
        browser.find_by_css('a.product-item h3')[i].click()
        full_image_element = browser.links.find_by_text('Sample').first
        img_url = full_image_element['href']
        title = browser.find_by_css("h2.title").text
        hemispheres["img_url"] = img_url
        hemispheres["title"] = title
        image_urls.append(hemispheres)
        browser.back()

    return image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

