#the libraries needed starts here
import requests         #library to get json data from Google Dev API
import time             #library to sleep the program when page loading
from selenium import webdriver  #webdriver to browse google map website
from selenium.webdriver.common.action_chains import ActionChains #to perform action on webdriver
import pandas as pd #to store it in DataFrame and store it in Excel File
#libraries needed ends here
API_key="AIzaSyBpt7uzx_FpSnHF6Rwwz50WOUDZjNIjDL4" #Google Map Dev API key



place_id="ChIJMR4wOECBHjkROMf1PSEupOM"     #Place_id


#to get the JSON data from the API
#in google API only 5 review are available to get all review we need to purchase it
#but with this scrapper we can get all reviews within 1-2 minutes without paying a single penny
res=requests.get("https://maps.googleapis.com/maps/api/place/details/json?place_id="+str(place_id)+"&key="+str(API_key))
dictionary_json=res.json() #store JSON data in the dictinary
site_url=dictionary_json['result']["url"]
driver = webdriver.Chrome()#webdriver is assigned to driver variable
site=driver.get(str(site_url))
time.sleep(5)
see_review = driver.find_elements_by_class_name("allxGeDnJMl__button" and "allxGeDnJMl__button-text")[0]
click_see_review=ActionChains(driver).move_to_element(see_review).click().perform()#click on See_all_review

#scroller to scroll till the end of Google Review so to load whole data
#so that we can scrap the whole data
flag=0
while(flag==0):
    elem_prev=driver.find_elements_by_class_name("section-review-title")[-1]
    scroller = driver.find_elements_by_class_name("section-review"and "ripple-container"and "GLOBAL__gm2-body-2")[-1]
    driver.execute_script("arguments[0].scrollIntoView();", scroller)
    time.sleep(5)
    elem_next=driver.find_elements_by_class_name("section-review-title")[-1]
    if(elem_prev==elem_next):
        driver.execute_script("arguments[0].scrollIntoView();", scroller)
        time.sleep(10)
        elem_next=driver.find_elements_by_class_name("section-review-title")[-1]
        if(elem_prev==elem_next):
            flag=1

#click on MORE button to load full text of the # REVIEW:
flag=0
while(flag==0):
    for more_button in driver.find_elements_by_class_name("section-expand-review"and"blue-link"):
        try:
            ActionChains(driver).move_to_element(more_button).click().perform()
        except:
            flag=1

#store all the names who has written the # REVIEW in list_of_names
list_of_names=[]
for name in driver.find_elements_by_class_name("section-review-title"):
    list_of_names.append(name.text)

#store all the ratings in the same index as names
list_of_rating=[]
for rating in driver.find_elements_by_class_name('section-review-stars'):
    list_of_rating.append(rating.get_attribute("aria-label"))
#store all the review in the list
list_of_review=[]
for review in driver.find_elements_by_class_name("section-review-review-content"):
    list_of_review.append(review.text)
#store all the published dates
published_ago=[]
for date in driver.find_elements_by_class_name("section-review-publish-date"):
    published_ago.append(date.text)
#close the webdriver after we get whole data
driver.close()
#store all the retrived data in data frames
output_df=pd.DataFrame(zip(list_of_names,list_of_rating,published_ago,list_of_review),columns=['Name','Rating','Published On','Review'])
output_df.to_excel("output.xlsx") # save the above data frame in excel file named output.xlsx
