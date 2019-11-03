# Load the dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup as bs
from time import sleep

# Define the main url (where to log the location)
url_main_page = "https://turo.com/en-us?locale=en_US"

# Define the city where to search the offers
location = "Montreal, Quebec"

# Define the driver for the execution
driver = webdriver.Firefox()

# Connect to the main page
driver.get(url_main_page)

# Input the location
inputElement = driver.find_element_by_id("js-searchFormExpandedLocationInput")
inputElement.send_keys(location)

# Submit the research
python_button = driver.find_elements_by_xpath("//button[@class='button button--green searchFormExpanded-button searchFormExpanded-button--round u-hideTinyScreen']")[0]
python_button.click()

# Let the page loading
sleep(10)

# Scroll all along the page of the search
# Based on https://michaeljsanders.com/2017/05/12/scrapin-and-scrollin.html

# Collect the current lenght of the page
previous_lengthpage = driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
print(original_lengthpage)
# Define a low bound for the scrolling window
lowbound = 0

# Infinite loop
while True:

    # Define the high bound of the scrolling window
    highbound = lowbound + 400
    
    # Scroll between the low and the high bounds
    driver.execute_script(f"window.scrollTo({lowbound}, {highbound});")
    
    # Collect all the data on the current page area
    source_data = driver.page_source
    soup = bs(source_data,features="html.parser")

    # Collect all the ads on the page
    ads = soup.findAll('span',{'class':'vehicleCard-makeModel'})

    print("Ads collected : ", len(ads))
    
    if len(ads) > 0:
        lowbound = highbound
    
    # Collect the length of the page after the scrolling
    lengthpage = driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    
    # If the past and current lenght page are similar stop the scraping
    if previous_lengthpage == lengthpage:
        break
    else:
        previous_lengthpage = lengthpage
        
    sleep(1)
    
# Stop the driver
driver.close()