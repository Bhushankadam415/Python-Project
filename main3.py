from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import csv
from csv import writer

chrome_options = Options()
chrome_options.add_argument("--headless")
page_main = webdriver.Chrome(chrome_options=chrome_options)
page_details = webdriver.Chrome(chrome_options=chrome_options)
movie_count = 0
headerList = ['Detail_url', 'Name', 'Rating', 'Genre','Date','Runtime','Director']
with open("moviedata2.csv", 'w') as file:
    dw = csv.DictWriter(file, delimiter=',', fieldnames=headerList)
    dw.writeheader()

for i in range(1,44):
  url = 'https://www.themoviedb.org/movie?page='+str(i)
  print(url)
  page_main.get(url)
  for data in WebDriverWait(page_main, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.card.style_1'))):
      try:
          record_list = []
          detail_url = data.find_element(By.CSS_SELECTOR, 'div.image div.wrapper a').get_attribute('href')
          # print(detail_url)
          record_list.append(detail_url)
          page_details.get(detail_url)   
          Name = page_details.find_element(By.CSS_SELECTOR, 'div.title.ott_true > h2 > a').text
          # print(Name)
          record_list.append(Name)
          Rating = page_details.find_element(By.CSS_SELECTOR, 'div.user_score_chart').get_attribute('data-percent')
          # print(Rating)
          record_list.append(Rating)
          Genre = page_details.find_element(By.CSS_SELECTOR, 'span.genres').text
          # print(Genre)
          record_list.append(Genre)
          Date = WebDriverWait(page_details, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.release'))).text
          # print(Date)
          record_list.append(Date)
          Runtime = page_details.find_element(By.CSS_SELECTOR, 'span.runtime').text
          # print(Runtime)
          record_list.append(Runtime)
          Director = page_details.find_element(By.CSS_SELECTOR, 'ol > li:nth-child(2) > p:nth-child(1) > a').text
          # print(Director)
          record_list.append(Director)
          # print('----------------------------------')
          movie_count += 1
          with open('moviedata2.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(record_list)
      except:
          pass
  print("Finished processing. Scraped {} movies".format(movie_count))