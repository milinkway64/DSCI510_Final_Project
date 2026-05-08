import requests
from bs4 import BeautifulSoup
import pandas as pd


def state_name_raw():
    url = "https://www.faa.gov/air_traffic/publications/atpubs/cnt_html/appendix_a.html"
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    name_lst = []
    abbr_lst = []
    per_row = table.find_all("td")
    for i in range(0, len(per_row), 2):
        state = per_row[i].text.strip()
        name_lst.append(state)
        abbr = per_row[i+1].text.strip()
        abbr_lst.append(abbr)
    state_dict = {}
    state_dict["State Name"] = name_lst
    state_dict["Abbr"] = abbr_lst
    df = pd.DataFrame(state_dict)
    df.to_csv("../data/raw/state_abbr.csv", index=False)