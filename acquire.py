import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import re
import math

url_beginning = 'https://www.'

def make_the_soup(domain, new_or_used, year, make, model):
    url = f'{url_beginning}{domain}/search{new_or_used}.aspx?Year={year}&Make={make}&Model={model}&pn=100'
    print(url)
    response = get(url)
    if response.status_code != 200:
        print('Webpage did not load successfully. Skipping.')
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup, response.status_code

def determine_number_of_pages(soup):
    max_number_of_pages = math.ceil(int(re.findall(r'(\d+) Vehicles', soup.find('p', class_='srpVehicleCount').text.strip())[0])/100)
    return max_number_of_pages


def get_years_and_models_lists(soup, make, i):
    vehicle_titles = soup.find_all('div', class_='row vehicleTitleContainer visible-xs')

    global vehicle_titles_list
    vehicle_titles_list = []
    for vehicle_title in vehicle_titles:
        vehicle_titles_list.append(vehicle_title.text.strip())

    if i == 1:
        global year_list
        year_list = []
        global model_list
        model_list = []
    
    for title_element in vehicle_titles_list:
        year_and_title = re.findall(f'(\d+) {make} (.*)', title_element)
        year_list.append(year_and_title[0][0])
        model_list.append(year_and_title[0][1])

    return year_list, model_list

def get_price_list(soup, i):
    prices = soup.find_all('div', class_="col-sm-6 col-sm-push-6 hidden-xs")

    if i == 1:    
        global price_list
        price_list = []

    for price in prices:
        if price.find('span', class_='pull-right primaryPrice') == None:
            price_block = price.find('li', class_='priceBlockItem priceBlockItemPrice')
            price_list.append(price_block.find('span', class_='pull-right').text)
        else:
            price_list.append(price.find('span', class_='pull-right primaryPrice').text)
        
    return price_list

def get_body_style_list(soup, i):
    body_styles = soup.find_all('ul', class_='list-unstyled srpVehicleDetails')

    if i == 1:
        global body_style_list
        body_style_list = []
   
    for body_style in body_styles:
        body_style_list.append(re.findall(r'Body Style: (.+)', body_style.find('li', class_='bodyStyleDisplay').text)[0])

    return body_style_list

def get_engine_list(soup, i):
    engines = soup.find_all('ul', class_='list-unstyled srpVehicleDetails')

    if i == 1:
        global engine_list
        engine_list = []
    
    for engine in engines:
        engine_list.append(re.findall(r'Engine: (.+)', engine.find('li', class_='engineDisplay').text)[0])

    return engine_list

def get_transmission_list(soup, i):
    transmissions = soup.find_all('ul', class_='list-unstyled srpVehicleDetails')

    if i == 1:
        global transmission_list
        transmission_list = []
   
    for transmission in transmissions:
        transmission_list.append(re.findall(r'Transmission: (.+)', transmission.find('li', class_='transmissionDisplay').text)[0])

    return transmission_list

def get_drivetrain_list(soup, i):
    drivetrains = soup.find_all('ul', class_='list-unstyled srpVehicleDetails')

    if i == 1:
        global driveTrain_list
        driveTrain_list = []
   
    for drivetrain in drivetrains:
        driveTrain_list.append(re.findall(r'Drive Type: (.+)', drivetrain.find('li', class_='driveTrainDisplay').text)[0])
    
    return driveTrain_list

def get_exterior_color_list(soup, i):
    exterior_colors = soup.find_all('ul', class_='list-unstyled srpVehicleDetails')

    if i == 1:
        global extColor_list
        extColor_list = []
   
    for exterior_color in exterior_colors:
        extColor_list.append(re.findall(r'Ext. Color: (.+)', exterior_color.find('li', class_='extColor').text)[0])
            
    return extColor_list

def get_mileage_and_condition_lists(soup, i):
    mileages = soup.find_all('ul', class_='list-unstyled srpVehicleDetails')

    if i == 1:
        global mileage_list
        mileage_list = []
        global condition_list
        condition_list = []
   
    for mileage in mileages:
        if mileage.find('li', class_='mileageDisplay') == None:
            mileage_list.append(int(0))
            condition_list.append('new')
        else:
            mileage_list.append(re.findall(r'Mileage: (.+)', mileage.find('li', class_='mileageDisplay').text)[0])
            condition_list.append('used')

    return mileage_list, condition_list

def grab_next_page_url(soup):
    new_url_ending = soup.find('ul', class_='pagination margin-x').find_all('a')[1]['href']
    return new_url_ending

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
    soup, website_response = make_the_soup(domain, new_or_used, year, make, model)
    if website_response == 200:
        max_number_of_pages = determine_number_of_pages(soup)
        if max_number_of_pages != 0:
            for i in range (1, max_number_of_pages+1):
                if i != 1:
                    new_url = f'{url_beginning}{domain}{new_url_ending}'
                    print(new_url)
                    response = get(new_url)
                    if response.status_code != 200:
                        print('Webpage did not load successfully.')
                    soup = BeautifulSoup(response.content, 'html.parser')    
                    
                year_list, model_list = get_years_and_models_lists(soup, make, i)
                price_list = get_price_list(soup, i)
                body_style_list = get_body_style_list(soup, i)
                engine_list = get_engine_list(soup, i)
                transmission_list = get_transmission_list(soup, i)
                drivetrain_list = get_drivetrain_list(soup, i)
                exterior_color_list = get_exterior_color_list(soup, i)
                mileage_list, condition_list = get_mileage_and_condition_lists(soup, i)
                if i != max_number_of_pages:
                    new_url_ending = grab_next_page_url(soup)

            df = create_dataframe(domain, new_or_used, year_list, 
            make, model_list, condition_list, price_list, body_style_list, 
            mileage_list, engine_list, transmission_list, 
            drivetrain_list, exterior_color_list)

            return df