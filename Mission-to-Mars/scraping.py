{
  "metadata": {
    "language_info": {
      "codemirror_mode": {
        "name": "python",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.8"
    },
    "kernelspec": {
      "name": "python",
      "display_name": "Python (Pyodide)",
      "language": "python"
    }
  },
  "nbformat_minor": 4,
  "nbformat": 4,
  "cells": [
    {
      "cell_type": "code",
      "source": "# Import Splinter, BeautifulSoup, and Pandas\nfrom splinter import Browser\nfrom bs4 import BeautifulSoup as soup\nimport pandas as pd\nimport datetime as dt\nfrom webdriver_manager.chrome import ChromeDriverManager\n\n\n# In[2]:\n\n\ndef scrape_all():\n    # Initiate headless driver for deployment\n    executable_path = {'executable_path': ChromeDriverManager().install()}\n    browser = Browser('chrome', **executable_path, headless=True)\n\n    news_title, news_paragraph = mars_news(browser)\n\n    # Run all scraping functions and store results in a dictionary\n    data = {\n        \"news_title\": news_title,\n        \"news_paragraph\": news_paragraph,\n        \"featured_image\": featured_image(browser),\n        \"facts\": mars_facts(),\n        \"last_modified\": dt.datetime.now(),\n        \"hemispheres\": mars_hemispheres(browser)             \n    }\n    \n# Stop webdriver and return data\n    browser.quit()\n    return data\n\n\n# In[3]:\n\n\ndef mars_news(browser):\n\n    # Scrape Mars News\n    # Visit the mars nasa news site\n    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'\n    browser.visit(url)\n\n    # Optional delay for loading the page\n    browser.is_element_present_by_css('div.list_text', wait_time=1)\n\n    # Convert the browser html to a soup object and then quit the browser\n    html = browser.html\n    news_soup = soup(html, 'html.parser')\n\n    # Add try/except for error handling\n    try:\n        slide_elem = news_soup.select_one('div.list_text')\n        # Use the parent element to find the first 'a' tag and save it as 'news_title'\n        news_title = slide_elem.find('div', class_='content_title').get_text()\n        # Use the parent element to find the paragraph text\n        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()\n\n    except AttributeError:\n        return None, None\n\n    return news_title, news_p\n\n\n# In[4]:\n\n\ndef featured_image(browser):\n    # Visit URL\n    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'\n    browser.visit(url)\n\n    # Find and click the full image button\n    full_image_elem = browser.find_by_tag('button')[1]\n    full_image_elem.click()\n\n    # Parse the resulting html with soup\n    html = browser.html\n    img_soup = soup(html, 'html.parser')\n\n    # Add try/except for error handling\n    try:\n        # Find the relative image url\n        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')\n\n    except AttributeError:\n        return None\n\n    # Use the base url to create an absolute url\n    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'\n\n    return img_url\n\n\n# In[5]:\n\n\ndef mars_facts():\n    # Add try/except for error handling\n    try:\n        # Use 'read_html' to scrape the facts table into a dataframe\n        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]\n\n    except BaseException:\n        return None\n\n    # Assign columns and set index of dataframe\n    df.columns=['Description', 'Mars', 'Earth']\n    df.set_index('Description', inplace=True)\n\n    # Convert dataframe into HTML format, add bootstrap\n    return df.to_html(classes=\"table table-striped\")\n\n\n# In[6]:\n\n\n# Mars_hemispheres function\n\ndef mars_hemispheres(browser):\n    url = 'https://marshemispheres.com'\n\n    browser.visit(url)\n\n    # Parse the HTML\n    html = browser.html\n\n    hemi_soup = soup(html, 'html.parser')\n\n    hemi_items = hemi_soup.find_all('div', class_='item')\n\n    # 2. Create a list to hold the images and titles.\n    hemisphere_image_urls = []\n\n    # 3. Write code to retrieve the image urls and titles for each hemisphere.\n    for x in hemi_items:\n        # Create empty dictionary to store values\n        hemispheres = {}\n        # Find image URL\n        main_url = x.find('a', class_='itemLink')['href']\n        browser.visit(url + '/' + main_url)\n        \n        main_url = browser.html\n        image_soup = soup(main_url, 'html.parser')\n        hemi_url = url + '/' + image_soup('img', class_='wide-image')[0]['src']\n\n        # Find the titles\n        hemi_title = x.find('h3').text\n\n        # Store findings in dictionary\n        hemispheres['image_url'] = hemi_url\n        hemispheres['title'] = hemi_title\n\n        # Add to list\n        hemisphere_image_urls.append(hemispheres)\n    return hemisphere_image_urls\n    \nif __name__ == \"__main__\":\n\n    # If running as script, print scraped data\n    print(scrape_all())\n\n",
      "metadata": {},
      "execution_count": null,
      "outputs": []
    }
  ]
}