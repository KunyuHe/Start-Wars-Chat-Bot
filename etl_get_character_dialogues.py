"""
Title:       etl_get_character_dialogues.py
Description: To extract dialogues where the character of interest is involved
Input file: ([Star-Wars-Chat-Bot]data/CleanDialogues/..) ->
Output file: ([Star-Wars-Chat-Bot]data/ByCharacter/..)
    -> (Multiple, depend on the CHARS list)
Author:      Kunyu He
"""

import os
import csv
import shutil
import pandas as pd

from etl_clean_dialogues import clear_output_directory, process_dialogues

INPUT_DIR = "[Star-Wars-Chat-Bot]data/CleanDialogues/"
OUTPUT_DIR = "[Star-Wars-Chat-Bot]data/ByCharacter/"

HEADERS = ["Char", "Dial"]
CHARS = ["YODA", "LUKE", "C-3PO", "HAN", "LEIA", "PADME", "OBI-WAN", "ANAKIN",
         "MACE WINDU"]


#----------------------------------------------------------------------------#
def get_character_dials(chunk, characters):
    """
    Process a chunk of dialogue data. Check if the characters of interest are
    involved in the conversation. If so, append the dialogue chunk to an
    output file.

    Inputs:
        - chunk (pandas.DataFrame): chunk of dialogue data
        - characters ([string]): list of the characters of interet

    Returns:
        (None) append to corresponding output file
    """
    for character in characters:
        question = open(OUTPUT_DIR + character + "_Q.txt", 'a')
        answer = open(OUTPUT_DIR + character + "_A.txt", 'a')

        for index, char in chunk.Char.iteritems():
            if char == character and index >= 1:
                question.write(chunk.iloc[index - 1].Dial + "\n")
                answer.write(chunk.iloc[index].Dial + "\n")

        question.close()
        answer.close()


#----------------------------------------------------------------------------#
clear_output_directory(OUTPUT_DIR)

for dialogue_file in os.listdir(INPUT_DIR):
    data = pd.read_csv(INPUT_DIR + dialogue_file, delimiter="\t",
                       header=None, encoding='gbk')
    data.columns = HEADERS

    process_dialogues(get_character_dials, CHARS, data)
