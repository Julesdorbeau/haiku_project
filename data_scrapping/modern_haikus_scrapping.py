import bs4
from bs4 import BeautifulSoup
from langdetect import detect
import pandas as pd
import requests
import re

def parse_modern_haikus() :
    """
    Parses modern haikus from the Modern Haiku website and returns them in a list.

    This function fetches the main page of the Modern Haiku website, extracts the links to individual haiku pages, and then parses haikus from each page.

    Returns:
        list: A list of haikus, where each haiku is represented as a list of three strings (each string being a line of the haiku).
    """
    response = requests.get("https://www.modernhaiku.org/previousissue.html", headers={"User-Agent": "XY"})
    soup = bs4.BeautifulSoup(response.text)

    haikus_list = []
    href_link_list = soup.table.table.find_all('a', href=True)
    for href_link in href_link_list : # Can also be : soup.select('table table td p a')
        if not "MH-Archive" in href_link['href'] :
            href_response = requests.get("https://www.modernhaiku.org/" + href_link['href'].split("/")[0] + "/haiku.html", headers={"User-Agent": "XY"})
            href_soup = bs4.BeautifulSoup(href_response.text)

            for haiku in href_soup.select('table table table p') :
                haiku_corps = haiku.text.split('\n')
                haiku_corps = [haiku_text.strip() for haiku_text in haiku_corps]
                haiku_corps = list(filter(None, haiku_corps))

                if len(haiku_corps) == 3 :
                    haiku_corps = [re.sub(r'\xa0', '', haiku_text) for haiku_text in haiku_corps]
                    haiku_corps = [re.sub(r'\r', '', haiku_text) for haiku_text in haiku_corps]
                    haiku_corps = [re.sub(r'\(', '', haiku_text) for haiku_text in haiku_corps]
                    haiku_corps = [re.sub(r'\)', '', haiku_text) for haiku_text in haiku_corps]

                    haikus_list.append(haiku_corps)

    return haikus_list

def modern_haikus_to_csv(parsed_haikus) :
    """
    Converts parsed modern haikus from the Modern Haiku website into a CSV format.

    This function takes a list of parsed haikus, where each haiku is represented as a list of three strings (each string being a line of the haiku). It then converts this list into a pandas DataFrame with appropriate column names and adds a source column.

    Args:
        parsed_haikus (list): A list of haikus, where each haiku is represented as a list of three strings.

    Returns:
        pandas.DataFrame: A DataFrame containing the haikus with columns "line_1", "line_2", "line_3", and "source".
    """
    cols_names = ["line_1", "line_2", "line_3"]
    csv = pd.DataFrame(parsed_haikus, columns=cols_names)
    csv["source"] = "modern_haikus"
    return csv