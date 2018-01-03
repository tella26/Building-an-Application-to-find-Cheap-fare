import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from bs4 import BeautifulSoup

# An algorithm use in the project Dbscan
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

print("Insert Url where you want to extract data:")
url= input()  # Insert Url where you want to extract data. 
driver = webdriver.PhantomJS() # Ensure you have phantomJS installed and put in the environment Path
dcap = dict(DesiredCapabilities.PHANTOMJS)
print("Check your user agent on google by typing 'my user agent' then copy and paste")
user_agent = input()
dcap["phantomjs.page.settings.userAgent"] = (user_agent) #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36 OPR/49.0.2725.64
driver.implicitly_wait(10)
driver.get(url)

    

s= BeautifulSoup(driver.page_source, "lxml")
print("check the DOM from the website and put the tag class such as LJV2HGB-d-Ab")
dataprice = input()
best_price_tags=s.findAll('div', dataprice) # check the DOM from the website and put the tag class such as LJV2HGB-d-Ab
    

print('Scrapping successfully done')
driver.save_screenshot(r'Web_picture2.png')
print('Please check your photo viewer for web_picture2.png to confirm the web page')
best_prices= []
for tag in best_price_tags:
    best_prices.append(tag.text.replace('$','').replace(',','').replace('USD','').replace('#',''))
price = pd.DataFrame(best_prices, columns=['price'])
price
# Plot of the data
#X = len(price)
#fig, ax = plt.subplots(figsize=(10,6))
#plt.scatter(np.linspace(-1, 1, X), best_prices) # X is the length of the data

fares = pd.DataFrame(best_prices, columns=['prices'])
px = (x for x in fares['prices'])
ff = pd.DataFrame(px, columns = ['fares']).reset_index()

X = StandardScaler().fit_transform(ff)
db = DBSCAN (eps = 0.5 , min_samples = 1).fit(X)

labels = db.labels_
clusters = len(set(labels))
pf = pd.concat([ff, pd.DataFrame(db.labels_, columns=['clusters'])], axis =1)
rf = pf.groupby('clusters')['prices'].agg(['min', 'count']).sort_values('min', ascending= True)
rf
