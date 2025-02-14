from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import os


#Initialize the driver
s=Service(r'...\chromedriver.exe') #Replace with the path to your driver

options = webdriver.ChromeOptions()
options.add_argument("--headless")  #(optional, but recommended)
driver = webdriver.Chrome(service=s, options=options)

#Pick category
url_list = ["https://www.citygross.se/matvaror/kott-och-fagel",
            #"https://www.citygross.se/matvaror/frukt-och-gront",
            #"https://www.citygross.se/matvaror/mejeri-ost-och-agg",
            #"https://www.citygross.se/matvaror/skafferiet",
            #"https://www.citygross.se/matvaror/fryst",
            #"https://www.citygross.se/matvaror/brod-och-bageri",
            #"https://www.citygross.se/matvaror/hem-och-stad",
            #"https://www.citygross.se/matvaror/godis",
            #"https://www.citygross.se/matvaror/dryck",
            #"https://www.citygross.se/matvaror/snacks",
            #"https://www.citygross.se/matvaror/skonhet-och-hygien",
            #"https://www.citygross.se/matvaror/chark",
            #"https://www.citygross.se/matvaror/manuell-delikatess",
            #"http://www.citygross.se/matvaror/fisk-och-skaldjur",
            #"https://www.citygross.se/matvaror/kyld-fardigmat",
            #"https://www.citygross.se/matvaror/vegetariskt",
            #"https://www.citygross.se/matvaror/barn",
            #"https://www.citygross.se/matvaror/blommor",
            #"https://www.citygross.se/matvaror/husdjur",
            #"https://www.citygross.se/matvaror/apotek-och-receptfria-lakemedel",
            #"https://www.citygross.se/matvaror/halsa",
            #"https://www.citygross.se/matvaror/tobak",
            #"https://www.citygross.se/matvaror/storpack"
            ]

products = []  #List to store product information

for base_url in url_list:
    
    #driver.get(base_url)
    page_number = 1
    
    while True: 
        
        #For accessing other pages
        url = base_url if page_number == 1 else f"{base_url}?page={page_number}"
        driver.get(url)
        
        try:
           
            time.sleep(5)
            
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            #Find all products
            product_ids = soup.find_all("div", class_="l-column-30_xs-30_sm-20_md-15_lg-12_xlg-10-mobileGutter")
            
            #Check if product_ids is empty - on extra page
            if not product_ids:  
                print(f"No products found on page {page_number}. Exiting.")
                break
            
            #Get name, price, detail
            for product in product_ids:
                name = product.find("h2", class_="details__name")  
                price_element = product.find("span", class_="compare-price")
                if price_element:
                    full_price_text = price_element.text.strip()
                
                    price = re.sub(r"Jfr pris\s*", "", full_price_text).strip()

                else:
                    price = "N/A"
                    
                det = product.find("h3")
                product_id = product.get("data-productid")
                
                products.append({"name": name.text, "price": price, "detail (manuf, quantity)": det.text, "id": product_id})
            
            #Next page
            page_number += 1
            
        except (TimeoutException, ConnectionError, TimeoutError) as e:
            print(f"Network error or timeout: {e}")
            break  
        
        except Exception as e:
            print(f"An error occurred: {e}")
            break
        
        
    driver.quit() 
    
df = pd.DataFrame(products)
script_dir = r'your path//WebScraper' #Replace with path to saving folder
csv_file_path = os.path.join(script_dir, "output.csv")
df.to_csv(csv_file_path, index=False, encoding="utf-8")
