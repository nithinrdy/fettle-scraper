#!/bin/sh

printf "Installing dependencies...\n"
pip install -r requirements.txt 1> /dev/null

printf "Dependencies in place!\n\n"

printf "\nRunning scraper\n"
printf "This will take (quite) a while...\n\n"
python bashable_scripts/scraper_script.py

printf "Scraping complete! "
printf "Formatting scraped HTML...\n\n"
python bashable_scripts/html_transform_script.py

printf "Formatting complete! "
printf "Generating encoded CSV with sentence transformer embeddings...\n\n"
python bashable_scripts/embedder_script.py 1> /dev/null

rm -rf output
mkdir output
cp ./diseases__encoded.csv output/

printf "Cleaning up...\n\n"
rm -rf *.csv

printf "CSV generation complete! You can find it in the output directory.\n"
