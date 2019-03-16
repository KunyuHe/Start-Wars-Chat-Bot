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
def clean_dialogue_chunk(chunk, file):
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
        pd.DataFrame(clean_lst).to_csv(f, sep="\t", header=False, index=False)
        f.write("===\t===\n")


def process_dialogues(fn, arg, data):
    """
    Divide the original dataframe into data chunks and use the given function
    to process the dialogues and append the results to the output file chunk
    by chunk.

    Inputs:
        - fn (function): function to process the chunk of dataframe
        - arg: argument for the function (can be list)
        - data (pandas.DataFrame): dialogue data read from .tsv file

    Returns:
        (None) append to the output file chunk by chunk
    """
    chunk_lst = []

    for row in data.itertuples(index=False):
        if row.Char == "===":
            chunk_df = pd.DataFrame(chunk_lst, columns=HEADERS)
            fn(chunk_df, arg)
            chunk_lst = []
        else:
            chunk_lst.append(list(row))


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
    data_df = pd.read_csv(DIALOGUES_DIR + dialogue_file, delimiter="\t",
                          header=None, encoding='gbk')
    data_df.columns = HEADERS
    data_df = data_df[data_df.Dial.shift() != data_df.Dial]

    process_dialogues(clean_dialogue_chunk, dialogue_file, data_df)
