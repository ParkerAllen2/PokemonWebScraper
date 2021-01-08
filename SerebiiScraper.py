import os, requests, pickle, html5lib
import argparse, sys
from bs4 import BeautifulSoup

BASE_URL = 'https://www.serebii.net/pokemon/'
file_name = 'serebii_scraped_page.pickle'

def scrape_general_page(url):
    if not os.path.exists(file_name):
        result = requests.get(url)
        assert result.status_code == 200, print(f'Attempt to retrieve web page failed - result code {result.status_code}')
        with open(file_name, 'wb') as f:
            pickle.dump(result, f)
    else:
        with open(file_name, 'rb') as f:
            result = pickle.load(f)
    return result


def create_bs4_object(result):
    return BeautifulSoup(result.content, 'html5lib')

def get_general_info(ic):
    t = ic.text.split()
    #print(t)
    return t

def parse_info(soup, pokemon_infos, gen_number):
    generation = soup.find_all("select")[gen_number]
    #print(generation)
    
    with open('serebii.csv', 'w', encoding = "utf-8") as f:
        f.write(pokemon_infos)
        
    with open('serebii.csv', 'a', encoding = "utf-8") as f:
        infocards = generation.find_all("option")
        for ic in infocards[1:]:
            gen_infos_list = list(get_general_info(ic))
            ic_infos = "\n" + ",".join(gen_infos_list)
            
            f.writelines(ic_infos)


def main(args):
    result = scrape_general_page(BASE_URL)
    soup = create_bs4_object(result)
    
    pokemon_infos = ('id_nb,name,type_1,type_2,link,data_species,data_height,data_weight,'
    'data_abilities,training_catch_rate,training_base_exp,training_growth_rate,'
    'breeding_gender,stats_hp,stats_attack,stats_defense, stats_sp_atk,stats_sp_def,'
    'stats_speed,stats_total,')

    parse_info(soup, pokemon_infos, int(args.g) - 1)


parser = argparse.ArgumentParser()
parser.add_argument('-g', help = 'generation numer 1 - 8')
args = parser.parse_args()

main(args)
    