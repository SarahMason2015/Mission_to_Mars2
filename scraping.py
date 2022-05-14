
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    #headless is whether use can see the work, if True, then it's in the background

    news_title, news_paragraph = mars_news(browser)
    hemispheres = martian_hemispheres(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        'hemispheres': hemispheres,
        'last_modified' : dt.datetime.now()
    }

    browser.quit()
    return data

def mars_news(browser):
#(browser) tells python to bring in the variable defined outside the function

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    #wait_time gives the browser 1 second to load the page
    #is-element_present_by_css directs to combination of <div> and <list_text> instead of separate directions


    html = browser.html
    news_soup = soup(html, 'html.parser')

        # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        #Note the . between div and list_text. It sets up the different classes of <div>
        # select_one shows that only 1 example will be chosen

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    #book has here url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Find the relative image url
    #img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    #get('src') gets the link to the pic. Note that this doesn't include the full link

    # Use the base URL to create an absolute URL
# =============================================================================
    try:
    # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
# # =============================================================================
#This is how to get the full address
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():

    try:
        #use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html(classes="table table-striped")
    #this will put the df back into html format

def martian_hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 3a. Write code to retrieve the titles for each hemisphere.
    hemisphere_titles = browser.find_by_css('h3')

    links = browser.find_by_css('a.product-item img')

    hemispheres = []

    html = browser.html
    img_soup = soup(html, 'html.parser')

    # 3b. Write code to retrieve the image urls for each hemisphere.
    for link in range(len(links)):

        hemisphere_title = browser.find_by_css('h3')[link].text

        #a) click on each hemisphere link    
        browser.find_by_css('a.product-item img')[link].click()

        #b) navigate to the full-resolution image page
        #hemisphere_url = img_soup.find("div", class_="downloads").find("li").find("a")['href']
        hemisphere_url = browser.find_by_text("Sample")['href']

        #c)retrieve the full-resolution image URL string and title for the hemisphere image,
        #hemisphere_url = f'https://marshemispheres.com/{hemisphere_url}'
 
        #Creates the dictionary
        mars_hemi = {
            'hemisphere_title' : hemisphere_title,
            'hemisphere_url' : hemisphere_url
        }

        hemispheres.append(mars_hemi)
        #hemispheres[hemisphere_titles] = hemisphere_url

        #d) use browser.back() to navigate back to the beginning to get the next hemisphere image
        browser.back()
    
    return hemispheres

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    