# Load the dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup as bs
from time import sleep
import requests

# Url to scrap
url_toscrap = "https://turo.com/ca/en-us/car-rental/montreal-qc/ford/mustang/702436?searchId=OD83L624"

# Define the driver
driver = webdriver.Firefox()

# Access the url of the page to scrap
driver.get(url_toscrap)

# Collect all the informations on the page
source_data = driver.page_source
soup = bs(source_data,features="html.parser")

# collect the number of pictures
extract_nbrpictures = soup.find("div",{"class":"fullScreenCarousel-count"})
if extract_nbrpictures != None:
    zoom_picturecarousel = extract_nbrpictures.text
    count_pictures = int(zoom_picturecarousel.split("of")[1].replace(" ",""))
    print(f"There is {count_pictures} pictures on this offer")
    # For each picture
    for i in range(count_pictures):
        # Scroll on the carousel
        python_button = driver.find_elements_by_xpath("//i[@class='fullScreenCarousel-navigation--next']")[0]
        python_button.click()
        
        # Collect the data on the page
        source_data = driver.page_source
        soup = bs(source_data,features="html.parser")
        
        # Extract the inofrmatrions related to the picture
        details_picture = soup.find('img',{'class':'heroImage-image'},src = True)
        link_picture = details_picture["src"]
        
        # Download the image (with a get request)
        response = get(link_picture)
        if response.ok:
            img_data = response.content
            # Save the picture in a file (picturei.jpg)
            with open(f"picture{i}.jpg", 'wb') as file:
                file.write(img_data)

sleep(2)

# Stop the driver
driver.close()