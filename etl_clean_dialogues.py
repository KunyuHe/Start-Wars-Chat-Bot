"""
Title:       etl_clean_dialogues.py
Description: To clean the dialogue document
Input file: ([Star-Wars-Chat-Bot]data/Dialogues/..) ->
Output file: ([Star-Wars-Chat-Bot]data/CleanDialogues/..):
            EpisodeIV_dialogues.tsv -> EpisodeIV_dialogues_clean.tsv
            EpisodeV_dialogues.tsv -> EpisodeV_dialogues_clean.tsv
            EpisodeVI_dialogues.tsv -> EpisodeVI_dialogues_clean.tsv
            EpisodeIII_dialogues.tsv -> EpisodeIII_dialogues_clean.tsv
            EpisodeII_dialogues.tsv -> EpisodeII_dialogues_clean.tsv
Author:      Kunyu He
"""

import pandas as pd
import os

HEADERS = ["Char", "Dial"]

DIALOGUES_DIR = "[Star-Wars-Chat-Bot]data/Dialogues/"
OUTPUT_DIR = "[Star-Wars-Chat-Bot]data/CleanDialogues/"


#----------------------------------------------------------------------------#
def process_data_chunk(chunk, file):
    """
    """
    chunk['Continues'] = chunk.Char.shift() == chunk.Char
    clean_lst = []

    for row in chunk.itertuples(index=False):
        if not row.Continues:
            clean_lst.append([row.Char, row.Dial])
        else:
            clean_lst[-1][-1] += " " + row.Dial

    with open(OUTPUT_DIR + file.replace(".tsv", "_clean.tsv"), 'a') as f:
        f.write("===\t===\n")
        pd.DataFrame(clean_lst).to_csv(f, sep="\t", header=False, index=False)


def clean_dialogue(file):
    """
    """
    data = pd.read_csv(DIALOGUES_DIR + file, delimiter="\t", header=None,
                       encoding='gbk')
    data.columns = HEADERS
    data = data[data.Dial.shift() != data.Dial]
    chunk_lst = []

    for row in data.itertuples(index=False):
        if row.Char == "===":
            chunk_df = pd.DataFrame(chunk_lst, columns=HEADERS)
            process_data_chunk(chunk_df, file)
            chunk_lst = []
        else:
            chunk_lst.append(list(row))

    return data


def clear_output_directory(path=OUTPUT_DIR):
    """
    """
    for file in os.listdir(path):
        os.remove(path + file)

#----------------------------------------------------------------------------#
files = os.listdir(DIALOGUES_DIR)
clear_output_directory()

for file in files:
    clean_dialogue(file)