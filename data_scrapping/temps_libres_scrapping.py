import bs4
from bs4 import BeautifulSoup
from langdetect import detect
import pandas as pd
import requests
import re

# ========================================================================================================
# Parsing the haikus from the website "tempslibres" in French
# ========================================================================================================

def french_haikus_tempslibre_parsing(verbose=False) :
    """
    Parses French haikus from the Temps Libres website and returns them in a list.

    This function fetches the main page of French haikus from the Temps Libres website, extracts the links to individual haiku pages, and then parses haikus from each page.

    Args:
        verbose (bool, optional): If True, prints detailed information about the parsing process, including any errors encountered. Defaults to False.

    Returns:
        list: A list of haikus, where each haiku is represented as a list of strings (each string being a line of the haiku).
    """
    haikus_list = []
    response = requests.get("https://www.tempslibres.org/tl/tlphp/dbauteursl.php?lang=fr&lg=e", headers={"User-Agent": "XY"})
    soup = bs4.BeautifulSoup(response.text)
    archives_href = [i['href'] for i in soup.article.find_all('a', href=True)]

    for href in archives_href : 
        link =  "https://www.tempslibres.org/tl/tlphp/" + href
        href_response = requests.get(link, headers={"User-Agent": "XY"})
        href_soup = bs4.BeautifulSoup(href_response.text)
        haikus_href_list = href_soup.body.find_all('p', {"class": "haiku"})
        for haikus_href in haikus_href_list : 
            haiku_corps = haikus_href.text.split('\n')
            if len(haiku_corps) == 3 :
                haiku_corps = [re.sub(r'\xa0', '', haiku_text) for haiku_text in haiku_corps]
                haiku_corps = [re.sub(r'\r', '', haiku_text) for haiku_text in haiku_corps]
                haiku_corps = [re.sub(r'\‏', '', haiku_text) for haiku_text in haiku_corps]
                haiku_corps = list(filter(None, haiku_corps))
                if len(haiku_corps) == 2 :
                    if verbose :
                        print("Error with haiku : ")
                        print(haiku_corps)
                        print("SKIPPING\n")
                    continue
                
                haikus_list.append(haiku_corps)
                if verbose :
                    print(haiku_corps)
    
    return haikus_list

def french_tempslibre_to_csv(parsed_haikus) :
    """
    Converts parsed French haikus from the Temps Libres website into a CSV format.

    This function takes a list of parsed haikus, where each haiku is represented as a list of three strings (each string being a line of the haiku). It then converts this list into a pandas DataFrame with appropriate column names and adds a source column.

    Args:
        parsed_haikus (list): A list of haikus, where each haiku is represented as a list of three strings.

    Returns:
        pandas.DataFrame: A DataFrame containing the haikus with columns "line_1", "line_2", "line_3", and "source".
    """
    cols_names = ["line_1", "line_2", "line_3"]
    csv = pd.DataFrame(parsed_haikus, columns=cols_names)
    csv["source"] = "tempslibre"
    return csv

# ========================================================================================================
# Parsing the haikus from the website "tempslibres" in English
# ========================================================================================================

def parse_languages_haikus(texts_list) :
    """
    Parses haikus from a list of text lines and categorizes them by language.

    This function iterates through a list of text lines, grouping them into haikus. It then detects the language of each haiku and categorizes them into French or English lists.

    Args:
        texts_list (list): A list of strings, where each string is a line of text that may be part of a haiku.

    Returns:
        tuple: A tuple containing two lists:
            - fr_list (list): A list of French haikus, where each haiku is represented as a list of three strings.
            - en_list (list): A list of English haikus, where each haiku is represented as a list of three strings.
    """
    fr_list, en_list = [], [] 
    haiku_list = []
    haiku_string = ""
    # Looping into the texts
    for text  in texts_list : 
        # If we reached an empty line
        if text == '' :
            lang = detect(haiku_string)
            if lang == "fr" : 
                fr_list.append(haiku_list)
            elif lang == "en" :
                en_list.append(haiku_list)
            haiku_list = []
            haiku_string = ""

        # Otherwise, store the text
        else : 
            haiku_string += text + '\n'
            haiku_list.append(text)

    # At the end, check if there is an haiku and parse it
    if len(haiku_list) == 3 :
        lang = detect(haiku_string)
        if lang == "fr" : 
            fr_list.append(haiku_list)
        elif lang == "en" :
            en_list.append(haiku_list)
        haiku_list = []
    
    return fr_list, en_list

def english_haikus_tempslibre_parsing(verbose=False) :
    """
    Parses English haikus from the Temps Libres website and categorizes them by language.

    This function fetches the main page of English haikus from the Temps Libres website, extracts the links to individual haiku pages, and then parses haikus from each page. It categorizes the haikus into French and English lists based on language detection.

    Args:
        verbose (bool, optional): If True, prints detailed information about the parsing process, including the haikus being parsed. Defaults to False.

    Returns:
        tuple: A tuple containing two lists:
            - french_haikus_list (list): A list of French haikus, where each haiku is represented as a list of three strings.
            - english_haikus_list (list): A list of English haikus, where each haiku is represented as a list of three strings.
    """
    french_haikus_list = []
    english_haikus_list = []
    response = requests.get("https://www.tempslibres.org/tl/tlphp/dbauteursl.php?lang=en&lg=e", headers={"User-Agent": "XY"})
    soup = bs4.BeautifulSoup(response.text)
    archives_href = [i['href'] for i in soup.article.find_all('a', href=True)]

    for href in archives_href : 
        link =  "https://www.tempslibres.org/tl/tlphp/" + href
        href_response = requests.get(link, headers={"User-Agent": "XY"})
        href_soup = bs4.BeautifulSoup(href_response.text)
        haikus_href_list = href_soup.body.find_all('p', {"class": "haiku"})
        for haikus_href in haikus_href_list : 
            haiku_corps = haikus_href.text.split('\n')
            haiku_corps = [re.sub(r'\xa0', '', haiku_text) for haiku_text in haiku_corps]
            haiku_corps = [re.sub(r'\r', '', haiku_text) for haiku_text in haiku_corps]
            haiku_corps = [re.sub(r'\(', '', haiku_text) for haiku_text in haiku_corps]
            haiku_corps = [re.sub(r'\)', '', haiku_text) for haiku_text in haiku_corps]

            if len(haiku_corps) == 3 or len(haiku_corps) == 7 :
                haiku_parsed = parse_languages_haikus(haiku_corps)
                if len(haiku_parsed[0]) != 0 :
                    french_haikus_list.append(haiku_parsed[0][0])
                if len(haiku_parsed[1]) != 0 :
                    english_haikus_list.append(haiku_parsed[1][0])
            
            if verbose :
                print(haiku_corps)
    
    return french_haikus_list, english_haikus_list

def english_tempslibre_to_csv(parsed_haikus) :
    """
    Converts parsed English and French haikus from the Temps Libres website into CSV format.

    This function takes a tuple of parsed haikus, where the first element is a list of French haikus and the second element is a list of English haikus. Each haiku is represented as a list of three strings. It then converts these lists into pandas DataFrames with appropriate column names and adds a source column.

    Args:
        parsed_haikus (tuple): A tuple containing two lists:
            - parsed_haikus[0] (list): A list of French haikus, where each haiku is represented as a list of three strings.
            - parsed_haikus[1] (list): A list of English haikus, where each haiku is represented as a list of three strings.

    Returns:
        tuple: A tuple containing two pandas DataFrames:
            - csv_french (pandas.DataFrame): A DataFrame containing the French haikus with columns "line_1", "line_2", "line_3", and "source".
            - csv_english (pandas.DataFrame): A DataFrame containing the English haikus with columns "line_1", "line_2", "line_3", and "source".
    """
    cols_names = ["line_1", "line_2", "line_3"]
    csv_french = pd.DataFrame(parsed_haikus[0], columns=cols_names)
    csv_french["source"] = "tempslibre"
    csv_english = pd.DataFrame(parsed_haikus[1], columns=cols_names)
    csv_english["source"] = "tempslibre"
    return csv_french, csv_english