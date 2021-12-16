import requests, bs4
from utils import debug_data

SCRAPER_COUNTRY_NAME = 1
SCRAPER_TOTAL_CASES  = 2
SCRAPER_NEW_CASES    = 3
SCRAPER_TOTAL_DEATHS = 4
SCRAPER_NEW_DEATHS   = 5
SCRAPER_POPULATION   = 14

CASE  = 10
TOTAL = 20

PAGE_URL = 'https://www.worldometers.info/coronavirus/'

class Row:
    def __init__(self, id, country_name, total_cases, total_deaths, new_cases, new_deaths, population):
        self.id = id
        self.country_name = country_name
        self.total_cases  = total_cases
        self.total_deaths = total_deaths
        self.population   = population
        self.new_cases    = new_cases
        self.new_deaths   = new_deaths
        self.population   = population

def init_scraper(target):
    debug_data('requesting page...')

    page = requests.get(PAGE_URL)
    page_soup = bs4.BeautifulSoup(page.text, 'html.parser')
  
    return scrape_table_data(page_soup, target)

def get_cell_data(cell_data, str_format):
    result = '0'
    if len(cell_data) == '':
        result = '0'
    else:
        result = cell_data

    if str_format == CASE and result != '0':
        result = result[1:]

    return result 

def scrape_table_data(page_soup, target):
    debug_data('scraping table...')

    country_id = 0
    raw_scraped_data = []
    for table_row in page_soup.select(target):
        cell_it = 0

        country_name  = ''
        total_cases   = ''
        new_cases     = ''
        total_deaths  = ''
        new_deaths    = ''
        population    = ''

        for table_cell in table_row.findAll('td'):
            if cell_it == SCRAPER_COUNTRY_NAME:
                aux = table_cell.find('a')
                if aux == None:
                    country_name = ""
                    break
                else: 
                    country_name = aux.get_text()
                    country_id += 1 

            if cell_it == SCRAPER_TOTAL_CASES:
                total_cases = get_cell_data(table_cell.get_text(), TOTAL)
                if total_cases == '' or total_cases == ' ':
                    total_cases = '0'
            if cell_it == SCRAPER_TOTAL_DEATHS:
                total_deaths = get_cell_data(table_cell.get_text(), TOTAL)
                if total_deaths == '' or total_deaths == ' ':
                    total_deaths = '0'
            if cell_it == SCRAPER_NEW_CASES:
                new_cases = get_cell_data(table_cell.get_text(), CASE)
                if new_cases == '' or new_cases == ' ':
                    new_cases = '0'
            if cell_it == SCRAPER_NEW_DEATHS:
                new_deaths = get_cell_data(table_cell.get_text(), CASE)
                if new_deaths == '' or new_deaths == ' ':
                    new_deaths = '0'
            if cell_it == SCRAPER_POPULATION:
                population = get_cell_data(table_cell.get_text(), TOTAL)
            cell_it += 1
        if country_name == "" or country_id == 0:
            continue
        raw_scraped_data.append(Row(country_id, country_name, total_cases, total_deaths, new_cases, new_deaths, population))

    return raw_scraped_data

def print_row(country_id, country_name, new_cases, new_deaths, population):
    debug_data(f"{country_id} {country_name} {new_cases} {new_deaths} {population}")