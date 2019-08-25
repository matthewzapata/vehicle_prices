import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import re

def prep_the_soup(domain, new_or_used, year, make, model):
    url = f'https://www.{domain}/searchused.aspx?Type={new_or_used}&Year={year}&Make={make}&Model={model}&pn=10'
    response = get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def get_years_and_models_lists(soup, make):
    vehicle_titles = soup.find_all('div', class_='row vehicleTitleContainer visible-xs')

    vehicle_titles_list = []
    for vehicle_title in vehicle_titles:
        vehicle_titles_list.append(vehicle_title.text.strip())

    year_list = []
    model_list = []

    for title_element in vehicle_titles_list:
        year_and_title = re.findall(f'(\d+) {make} (.*)', title_element)
        year_list.append(year_and_title[0][0])
        model_list.append(year_and_title[0][1])

    return year_list, model_list

def get_price_list(soup):
    prices = soup.find_all('span', class_='pull-right primaryPrice')

    price_list = []
    for price in prices:
        price_list.append(price.text)
        
    j = 1
    for i, price in enumerate(price_list):
        if price_list[i] == price_list[j]:
            del price_list[i]
        j += 1
    
    return price_list

def get_body_style_list(soup):
    body_styles = soup.find_all('li', class_='bodyStyleDisplay')

    body_style_list = []
    for style in body_styles:
        body_style_list.append(re.findall(r'Body Style: (.+)', style.text)[0])
        
    j = 1
    for i, style in enumerate(body_style_list):
        if body_style_list[i] == body_style_list[j]:
            del body_style_list[i]
        j += 1

    return body_style_list

def get_engine_list(soup):
    engines = soup.find_all('li', class_='engineDisplay')

    engine_list = []
    for style in engines:
        engine_list.append(re.findall(r'Engine: (.+)', style.text)[0])
        
    j = 1
    for i, style in enumerate(engine_list):
        if engine_list[i] == engine_list[j]:
            del engine_list[i]
        j += 1

    return engine_list

def get_transmission_list(soup):
    transmissions = soup.find_all('li', class_='transmissionDisplay')

    transmission_list = []
    for style in transmissions:
        transmission_list.append(re.findall(r'Transmission: (.+)', style.text)[0])
        
    j = 1
    for i, style in enumerate(transmission_list):
        if transmission_list[i] == transmission_list[j]:
            del transmission_list[i]
        j += 1

    return transmission_list

def get_drivetrain_list(soup):
    driveTrains = soup.find_all('li', class_='driveTrainDisplay')

    driveTrain_list = []
    for style in driveTrains:
        driveTrain_list.append(re.findall(r'Drive Type: (.+)', style.text)[0])
        
    j = 1
    for i, style in enumerate(driveTrain_list):
        if driveTrain_list[i] == driveTrain_list[j]:
            del driveTrain_list[i]
        j += 1
    
    return driveTrain_list

def get_exterior_color_list(soup):
    extColors = soup.find_all('li', class_='extColor')

    extColor_list = []
    for style in extColors:
        extColor_list.append(re.findall(r'Ext. Color: (.+)', style.text)[0])
        
    j = 1
    for i, style in enumerate(extColor_list):
        if extColor_list[i] == extColor_list[j]:
            del extColor_list[i]
        j += 1
            
    return extColor_list

def get_mileage_list(soup):
    mileages = soup.find_all('li', class_='mileageDisplay')

    mileage_list = []
    for style in mileages:
        mileage_list.append(re.findall(r'Mileage: (.+)', style.text)[0])
        
    j = 1
    for i, style in enumerate(mileage_list):
        if mileage_list[i] == mileage_list[j]:
            del mileage_list[i]
        j += 1
    return mileage_list

def create_dataframe(domain, new_or_used, year_list, make, model_list, price_list, body_style_list, mileage_list, engine_list, transmission_list, driveTrain_list, extColor_list):
    if domain == 'mccombsfordwest.com':
        dealer = 'McCombs Ford West'
    elif domain == 'nsford.com':
        dealer = 'Northside Ford'
    elif domain == 'southwayford.com':
        dealer = 'Southway Ford'
    elif domain == 'jordanford.net':
        dealer == 'Jordan Ford'

    if new_or_used == 'U':
        condition = 'Used'
    else:
        condition = 'New'

    df = pd.DataFrame({'year':year_list, 'make':make, 'model':model_list, 
              'condition':condition, 'price':price_list, 
              'body_style':body_style_list, 'mileage':mileage_list, 'engine':engine_list, 
              'transmission':transmission_list, 'drivetrain':driveTrain_list,
              'ext_color':extColor_list, 'dealer':dealer})

    return df

def get_dealership_data(domain, new_or_used, year, make, model):
    soup = prep_the_soup(domain, new_or_used, year, make, model)
    year_list, model_list = get_years_and_models_lists(soup, make)
    price_list = get_price_list(soup)
    body_style_list = get_body_style_list(soup)
    engine_list = get_engine_list(soup)
    transmission_list = get_transmission_list(soup)
    drivetrain_list = get_drivetrain_list(soup)
    exterior_color_list = get_exterior_color_list(soup)
    mileage_list = get_mileage_list(soup)
    
    df = create_dataframe(domain, new_or_used, year_list, 
    make, model_list, price_list, body_style_list, 
    mileage_list, engine_list, transmission_list, 
    drivetrain_list, exterior_color_list)

    return df