# %%
import pandas as pd
import bs4
import numpy as np


# %%
diseases = pd.read_csv('diseases_with_desc.csv')
diseases.dropna(inplace=True)

# %%
subAttr = {'data-attrid': 'subtitle'}
descAttr = {'data-attrid': 'kc:/medicine/disease:description'}
secondaryDescAttr = {'data-attrid': 'kc:/medicine/disease:long description'}
rarityAttr = {'data-attrid': 'kc:/medicine/disease:location prevalence title'}

symptomAttr = {'data-attrid': 'kc:/medicine/disease:detailed symptoms'}

# %%
diseases_complete = pd.DataFrame()
diseases_complete['disease'] = diseases['disease']
diseases_complete['cleaned_disease'] = diseases['cleaned_disease']
diseases.drop_duplicates('cleaned_disease', inplace=True)
diseases_complete.drop_duplicates('cleaned_disease', inplace=True)

# %%
def filterSubtitles(descDiv):
    soup = bs4.BeautifulSoup(descDiv, 'html.parser')
    subtitleElement = soup.find('div', subAttr)
    if subtitleElement is not None:
        return subtitleElement.text

def filterPrimaryDescriptions(descDiv):
    soup = bs4.BeautifulSoup(descDiv, 'html.parser')
    primaryDescElement = soup.find('div', descAttr)
    if primaryDescElement is not None:
        return primaryDescElement.text

def filterSecondaryDescriptions(descDiv):
    soup = bs4.BeautifulSoup(descDiv, 'html.parser')
    secondaryDescElement = soup.find('div', secondaryDescAttr)
    if secondaryDescElement is not None:
        return secondaryDescElement.text

def filterRarity(descDiv):
    soup = bs4.BeautifulSoup(descDiv, 'html.parser')
    rarityElement = soup.find('div', rarityAttr)
    if rarityElement is not None:
        return rarityElement.text

def getSymptomPossibility(symptomDiv):
    soup = bs4.BeautifulSoup(symptomDiv, 'html.parser')
    symptomPossibility = soup.find('div', symptomAttr)
    if symptomPossibility is not None:
        return symptomPossibility.text

diseases_complete['subtitle'] = diseases['desc'].apply(filterSubtitles)
diseases_complete['primary_description'] = diseases['desc'].apply(filterPrimaryDescriptions)
diseases_complete['secondary_description'] = diseases['desc'].apply(filterSecondaryDescriptions)
diseases_complete['rarity'] = diseases['desc'].apply(filterRarity)
diseases_complete['symptom_possibility'] = diseases['sympt'].apply(getSymptomPossibility)
diseases_complete.reset_index(inplace=True)
diseases.reset_index(inplace=True)
diseases_complete.drop('index', axis=1, inplace=True)


# %%
basic_kinds = {'Cough', 'Headache'}
vague_kinds = {'Common symptoms', 'Pain circumstances', 'Pain types'}

diseases_complete['symptoms'] = np.NaN

for sym, cleaned_disease in zip(diseases['sympt'], diseases['cleaned_disease']):
    soup = bs4.BeautifulSoup(sym, 'html.parser')
    symptomSets = soup.find_all('div', symptomAttr)[1:]
    if len(symptomSets) > 0:
        symptoms = []
        symptomPairs = [symptomSet.text.split(':') for symptomSet in symptomSets]
        for pair in symptomPairs:
            if pair[0] in basic_kinds:
                symptoms.append(pair[0])
            elif pair[0] in vague_kinds:
                continue
            elif pair[0] == 'Pain areas':
                raw_symptoms = pair[1].replace(' in the ', ' ')
                raw_symptoms = raw_symptoms.replace(' of the ', ' ')
                raw_symptoms = raw_symptoms.replace(' or ', ' ')
                raw_symptoms = raw_symptoms.replace(', ', ' ')
                raw_symptoms = [area + ' pain' for area in raw_symptoms.split(' ')]
                raw_symptoms = [area for area in raw_symptoms if area != ' pain']
                symptoms += raw_symptoms
            else:
                raw_symptoms = pair[1].replace(' and ', ', ')
                raw_symptoms = raw_symptoms.replace(' or ', ', ')
                raw_symptoms = raw_symptoms.replace(' the ', ' ')
                raw_symptoms = raw_symptoms.split(', ')
                raw_symptoms = [symptom for symptom in raw_symptoms if symptom != '']
                symptoms += raw_symptoms
        if len(symptoms) > 0:
            diseases_complete.loc[diseases_complete['cleaned_disease'] == cleaned_disease, 'symptoms'] = ', '.join(symptoms)

# %%
import json

def getRawSymptomsList(symptomDiv):
    soup = bs4.BeautifulSoup(symptomDiv, 'html.parser')
    symptomSets = soup.find_all('div', symptomAttr)[1:]
    if len(symptomSets) > 0:
        return json.dumps([symptomSet.text for symptomSet in symptomSets])

diseases_complete['raw_symptoms'] = diseases['sympt'].apply(getRawSymptomsList)
diseases_complete.to_csv('diseases_complete.csv', index=False)


