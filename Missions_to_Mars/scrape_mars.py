from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

mars_data = {}

def scrape():
    browser= init_browser()


    news_url ="https://mars.nasa.gov/news"
    browser.visit(news_url)

    time.sleep(1)

    html=browser.html
    soup= bs(html,"html.parser")

    article_title = soup.find("div", class_="list_text").text
    article_paragraph = soup.find("div", class_="article_teaser_body").text

    mars_data["Article_Title"] = article_title
    mars_data["Article_Paragraph"] = article_paragraph

    image_url= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)    
    html=browser.html
    soup=bs(html,"html.parser")

    time.sleep(2)

    image= soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov/" + image

    mars_data["Featured_Image_URL"] = featured_image_url

    weather_url= "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    html= browser.html
    soup=bs(html,"html.parser")

    time.sleep(2)
    
    weather= soup.find("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").text

    mars_data["Weather"] = weather

    facts_url ="https://space-facts.com/mars/"
    browser.visit(facts_url)

    time.sleep(2)

    mars_dt = pd.read_html(facts_url)
    mars_df= pd.DataFrame(mars_dt)
    mars_html = mars_df.to_html(header=False, index=False)

    mars_data["Mars_Facts"] = mars_html

    hemispheres_url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=mars"
    browser.visit(hemispheres_url)
    html=browser.html
    soup=bs(html,"html.parser")

    time.sleep(2)

    hemisphere_image_url=[]
    hemispheres= soup.find_all("div", class_="item")

    for h in hemispheres:
        title = h.find("h3")
        hemi_url = h.find("a", class_="itemLink product-item")["href"]
        final_url = "https://astrogeology.usgs.gov" + hemi_url
        browser.visit(final_url)
        html= browser.html
        soup=bs(html, "html.parser")
        download = soup.find("div", class_="downloads")
        image_url= download.find("a")["href"]
        hemisphere_image_url.append({"Title" : title, "Image_url" : image_url})

    mars_data["Hemispheres"] = hemisphere_image_url

    browser.quit()

    return mars_data