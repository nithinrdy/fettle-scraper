# Notebooks (and scripts) for scraping disease data

## Overview

Contains three separate scripts for scraping, and then processing, disease data from the web.

- `scraper_script.py` - scrapes a list of diseases, and then their corresponding details (such as symptoms) and saves it to a csv file.
- `html_transform_script.py` - Formats the scraped (mainly) HTML data so that it's easier to work with (splitting descriptions into primary and secondary, extracting symptoms -- in human readable form (i.e. 'raw_symptoms', just the way they were scraped) and in space-separated form, stitched together after removing vague/indeterministic symptoms to allow for easy generating of vector embeddings).
- `embedder_script.py` - Generates vector embeddings for the symptoms, and saves them to a csv file (diseases__encoded.csv).

## But Nithin, why do you have the exact same code in the form of notebooks and scripts?

That's a wonderful question, my dear internet stranger. I'd originally written all three pieces of code as notebooks, as I find them much easier to work with (easier to focus on small cells of code, compared to a humongous script). Sounds fine, what's the catch?

Well, when I later decided to add a small bash script to automate the whole thing, I, for the life of me, couldn't figure out how to execute the notebooks (or rather, the cells within them) from a shell script.

The busy (read _lazy_) person that I am, I decided to export the notebooks as scripts and work with _them_ instead, and here we are.

## Usage

1. Clone the repo.
2. Make sure you have python installed (preferably, set up a virtual environment for this project while you're at it).
3. Make the script executable: `chmod +x generate_csv.sh`
4. Run the script: `./generate_csv.sh`
5. Wait a decade or so (depending on your internet connection).
6. You should now have a csv file in the `output` directory. This is what fettle's flask web_app serves to the frontend.
