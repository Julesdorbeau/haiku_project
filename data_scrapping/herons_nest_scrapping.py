import bs4
from bs4 import BeautifulSoup
from langdetect import detect
import pandas as pd
import requests
import re

def parsing_archive_page(archive_page_link) :
    """
    Parses an archive page of haikus and returns a list of haikus.

    This function iterates through pages of an archive, fetching and parsing haikus from each page until it encounters a 404 error or a redirect.

    Args:
        archive_page_link (str): The base URL of the archive page without the page number and extension.

    Returns:
        list: A list of haikus, where each haiku is represented as a list of three strings (each string being a line of the haiku).
    """
    page_index = 1

    # List to store all the haikus 
    archive_haikus_list = []

    # Loop to get all the possible pages
    archive_parsing = True
    while archive_parsing :
        # Getting the final link and doing the request
        archive_link = archive_page_link + str(page_index) + ".html"
        # print(f"Parsing page {archive_link}...")
        response_archive = requests.get(archive_link, headers={"User-Agent": "XY"})

        # Checking the status of the request (if we got a 404 or not) and the link of the request (if we got redirected)
        response_status = response_archive.status_code
        response_link = response_archive.request.url
        
        # If we have a successful request, then we are parsing it
        if response_status != 404 and (response_link == archive_link) :
            archive_soup = bs4.BeautifulSoup(response_archive.text)

            # Parsing the texts
            haikus_html_list = archive_soup.body.find_all('p', {'class':"haiku"})

            # Now getting the corps
            for haiku in haikus_html_list :
                haiku_corps = haiku.text.split('\n')
                if len(haiku_corps) == 3 :
                    haiku_corps = [re.sub(r'\xa0', '', haiku_text) for haiku_text in haiku_corps]
                    haiku_corps = [haiku_text.strip() for haiku_text in haiku_corps]
                    archive_haikus_list.append(haiku_corps)
        else :
            archive_parsing = False
        
        page_index += 1
    return archive_haikus_list


def parse_heronsnest_haikus(verbose = False) :
    """
    Parses haikus from The Heron's Nest archives and returns them in a dictionary.

    This function fetches the archive page of The Heron's Nest, extracts the links to individual archive months, and then parses haikus from each month's archive page.

    Args:
        verbose (bool, optional): If True, prints detailed information about the parsing process. Defaults to False.

    Returns:
        dict: A dictionary where the keys are the month identifiers and the values are lists of haikus. Each haiku is represented as a list of three strings (each string being a line of the haiku).
    """
    response = requests.get("https://theheronsnest.com/archives.html", headers={"User-Agent": "XY"})
    soup = bs4.BeautifulSoup(response.text)
    archives_href = [i['href'] for i in soup.body.section.find_all('a', href=True)]

    haikus_dict = {}

    for href_month in archives_href :
        # Setting up the link for the request 
        splitted_link = href_month.split("/")
        archive_page_link = splitted_link[0] + "//" + splitted_link[2] + "/" + splitted_link[3]+ "/haiku-p"

        if splitted_link[3] == "Archives" :
            continue

        # List to store all the haikus 
        archive_haikus_list = parsing_archive_page(archive_page_link)
        
        if len(archive_haikus_list) == 0 : 
            print("Warning : Must do a different parsing for this page !")
        
        haikus_dict[splitted_link[3]] = archive_haikus_list

        if verbose :
            print("Paring haikus of : " + splitted_link[3])
            print(f"Parsed {len(archive_haikus_list)} haikus !\n")

    return haikus_dict


def heronsnest_to_csv(parsed_haikus) :
    """
    Converts parsed haikus from The Heron's Nest into a CSV format.

    This function takes a dictionary of parsed haikus, where each key is a month identifier and the value is a list of haikus. It then flattens this dictionary into a list of haikus and converts it into a pandas DataFrame with appropriate column names.

    Args:
        parsed_haikus (dict): A dictionary where the keys are month identifiers and the values are lists of haikus. Each haiku is represented as a list of three strings (each string being a line of the haiku).

    Returns:
        pandas.DataFrame: A DataFrame containing the haikus with columns "line_1", "line_2", "line_3", and "source".
    """
    cols_names = ["line_1", "line_2", "line_3"]
    csv_list = []
    for month in parsed_haikus :
        csv_list.extend(parsed_haikus[month])
    csv = pd.DataFrame(csv_list, columns=cols_names)
    csv["source"] = "herons_nest"
    return csv