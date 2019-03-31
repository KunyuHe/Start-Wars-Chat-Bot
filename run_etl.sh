#!/bin/bash

pip install --user -r requirements.txt
sudo apt-get install python3-tk

python etl_get_scripts_bs4.py
python etl_get_dialogues.py
python etl_clean_dialogues.py
python etl_get_character_dialogues.py
python etl_get_training_data.py
