"""
Title:       etl_get_training_data.py
Description: get padded and tokenized questions and answer pickle files for
             model training
Input file: ([Star-Wars-Chat-Bot]data/CleanDialogues/..) ->
Output file: ([Star-Wars-Chat-Bot]train/temp/..)
Author:      Kunyu He
"""
# pylint: disable=redefined-outer-name, invalid-name, too-many-arguments, import-error

import pickle
from itertools import chain
import nltk
import numpy as np

from keras.preprocessing import sequence
from etl_clean_dialogues import clear_output_directory

INPUT_DIR = "[Star-Wars-Chat-Bot]data/ByCharacter/"
OUTPUT_DIR = "[Star-Wars-Chat-Bot]train/temp/"

WORD_INDEX = 0
UNKNOWN_TOKEN = "something"

CHARS = ["ANAKIN", "OBI-WAN", "LUKE", "YODA", "MACE WINDU"]


#----------------------------------------------------------------------------#
def get_inputs(chars):
    """
    Given a list of character names from console input, read corresponding
    question and answer files, combine both into whole text.

    Inputs:
        - ([string]): list of character names

    Returns:
        (tuple of string) question text, answer text, and whole text
    """
    questions = ""
    answers = ""

    for char in chars:
        with open(INPUT_DIR + char + "_Q.txt") as q:
            questions += q.read()
        with open(INPUT_DIR + char + "_A.txt") as a:
            answers += a.read()

    return questions, answers, questions + answers


def build_vocab(text, max_vocab=7000):
    """
    Given whole text, build and store vocabulary dict.

    Inputs:
        - text (string): whole text extracted from pickle files
        - max_vob (int): number of unique words allowed in the list

    Returns:
        ({word: int}) dictionary of words to frequency
    """
    tokenized_text = " ".join(text).split()
    vocab = nltk.FreqDist(chain(tokenized_text)).most_common(max_vocab - 1)

    with open(OUTPUT_DIR + "vocab", 'wb') as f:
        pickle.dump(vocab, f)

    return vocab


def get_data(tokenized_text, word_dict, question=True,
             maxlen_output=50, maxlen_input=50, unknown_token=UNKNOWN_TOKEN):
    """
    Given the tokenized text (either questions or answers), vectorize and pad
    the text, and then store it.

    Inputs:
        - tokenized_text ([[string]])
        - word_dict ({word: int})
        - question (bool): flag whether the text is question test
        - maxlen_output (int): maximum length of output list
        - maxlen_input (int): maximum length of input list
        - unknown_token (string): prepared word for replacement

    Returns:
        (None)
    """
    for i, sentence in enumerate(tokenized_text):
        tokenized_text[i] = [word if word in word_dict else unknown_token
                             for word in sentence]
    word_vec = np.asarray([[word_dict[word] for word in sentence]
                           for sentence in tokenized_text])
    if not question:
        answer = sequence.pad_sequences(word_vec, maxlen=maxlen_output,
                                        padding='post')
        with open(OUTPUT_DIR + "padded_answers", 'wb') as f:
            pickle.dump(answer, f)
    else:
        question = sequence.pad_sequences(word_vec, maxlen=maxlen_input)
        with open(OUTPUT_DIR + "padded_questions", 'wb') as f:
            pickle.dump(question, f)


#----------------------------------------------------------------------------#
if __name__ == "__main__":
    clear_output_directory(OUTPUT_DIR)

    question, answer, whole_text = get_inputs(CHARS)
    tokenized_q = [("BOS " + row + " EOS").split()
                   for row in question.split("\n")]
    tokenized_a = [("BOS " + row + " EOS").split()
                   for row in answer.split("\n")]
    whole_text = ["BOS " + row + " EOS" for row in whole_text.split("\n")]

    vocab_dict = build_vocab(whole_text)
    word_lst = [pair[WORD_INDEX] for pair in vocab_dict]
    word_lst.append(UNKNOWN_TOKEN)
    word_dict = {word: index for index, word in enumerate(word_lst)}

    get_data(tokenized_q, word_dict, question=True)
    get_data(tokenized_a, word_dict, question=False)
