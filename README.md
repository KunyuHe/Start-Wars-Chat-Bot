# Chat with the Jedi Masters - JediChat

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c1997cf03119405d9ccb17bfd9fbf373)](https://app.codacy.com/app/kunyuhe/Star-Wars-Chat-Bot?utm_source=github.com&utm_medium=referral&utm_content=KunyuHe/Star-Wars-Chat-Bot&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.com/KunyuHe/Star-Wars-Chat-Bot.svg?branch=master)](https://travis-ci.com/KunyuHe/Star-Wars-Chat-Bot) [![Maintainability](https://api.codeclimate.com/v1/badges/51bb1108bff035ba0a56/maintainability)](https://codeclimate.com/github/KunyuHe/Star-Wars-Chat-Bot/maintainability) [![codecov](https://codecov.io/gh/KunyuHe/Star-Wars-Chat-Bot/branch/master/graph/badge.svg)](https://codecov.io/gh/KunyuHe/Star-Wars-Chat-Bot) [![HitCount](http://hits.dwyl.io/KunyuHe/Star-Wars-Chat-Bot.svg)](http://hits.dwyl.io/KunyuHe/Star-Wars-Chat-Bot) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)

JediChat is a dialogue system that chats like a Star Wars character (do not have to be one of the Jedi masters) in text conversations with you.

If you want to further customize JediChat or include another character that you would like to chat with, download this repository and follow the guides below to manually set things up on your local machine.

## Data Source

We train JediChat based on dialogues from Star Wars IV, V, VI, and II, III movie scripts. We download scripts for IV, V and VI from [Gaston Sanchez's repo](https://github.com/gastonstat/StarWars/tree/master/Text_files), and parse the scripts for II and III from the [Internet Movie Script Database (IMSDb)](https://www.imsdb.com/).

All logos, characters, artwork, stories, information, names, and other elements associated thereto, are the sole and exclusive property of [Lucasfilm Limited](https://www.lucasfilm.com/). The content licensing of this repo does NOT apply to the original works and trademarked names.

In order to get better training outcomes, we combine our data with dialogue data from [Cornell Movie--Dialogs Corpus](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html). We use both data to train our chatbot so that it responds reasonably.

## Setup

Check a list of denpendencies [here](https://github.com/KunyuHe/Star-Wars-Chat-Bot/network/dependencies). To download them, run the following commands in the repo directory (where you place the downloads) under the environment you prefer:

```(bash)
$ pip install --user -r requirements.txt
```

## Prepare & Customize Data

The ETL (Extract-Transform-Load) process is executed by the following python scripts:

*   `etl_get_scripts_bs4.py`: parse Star Wars scripts from IMSDb with `BeautifulSoup` and save them into `.txt` files [here](https://github.com/KunyuHe/Star-Wars-Chat-Bot/tree/master/%5BStar-Wars-Chat-Bot%5Ddata/Scripts).
*   `etl_get_dialogues.py`: extract dialogues from movie scripts segmented by scene in to dialogue files (.tsv) [here](https://github.com/KunyuHe/Star-Wars-Chat-Bot/tree/master/%5BStar-Wars-Chat-Bot%5Ddata/Dialogues).
*   `etl_clean_dialogues.py`: clean the dialogue files by combining consecutive sentences by the same character within each scene and store the cleaned dialogue files [here](https://github.com/KunyuHe/Star-Wars-Chat-Bot/tree/master/%5BStar-Wars-Chat-Bot%5Ddata/CleanDialogues).
*   `etl_get_character_dialogues.py`: get dialogues that the characters of interest are involved and store the output [here](https://github.com/KunyuHe/Star-Wars-Chat-Bot/tree/master/%5BStar-Wars-Chat-Bot%5Ddata/ByCharacter).
*   `etl_get_training_data.py`: get padded and tokenized questions and answer pickle files for model training [here](https://github.com/KunyuHe/Star-Wars-Chat-Bot/tree/master/%5BStar-Wars-Chat-Bot%5Dtrain/temp).

If you want to execute these python scripts manually, note that you have to run them in the specific order and no further arguments are needed. Or you can run the prepared shell script with:

```(bash)
$ chmod u+x run_etl.sh
$ run_etl.sh
```

If you want to customize and train your JediChat based on dialogues of a character that's not pre-included, you need to customize input data for training. You can do that by modifying the list `CHARS` (of pre-included characters) in the `etl_get_character_dialogues.py` script. Include the character of your choice at the end of the list and run the shell script again.

## Model Training & Customize

The model training part is based on Oswaldo Ludwig's repo [Seq2seq-Chatbot-for-Keras](https://github.com/oswaldoludwig/Seq2seq-Chatbot-for-Keras). We use a new generative model of chatbot based on `seq2seq modeling`. Further details on this model can be found in Section 3 of the paper [End-to-end Adversarial Learning for Generative Conversational Agents](https://www.researchgate.net/publication/321347271_End-to-end_Adversarial_Learning_for_Generative_Conversational_Agents).

The architecture presented here assumes the same prior distributions for input and output words. Therefore, it shares an embedding layer ([Glove pre-trained word embedding](https://nlp.stanford.edu/projects/glove/?fbclid=IwAR1JVmPTDh37oXeHvdXtyqIEeFd7vcZoaideVsOHK4pnod6rXNGM71NL-8E)) between the encoding and decoding processes through the adoption of a new model.

The weights are fine tuned in `train_seq2seq.py`. To chat with our pre-trained Jedi Masters, just run `JediChat.py`. The model we use here is based on our pretrained weights [here](https://www.dropbox.com/s/ss8nnkfzgwazfyy/JediChatPreTrained.h5?dl=0) based on both Cornell movie and Star Wars movie dialogues. You can switch to another set of weights pre-trained solely on Star Wars movie dialogues [here](https://drive.google.com/drive/folders/1URT-lZdYWQWTLFuR3oSC09EKkHCBrcI7?usp=sharing). Just need to modify the `weights_file` variable in the `JediChat.py` script.
