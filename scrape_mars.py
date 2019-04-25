from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd



def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()  
    url1 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    articles_title = soup.find_all('div', class_='content_title')
    news_title = articles_title[0].text
    articles_paragraph = soup.find_all('div', class_='article_teaser_body')
    news_p = articles_paragraph[0].text
 
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('article', class_='carousel_item')
    for image in images:
        link = image.find("a")
        href = link["data-fancybox-href"]
        featured_image_url = f"https://www.jpl.nasa.gov/{href}"
    
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    weathers = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather = weathers[0].text

    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('div', class_='description')
    link_list = []

    hemisphere_image_urls = []

    for article in articles:
        a = article.find('a')
        href = a["href"]
        links = f"https://astrogeology.usgs.gov{href}"
        link_list.append(links)

    for link in link_list:
        browser.visit(link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        images = soup.find_all('div', class_='container')
        for image in images:
            img = {}
            image_link = image.find("img", class_="wide-image")
            image_link_src = image_link["src"]
            img_full_link = f"https://astrogeology.usgs.gov{image_link_src}"
            image_title = image.find("h2", class_="title").text

            img["title"] = image_title
            img["img_url"] = img_full_link

            hemisphere_image_urls.append(img)

    # url4 = "http://space-facts.com/mars/"
    # browser.visit(url4)
    # tables = pd.read_html(url4)
    # df_mars_facts = tables[0]
    # df_mars_facts.columns = ["information", "values"]
    

       

    
    

    mars_data = {
        "hemisphere_image_urls": hemisphere_image_urls,
        "news_title" : news_title,
        "news_p" : news_p,
        "featured_image_url": featured_image_url,
        "mars_weather" : mars_weather
        # "df_mars_facts": df_mars_facts

    }

    browser.quit()
  
    return mars_data
    
