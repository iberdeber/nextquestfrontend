from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
from bs4 import BeautifulSoup

def aptscraper(city): #city-stateinitial (chicago-il)

    apts = []
    path = 'lib\chromedriver-win64\chromedriver-win64\chromedriver.exe'
    service = Service(executable_path=path)

    chrome_options = Options()
    chrome_options.headless = False
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--disable-web-security')

    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(f"https://www.apartments.com/{city}")
    html = driver.page_source

    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    names = soup.find_all('div', class_='property-title')
    addys = soup.find_all('div', class_='property-address js-url')
    pricings = soup.find_all('p', class_='property-pricing')
    links = soup.find_all('a', class_="property-link js-url")

    # Ensure we iterate over all lists simultaneously
    for name, addy, pricing, link in zip(names, addys, pricings, links):
        apt_name = name.get("title")
        single_addy = addy.get_text(strip=True)
        price_text = pricing.get_text(strip=True)
        link_indiv = link.get("href")

        # Create a dictionary for each apartment
        apartment_data = {
            'name': apt_name,
            'address': single_addy,
            'price_range': price_text,
            'link': link_indiv
        }
        # Append the dictionary to the apts list
        apts.append(apartment_data)
    # Convert the list of dictionaries to JSON format and save to file
    with open(f"{city}-apartments.json", "w") as json_file:
        json.dump(apts, json_file, indent=4)
    return apts

aptscraper("richmond-va")
