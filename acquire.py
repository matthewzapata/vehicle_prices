import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import re

def prep_the_soup(domain, new_or_used, year, make, model):
    url = f'https://www.{domain}/search{new_or_used}.aspx?Year={year}&Make={make}&Model={model}&pn=100'
    print(url)
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
    prices = soup.find_all('div', class_="col-sm-6 col-sm-push-6 hidden-xs")

    price_list = []

    for price in prices:
        if price.find('span', class_='pull-right primaryPrice') == None:
            price_block = price.find('li', class_='priceBlockItem priceBlockItemPrice')
            price_list.append(price_block.find('span', class_='pull-right').text)
        else:
            price_list.append(price.find('span', class_='pull-right primaryPrice').text)
        
    return price_list

def get_body_style_list(soup):
    body_styles = soup.find_all('ul', class_='list-unstyled srpVehicleDetails')

    body_style_list = []
   
    for body_style in body_styles:
        body_style_list.append(re.findall(r'Body Style: (.+)', body_style.find('li', class_='bodyStyleDisplay').text)[0])

    return body_style_list

def get_engine_list(soup):
    engines = soup.find_all('ul', class_='list-unstyled srpVehicleDetails')

    engine_list = []
    for engine in engines:
        engine_list.append(re.findall(r'Engine: (.+)', engine.find('li', class_='engineDisplay').text)[0])

    return engine_list

def get_transmission_list(soup):
    transmissions = soup.find_all('ul', class_='list-unstyled srpVehicleDetails')

    transmission_list = []
   
    for transmission in transmissions:
        transmission_list.append(re.findall(r'Transmission: (.+)', transmission.find('li', class_='transmissionDisplay').text)[0])

    return transmission_list

def get_drivetrain_list(soup):
    drivetrains = soup.find_all('ul', class_='list-unstyled srpVehicleDetails')

    driveTrain_list = []
   
    for drivetrain in drivetrains:
        driveTrain_list.append(re.findall(r'Drive Type: (.+)', drivetrain.find('li', class_='driveTrainDisplay').text)[0])
    
    return driveTrain_list

def get_exterior_color_list(soup):
    exterior_colors = soup.find_all('ul', class_='list-unstyled srpVehicleDetails')

    extColor_list = []
   
    for exterior_color in exterior_colors:
        extColor_list.append(re.findall(r'Ext. Color: (.+)', exterior_color.find('li', class_='extColor').text)[0])
            
    return extColor_list

def get_mileage_and_condition_lists(soup):
    mileages = soup.find_all('ul', class_='list-unstyled srpVehicleDetails')

    mileage_list = []
    condition_list = []
   
    for mileage in mileages:
        if mileage.find('li', class_='mileageDisplay') == None:
            mileage_list.append(int(0))
            condition_list.append('new')
        else:
            mileage_list.append(re.findall(r'Mileage: (.+)', mileage.find('li', class_='mileageDisplay').text)[0])
            condition_list.append('used')

    return mileage_list, condition_list

def create_dataframe(domain, new_or_used, year_list, make, model_list, condition_list, 
price_list, body_style_list, mileage_list, engine_list, transmission_list, driveTrain_list, extColor_list):
    if domain == 'mccombsfordwest.com':
        dealer = 'McCombs Ford West'
    elif domain == 'nsford.com':
        dealer = 'Northside Ford'
    elif domain == 'southwayford.com':
        dealer = 'Southway Ford'
    elif domain == 'jordanford.net':
        dealer = 'Jordan Ford'
    elif domain == 'ancirakiasa.com':
        dealer = 'Ancira Kia'
    elif domain == 'worldcarkianorth.com':
        dealer = 'World Car Kia North'
    elif domain == 'ancirachev.com':
        dealer = 'Ancira Chevrolet'
    elif domain == 'freedomchevy.com':
        dealer = 'Freedom Chevrolet'
    elif domain == 'mynschevy.com':
        dealer = 'Northside Chevrolet'
    elif domain == 'anciracjd.com':
        dealer = 'Ancira Chrysler Jeep Dodge'
    elif domain == 'northstardodge.net':
        dealer = 'Northstar Dodge'
    elif domain == 'sanantoniododgechryslerjeepram.com':
        dealer = 'San Antonio DCJR'
    elif domain == 'ingramparkcj.net':
        dealer = 'Ingram Park DCJR'
    elif domain == 'lonestarchryslerdodgejeepsanantonio.com':
        dealer = 'Lonestar DCJR'
    elif domain == 'northparktoyota.com':
        dealer = 'Northpark Toyota'
    elif domain == 'cavendertoyota.com':
        dealer = 'Cavender Toyota'
    elif domain == 'redmccombstoyota.com':
        dealer = 'Red McCombs Toyota'
    elif domain == 'universaltoyota.com':
        dealer = 'Universal Toyota'
    

    print(len(year_list))
    print(len(make))
    print(len(model_list))
    print(len(condition_list))
    print(len(price_list))
    print(len(body_style_list))
    print(len(mileage_list))
    print(len(engine_list))
    print(len(transmission_list))
    print(len(driveTrain_list))
    print(len(extColor_list))
    print(len(dealer))

    df = pd.DataFrame({'year':year_list, 'make':make, 'model':model_list, 
              'condition':condition_list, 'price':price_list, 
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
    mileage_list, condition_list = get_mileage_and_condition_lists(soup)
    
    df = create_dataframe(domain, new_or_used, year_list, 
    make, model_list, condition_list, price_list, body_style_list, 
    mileage_list, engine_list, transmission_list, 
    drivetrain_list, exterior_color_list)

    return df