##############################################################################
# Title:       [Star-Wars-Chat-Bot]_GetScripts_BeautifulSoup.py
# Description: To get Star Wars scripts from `https://www.imsdb.com/scripts/`
#              with bs4 and save them into .txt files
# Input file:  None -> Output file: ([Star-Wars-Chat-Bot]data/Scripts/..):
#     -> EpisodeIII_script.txt
#     -> EpisodeII_script.txt
#     -> EpisodeI_script.txt
# Author:      Kunyu He
##############################################################################

import requests
import bs4


#----------------------------------------------------------------------------#
def get_script_from_url(url, file_name, lst_to_replace, encoding=None):
    """
    """
    page = requests.get(url).text.encode('iso-8859-1')
    soup = bs4.BeautifulSoup(page, "html5lib")
    script = soup.find('td', class_ = "scrtext").text

    if not encoding:
        with open('[Star-Wars-Chat-Bot]data/Scripts/' + file_name, 'w') as f:
            f.write(script.replace(*lst_to_replace))
    else:
        with open('[Star-Wars-Chat-Bot]data/Scripts/' + file_name, 'wb') as f:
            f.write(script.replace(*lst_to_replace).encode(encoding))


# Star Wars Episode III: Revenge of the Sith---------------------------------#
url = "https://www.imsdb.com/scripts/Star-Wars-Revenge-of-the-Sith.html"
get_script_from_url(url, "EpisodeIII_script.txt", ["\xa0", " "])


# Star Wars Episode II: Attack of the Clones---------------------------------#
url = "https://www.imsdb.com/scripts/Star-Wars-Attack-of-the-Clones.html"
get_script_from_url(url, "EpisodeII_script.txt", ["\t", "    "],
                    encoding='utf8')


#