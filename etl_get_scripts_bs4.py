"""
Title:       etl_get_scripts_bs4.py
Description: To get Star Wars scripts from `https://www.imsdb.com/scripts/`
             with bs4 and save them into .txt files
Input file:  None -> Output file: ([Star-Wars-Chat-Bot]data/Scripts/..):
                  -> EpisodeIII_script.txt
                  -> EpisodeII_script.txt
Author:      Kunyu He
"""

import requests
import bs4

from functools import reduce

REPLACE = [("\xa0", " "), ("\t", "    "), ("\xe9", "e"), ('\xc9', "E"),
           ("’", "'"), ("‘", "'")]


#----------------------------------------------------------------------------#
def get_script_from_url(url, name, lst_to_replace):
    """
    Takes a url and parse Star Wars script from the webpage (cerdit to:
    https://www.imsdb.com/scripts/) with BeautifulSoup. Write the parsed
    script as a .txt file and replace some characters.

    Inputs:
        - url (string): website url
        - name (string): output file name
        - lst_to_replace (list of strings): [string to be replaced,
                                             string for replacement]

    Returns:
        (None)
    """
    page = requests.get(url).text.encode('iso-8859-1')
    soup = bs4.BeautifulSoup(page, "html5lib")
    script = soup.find('td', class_="scrtext").text

    with open('[Star-Wars-Chat-Bot]data/Scripts/' + name, 'w') as file:
        file.write(reduce(lambda string, rep: string.replace(*rep),
                          lst_to_replace, script))


#----------------------------------------------------------------------------#
URL = "https://www.imsdb.com/scripts/Star-Wars-Revenge-of-the-Sith.html"
get_script_from_url(URL, "EpisodeIII_script.txt", REPLACE)

URL = "https://www.imsdb.com/scripts/Star-Wars-Attack-of-the-Clones.html"
get_script_from_url(URL, "EpisodeII_script.txt", REPLACE)
