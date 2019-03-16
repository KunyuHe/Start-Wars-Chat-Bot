# Chat with the Jedi Masters - JediChat

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c1997cf03119405d9ccb17bfd9fbf373)](https://app.codacy.com/app/kunyuhe/Star-Wars-Chat-Bot?utm_source=github.com&utm_medium=referral&utm_content=KunyuHe/Star-Wars-Chat-Bot&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.com/KunyuHe/Star-Wars-Chat-Bot.svg?branch=master)](https://travis-ci.com/KunyuHe/Star-Wars-Chat-Bot) [![Maintainability](https://api.codeclimate.com/v1/badges/51bb1108bff035ba0a56/maintainability)](https://codeclimate.com/github/KunyuHe/Star-Wars-Chat-Bot/maintainability) [![codecov](https://codecov.io/gh/KunyuHe/Star-Wars-Chat-Bot/branch/master/graph/badge.svg)](https://codecov.io/gh/KunyuHe/Star-Wars-Chat-Bot) [![HitCount](http://hits.dwyl.io/KunyuHe/Star-Wars-Chat-Bot.svg)](http://hits.dwyl.io/KunyuHe/Star-Wars-Chat-Bot) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)

JediChat is a dialogue system that chats like a Star Wars character (do not have to be one of the Jedi masters) in text conversations with you. [Try it out]()!

If you want to further customize JediChat or include another character that you would like to chat with, download this repository and follow the guides below to manually set things up on your local machine.

## Data Source

We train JediChat based on dialogues from Star Wars IV, V, VI, and II, III movie scripts. We download scripts for IV, V and VI from [Gaston Sanchez's repo](https://github.com/gastonstat/StarWars/tree/master/Text_files), and parse the scripts for II and III from the [Internet Movie Script Database (IMSDb)](https://www.imsdb.com/).

All logos, characters, artwork, stories, information, names, and other elements associated thereto, are the sole and exclusive property of [Lucasfilm Limited](https://www.lucasfilm.com/). The content licensing of this repo does NOT apply to the original works and trademarked names.

## Setup

Check a list of denpendencies [here](https://github.com/KunyuHe/Star-Wars-Chat-Bot/network/dependencies). To download them, run the following commands in the repo directory (where you place the downloads) under the environment you prefer:

```(bash)
$ pip install -r requirements.txt
```

## Prepare & Customize Data

The ETL (Extract-Transform-Load) process is executed by the following python scripts:

*   `etl_get_scripts_bs4.py`: parse Star Wars scripts from IMSDb with `BeautifulSoup` and save them into `.txt` files [here](https://github.com/KunyuHe/Star-Wars-Chat-Bot/tree/master/%5BStar-Wars-Chat-Bot%5Ddata/Scripts).
*   `etl_get_dialogues.py`: extract dialogues from movie scripts segmented by scene in to dialogue files (.tsv) [here](https://github.com/KunyuHe/Star-Wars-Chat-Bot/tree/master/%5BStar-Wars-Chat-Bot%5Ddata/Dialogues).
*   `etl_clean_dialogues.py`: clean the dialogue files by combining consecutive sentences by the same character within each scene and store the cleaned dialogue files [here](https://github.com/KunyuHe/Star-Wars-Chat-Bot/tree/master/%5BStar-Wars-Chat-Bot%5Ddata/CleanDialogues).
*   `etl_get_character_dialogues.py`: get dialogues that the characters of interest are involved and store the output [here](https://github.com/KunyuHe/Star-Wars-Chat-Bot/tree/master/%5BStar-Wars-Chat-Bot%5Ddata/ByCharacter).

If you want to execute these python scripts manually, note that you have to run them in the specific order and no further arguments are needed. Or you can run the prepared shell script with:

```(bash)
$ chmod u+x run_etl.sh
$ run_etl.sh
```

If you want to customize and train your JediChat based on dialogues of a character that's not pre-included, you need to customize input data for training. You can do that by modifying the list `CHARS` (of pre-included characters) in the `etl_get_character_dialogues.py` script. Include the character of your choice at the end of the list and run the shell script again.
