import requests
import requests.packages.urllib3.util.connection as urllib3_cn
import socket
import bs4
import csv
import pandas as pd

def address_family():
    return socket.AF_INET


urllib3_cn.allowed_gai_family = address_family


# %%
alph = 'a'


def cdc_page_url(alphabet):
    return 'https://www.cdc.gov/diseasesconditions/az/' + alphabet + '.html'


disease_list = []

while alph != '{':
    page_response = requests.get(cdc_page_url(alph))
    soup = bs4.BeautifulSoup(page_response.text, 'html.parser')
    list = soup.find('div', {'class': 'az-content'}
                     ).findChild('ul').findChildren('li', recursive=False)
    for item in list:
        disease_list.append(item.findChild('a').getText())
    alph = chr(ord(alph) + 1)


# %%
with open('disease_list.csv', 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=['disease'])
    writer.writeheader()
    for disease in disease_list:
        writer.writerow({'disease': disease})
    csv_file.close()

diseases_df = pd.read_csv('disease_list.csv')


# %%
def remove_references(x):
    return x.split('see')[0]

def remove_appendations(x):
    if '-' in x:
        return x.split('-')[0]
    if '—' in x:
        return x.split('—')[0]
    else:
        return x

def clean_parentheses(x):
    if '(' not in x:
        return x
    else:
        cleaned_up = ''
        opening_split = x.split('(')
        for item in opening_split:
            closing_split = item.split(')')
            for phrase in closing_split:
                if len(phrase) > len(cleaned_up):
                    cleaned_up = phrase
        return cleaned_up

def clean_square_brackets(x):
    if '[' not in x:
        return x
    else:
        cleaned_up = ''
        opening_split = x.split('[')
        for item in opening_split:
            closing_split = item.split(']')
            for phrase in closing_split:
                if len(phrase) > len(cleaned_up):
                    cleaned_up = phrase
        return cleaned_up

def remove_vaccinations(x: str):
    x = x.replace('Adult Vaccinations', '')
    return x.replace('Vaccination', '')


diseases_df['disease'] = diseases_df['disease'].apply(
    lambda x: remove_references(x))
diseases_df['disease'] = diseases_df['disease'].apply(
    lambda x: remove_appendations(x))



diseases_df['cleaned_disease'] = diseases_df['disease']
diseases_df['cleaned_disease'] = diseases_df['cleaned_disease'].apply(
    lambda x: remove_vaccinations(x))
diseases_df['cleaned_disease'] = diseases_df['cleaned_disease'].apply(
    lambda x: clean_parentheses(x))
diseases_df['cleaned_disease'] = diseases_df['cleaned_disease'].apply(
    lambda x: clean_square_brackets(x))
diseases_df['cleaned_disease'] = diseases_df['cleaned_disease'].apply(
    lambda x: x.lower())
diseases_df['cleaned_disease'] = diseases_df['cleaned_disease'].apply(
    lambda x: x.strip())


# %%
url = 'https://www.google.com/search?q='

def get_query_form(st):
    return url + st.replace(' ', '+')

def symptom_query_form(st):
    return get_query_form(st) + '+symptoms'


# %%
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

temp = diseases_df
temp['desc'] = None
temp['sympt'] = None

for disease in diseases_df['cleaned_disease']:
    response = requests.get(get_query_form(disease), headers=headers)
    sp = bs4.BeautifulSoup(response.text, 'html.parser')
    rhs = sp.find('div', {'class': 'liYKde'})

    response2 = requests.get(symptom_query_form(disease), headers=headers)
    sp2 = bs4.BeautifulSoup(response2.text, 'html.parser')
    rhs2 = sp2.find('div', {'class': 'liYKde'})

    if (rhs is not None) and (rhs2 is not None):
        if '/' in disease:
            disease = disease.replace('/', '-')
        try:
            rhstr = str(rhs)
            rhs2tr = str(rhs2)
            temp['desc'][temp['cleaned_disease'] == disease] = rhstr
            temp['sympt'][temp['cleaned_disease'] == disease] = rhs2tr
        except:
            continue

temp.to_csv('diseases_with_desc.csv')


