"""
Title:       get_dialogues.py
Description: To parse Star Wars scripts (.txt) in to dialogue
             documents
Input file: ([Star-Wars-Chat-Bot]data/Scripts/..) ->
Output file: ([Star-Wars-Chat-Bot]data/Dialogues/..):
            EpisodeIV_script.txt -> EpisodeIV_dialogues.tsv
            EpisodeV_script.txt -> EpisodeV_dialogues.tsv
            EpisodeVI_script.txt -> EpisodeVI_dialogues.tsv
            EpisodeIII_script.txt -> EpisodeIII_dialogues.tsv
            EpisodeII_script.txt -> EpisodeII_dialogues.tsv
Author:      Kunyu He
"""
# pylint: disable=redefined-outer-name, invalid-name, dangerous-default-value


import re

# Party line of names
NAME_DICT = {'BEN': "OBI-WAN",
             'THREEPIO': "C-3PO",
             'DARTH SlDIOUS': "DARTH SIDIOUS",
             'PALPATINE': "DARTH SIDIOUS",
             'EMPEROR': "DARTH SIDIOUS",
             'FlRESHIP PILOT': "FIRESHIP PILOT",
             'GlDDEAN DANU': "GIDDEAN DANU",
             'GiDDEAN DANU': "GIDDEAN DANU",
             'Kl-ADI-MUNDI': "KI-ADI-MUNDI",
             'TlON MEDON': "TION MEDON",
             'MACE WlNDU': "MACE WINDU",
             'MACE WiNDU': "MACE WINDU",
             'FANGZAR': "FANG ZAR",
             'QUI -GON': "QUI-GON",
             'PADMÉ': "PADME",
             'CORDÉ': "CORDE"}


#----------------------------------------------------------------------------#
def read_script(name, encoding=None):
    """
    Given name of the script file, reads it with assigned encoding method and
    returns a list of lines in the script with newline char removed.

    Inputs:
        name (string): name and extension of the script text file
        encoding (string): encoding method of the script file, i.e. 'gbk'

    Outputs:
        (list of strings) of lines in the script with newline char removed
    """
    with open('[Star-Wars-Chat-Bot]data/Scripts/' + name, 'r',
              encoding=encoding) as f:
        return [line.rstrip("\n") for line in f.readlines()]


def line_type(line, num_spaces):
    """
    Given a line, determines its type rouoghly by counting leading white
    spaces. Returns True if it equals to the desired number.

    Inputs:
        - line (string): a line from the list to check
        - num_spaces (int): number of spaces desired

    Returns:
        (Bool) True if the number of leading white spaces equals to our
        desired number
    """
    return len(line) - len(line.lstrip()) == num_spaces


def clean_name(line, name_party_line=NAME_DICT):
    """
    Given a line containing a name, parses the line and returns the name.

    Inputs:
        - line (string): a name line from the list
        - name_party_line (dict): takes care of wrong spellings

    Returns:
        (string) cleaned name
    """
    name = line.strip()
    if "'S" in name:
        name = re.search(r"^[A-Z0-9\s]+[^']", name).group().strip()

    if "(" in name:
        name = re.search(r"[\w]+[^(]", name).group().strip()
    name = name_party_line.get(name, name)

    name = re.search(r"^[A-Z0-9&\s-]+[^a-z#]", name)
    if not name:
        return None

    return name.group().strip()


def write_dialogue(condition, cond_line, write_line, file):
    """
    Given a dialogue line, write it into the tsv file under the assigned
    condition.

    Inputs:
        - condition (a function): evaluates to True or False
        - cond_line (string): a line from the script to check the condition
        - write_line (string): a line from the script to write
        - file (TextIOWrapper): connection to the .tsv file

    Returns:
        (None)
    """
    if condition(cond_line):
        file.write(write_line.strip() + "\n")
    else:
        file.write(write_line.strip() + " ")


# Star Wars Episode IV: A New Hope-------------------------------------------#
script = read_script('EpisodeIV_script.txt')
f = open('[Star-Wars-Chat-Bot]data/Dialogues/EpisodeIV_dialogues.tsv', 'w')

for i in range(50, len(script) - 1):
    line, next_line = script[i], script[i + 1]

    if line_type(line, 20):
        name = clean_name(line, {key: val for key, val in NAME_DICT.items()
                                 if key != "CREATURE"})
        if not name:
            continue
        f.write(name + '\t')

    elif line_type(line, 10):
        write_dialogue(lambda x: not x.strip(), next_line, line, f)

f.close()


# Star Wars Episode V: The Empire Strikes Back-------------------------------#
script = read_script('EpisodeV_script.txt')
f = open('[Star-Wars-Chat-Bot]data/Dialogues/EpisodeV_dialogues.tsv', 'w')

for i in range(60, len(script) - 1):
    line, next_line = script[i], script[i + 1]

    if ":" in line:
        name, dialogue = line.split(":")
        if name in ["INTERIOR", "EXTERIOR"]:
            continue

        name = clean_name(name, NAME_DICT)
        if not name:
            continue

        dialogue = re.sub(r"[\(\[].*?[\)\]]", "", dialogue).strip()
        write_dialogue(lambda x: not x.strip(), next_line,
                       name + "\t" + dialogue, f)

    elif line and line_type(line, 0):
        write_dialogue(lambda x: not x.strip() or not line_type(x, 0),
                       next_line, line, f)

f.close()


# Star Wars Episode VI: Return of the Jedi-----------------------------------#
script = read_script('EpisodeVI_script.txt')
f = open('[Star-Wars-Chat-Bot]data/Dialogues/EpisodeVI_dialogues.tsv', 'w')

for i in range(70, len(script) - 1):
    line, next_line = script[i], script[i + 1]

    if line_type(line, 30):
        name = clean_name(line, NAME_DICT)
        if not name or name == "FADE OUT":
            continue
        f.write(name + "\t")

    elif line_type(line, 15):
        write_dialogue(lambda x: not x.strip(), next_line, line, f)

f.close()


# Star Wars Episode III: Revenge of the Sith---------------------------------#
script = read_script('EpisodeIII_script.txt')
f = open('[Star-Wars-Chat-Bot]data/Dialogues/EpisodeIII_dialogues.tsv', 'w')

for line in script:
    if ":" in line and len(line) == len(line.lstrip()):
        name, dialogue = line.split(":", 1)
        name = clean_name(name, NAME_DICT)
        f.write(name.strip() + "\t" +
                re.sub(r"[\(\[].*?[\)\]]", "", dialogue).strip() + "\n")

f.close()


# Star Wars Episode II: Attack of the Clones---------------------------------#
script = read_script('EpisodeII_script.txt', encoding='utf-8')
f = open('[Star-Wars-Chat-Bot]data/Dialogues/EpisodeII_dialogues.tsv', 'w',
         encoding='utf-8')

for i in range(30, len(script) - 1):
    line, next_line = script[i], script[i + 1]

    if line_type(line, 16) and ("(") not in line:
        name = clean_name(line, NAME_DICT)
        if not name:
            continue
        f.write(name + "\t")

    elif line_type(line, 12):
        write_dialogue(lambda x: not x.strip(), next_line, line, f)

f.close()