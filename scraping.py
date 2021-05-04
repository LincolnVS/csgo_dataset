from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep

import argparse
import numpy as np 
import pandas as pd

## Parse settings
parser = argparse.ArgumentParser(description='CSGO Web Scraping Options')
parser.add_argument('--p','--pages', default=0, type=int, help='number of pages to scrap (0 == automatic)')
parser.add_argument('--s','--save-type', default='csv', type=str, choices=['csv', 'json'], help='save type (csv or json)')
parser.add_argument('--d','--depth', default='simple', type=str, choices=['simple', 'deep'], help='scraping depth')
parser.add_argument('--o','--output', default='./csgo_dataset', type=str, help='define output file name')

parser.add_argument('--nopd','--no-process-data', default=False, action="store_true", help="don't processes the data")
parser.add_argument("--nopb",'--no-progress-bar', default=False, action="store_true", help="don't show progress bar")

args = parser.parse_args()

## Selective imports 
if args.save_type == 'json':
    import json
if ~args.no_progress_bar:
    from tqdm import tqdm

## Selenium
op = webdriver.ChromeOptions()
op.add_argument('headless')
browser = webdriver.Chrome(ChromeDriverManager().install(),options=op)

## page constant
PAGE_PREFIX = 'https://www.hltv.org/results?offset=' # 0; 100; 200; 300; 400...
FIRST_PAGE = PAGE_PREFIX+"0"

def read_page_result(page):
    browser.get(page)
    sleep(2)
    elements = browser.find_elements_by_xpath("//*[@class='standard-headline' or @class='a-reset']")
    page_results = pd.DataFrame()
    match_date = '-'
    for element in elements:
        text = element.text 
        if 'Results for ' in text[:12]:
            match_date = text[12:]
            continue
        elif text == '' or match_date == '-':
            continue

        dict_matchs = {'date':match_date,
                        'match': text.replace('\n',';'),
                        'link': element.get_attribute('href')}
        page_results = page_results.append(dict_matchs,ignore_index=True)

    return page_results

def read_results(pages_link):
    results = pd.DataFrame()
    if args.no_progress_bar:
        for page_link in pages_link:
            results = results.append(read_page_result(page_link))
    else:
        for page_link in tqdm(pages_link):
            results = results.append(read_page_result(page_link))
    return results

def get_pages_link():
    if args.pages <= 0 :
        browser.get(FIRST_PAGE)
        sleep(2)
        num_pages_aux = browser.find_element_by_class_name('pagination-data').text[11:]
        n_pages = round(int(num_pages_aux)/100)
    else:
        n_pages = args.pages

    list_pages = []
    [list_pages.append(PAGE_PREFIX + str(100*n)) for n in range(0,n_pages)]
    
    return list_pages

def write_file(df):
    if args.save_type == 'csv':
        df.to_csv(f'{args.output}.csv', sep=';', date_format='%Y%m%d')
    elif args.save_type == 'json':
        with open(f'{args.output}.json', 'w') as json_file:
            json.dump(df.to_dict(orient="records"),json_file, indent=4)

def process_results(data):
    if args.depth == 'simple':
        ## Tratamento
        #Define Match_ID
        data['match_id'] = data['link'].str.replace('https://www.hltv.org/matches/','',regex=False).str.replace('(/)[a-z0-9]+.*','', regex=True)

        #Split Coluna 'jogo'
        #data['date'] = data['date']
        match_split = data['match'].str.split(';') 
        data['time_1'] = match_split.str[0]
        result = match_split.str[1]
        data['time_2'] = match_split.str[2]
        
        result_split = result.str.split(' ')
        data['score_t1'] = pd.to_numeric(result_split.str[0])
        data['score_t2'] = pd.to_numeric(result_split.str[2])

        data['event'] = match_split.str[3]
        data['best_of'] = match_split.str[4]

        #Drop Columns and Drop NaN
        data.drop(columns=['match'], inplace=True)
        data = data.dropna()
        data = data.reset_index(drop=True)

        #Rename columns and reorder
        data.columns = ['date', 'match_url','match_id', 'team_A', 'team_B', 'score_tA', 'score_tB', 'event', 'type_of_match']
        columns_order = ['date','match_id', 'team_A', 'team_B', 'score_tA', 'score_tB', 'event', 'type_of_match', 'match_url']
        data = data[columns_order]

        # Convert map name in bo1 type
        data['type_of_match'] = np.where(
            (data["type_of_match"] != "bo5")
            & (data["type_of_match"] != "bo3") 
            & (data["type_of_match"] != "-"),#condition
            "bo1",#value insert
            data["type_of_match"]#Column effected
        )
        # Convert score TA and TB in bo1 score (1 x 0 or 0 x 1)
        score_tA_bo1 = np.where(
            data["score_tA"] > data["score_tB"],#condition
            1,#value insert
            0#Column effected
        )
        score_tB_bo1 = np.where(
            data["score_tA"] < data["score_tB"],#condition
            1,#value insert
            0#Column effected
        )
        data["score_tA"] = np.where(
            (data["type_of_match"] == "bo1") | (data["type_of_match"] == "-"),#condition
            score_tA_bo1,#value insert
            data["score_tA"]#Column effected
        )
        data["score_tB"] = np.where(
            (data["type_of_match"] == "bo1") | (data["type_of_match"] == "-"),#condition
            score_tB_bo1,#value insert
            data["score_tB"]#Column effected
        )
    else:
        raise Exception('Not Implemented Deep Scraping yet')
        data = []
    return data

if __name__ == '__main__':
    print('\n\n====== Starting CSGO Scraping Script ======')
    print('Get Num of Pages')
    pages_link = get_pages_link()
    print('Geting Matchs')
    results = read_results(pages_link)
    if ~args.no_process_data:
        print('Process Data')
        results = process_results(results)
    print(f'Saving {args.save_type}')
    write_file(results)
