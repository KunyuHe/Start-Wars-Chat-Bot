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

import os
import pandas as pd

HEADERS = ["Char", "Dial"]

DIALOGUES_DIR = "[Star-Wars-Chat-Bot]data/Dialogues/"
OUTPUT_DIR = "[Star-Wars-Chat-Bot]data/CleanDialogues/"


#----------------------------------------------------------------------------#
def process_data_chunk(chunk, file):
    """
    Given a chunk of dataframe (dialogues between two ===\t===), combines
    characters words until the character changes and writes the processed
    dialogues to a cleaned dialogue file.

    Inputs:
        - chunk (pandas.DataFrame): a chunk of dialogue data
        - file (string): name of data source (the dialogue file)

    Returns:
        (None) append to the output file
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
    Given the name of a dialogue file, reads in the dialogues as a dataframe,
    gets rids of consecutive duplicate separators ("===\t===") first, and
    divide the original dataframe into data chunks. Process the dialogues in
    each chunk and append to the output file chunk by chunk.

    Inputs:
        - file (string): name of data source (the dialogue file)

    Returns:
        (None) append to the output file chunk by chunk
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
    As we append cleaned dialogues chunk by chunk to the output file,
    everytime before data cleaning, deletes all the files in the output
    directory.

    Inputs:
        - path (string): path to the output directory

    Returns:
        (None) wipe out all the files in the output directory
    """
    for file in os.listdir(path):
        os.remove(path + file)

#----------------------------------------------------------------------------#
clear_output_directory()

for dialogue_file in os.listdir(DIALOGUES_DIR):
    clean_dialogue(dialogue_file)
