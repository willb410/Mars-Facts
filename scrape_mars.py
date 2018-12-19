def scrape():
    # Dependencies
    from bs4 import BeautifulSoup
    import html5lib
    import requests
    from splinter import Browser
    from splinter.exceptions import ElementDoesNotExist
    import time
    import pandas as pd

    # Splinter setup
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    ##########################################################################
    # Nasa Mars News                                                         
    ##########################################################################

    # Retrieve relevant html
    url = ('https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest')
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find('div', class_ = 'image_and_description_container')

    # Save title and description 
    news_title = result.find('div', class_ = 'content_title').text
    news_p = result.find('div', class_ = 'article_teaser_body').text


    ##########################################################################
    # JPL Mars Space Images - Featured Image
    ##########################################################################

    # Retrieve relevant html
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    browser.click_link_by_id('full_image')
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html5lib')

    # Save the featured image URL
    images = soup.find_all('img', class_ = 'fancybox-image')
    for image in images:
        featured = image['src']
    featured
    featured_image = 'https://www.jpl.nasa.gov' + featured

    # Close browser instance
    browser.quit()
    ##########################################################################
    # Mars Weather
    ##########################################################################

    # Scrape html from Mars Weather Twitter account
    url = ('https://twitter.com/marswxreport?lang=en')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Pull text from latest tweet about Mars weather
    mars_tweet = soup.find('p', class_ = 'tweet-text').text

    ##########################################################################
    # Mars Facts
    ##########################################################################


    # Retrieve the specified page html
    url = ('https://space-facts.com/mars/')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Pull the table into pandas and convert back to html
    mars_facts_df = pd.read_html(url)
    mars_facts_df = mars_facts_df[0]
    mars_facts_html = mars_facts_df.to_html()
    mars_facts_html = mars_facts_html.replace('\n', '')

    ##########################################################################
    # ### Mars Hemispheres
    ##########################################################################

    # Define URLs for images
    Cerberus = 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'
    Schiaparelli = 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'
    Syrtis_Major = 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'
    Valles_Marineris = 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'

    # Save information as dictionaries
    hemisphere_image_urls = [{'title':'Cerberus Hemisphere', 'img_url':Cerberus}, 
                            {'title':'Schiaparelli Hemisphere', 'img_url':Schiaparelli}, 
                            {'title':'Syrtis Major Hemisphere', 'img_url':Syrtis_Major}, 
                            {'title':'Valles Marineris Hemisphere', 'img_url':Valles_Marineris}]


    # Save outputs as dictionaries
    return {'news_title': news_title,
            'news_p': news_p,
            'featured_image':featured_image,
            'mars_tweet':mars_tweet,
            'mars_facts_html':mars_facts_html,
            'hemisphere_image_urls':hemisphere_image_urls}
