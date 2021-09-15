import os
import os.path
import requests
import zipfile
import pysrt
import nltk
from nltk import word_tokenize as tok

def extract_zip(input_zip, directory):
    zip_file = zipfile.ZipFile(input_zip)
    return zip_file.extractall(directory)


def DownloadSubs(serie_name, seasons_number):
    serie = serie_name.replace(" ", "%20")
    for season in range(1, seasons_number+1):
        if os.path.isfile(f'{serie_name}-season-{season}.zip'):
            next 
        season_n = season
        url = f"http://www.tvsubtitles.net/files/seasons/{serie}%20-%20season%20{season_n}.en.zip"
        
        req = requests.get(url, allow_redirects=True)
        open(f'{serie_name}-season-{season}.zip', 'wb').write(req.content)


def download_extract(serie_name, season_n):
    DownloadSubs(serie_name, season_n)
    for season in range(1, season_n+1):
        if zipfile.is_zipfile(f'{serie_name}-season-{season}.zip'):
            extract_zip(f'{serie_name}-season-{season}.zip', f"./{serie_name}")


def clean_newlines(string_file):
    clean_file = string_file
    to_clean = ["/n", "/", ".", ",", ":", "!", "?"]
    for clean in to_clean:
        clean_file = clean_file.replace(clean, " ")
    return clean_file

def srt_total(directory):
    totaltext = ""
    for filename in os.listdir(directory):
        if "DVD" in filename or "3x" in filename: 
            try:
                file = pysrt.open(f'{directory}/{filename}')
                clean_text = clean_newlines(file.text)
                totaltext += clean_text
            except UnicodeDecodeError:
                print(f'Decode error on file {filename}')         
                next
        else:
            next
    return totaltext

def token_dict(list_tokens):
    D = {}
    for word in list_tokens:
        if word in D:
            D[word] += 1
        else:
            D[word] = 1
    return D


def main(serie, seasons):
    download_extract(serie, seasons)
    text = srt_total(f"./{serie}")
    List_tokens = tok(text)
    dict_tok = token_dict(List_tokens)
    return dict_tok

#if files already downloaded, skip downloading
def main_quick(serie):
    text = srt_total(f"./{serie}")
    List_tokens = tok(text)
    dict_tok = token_dict(List_tokens)
    return dict_tok

###The function doesn't check if the zip files have already been extracted
###Until a checker is added, remember to cancel the folder

result = main_quick("Lost")
sorted_x = sorted(result.items(), key=lambda kv: kv[1])

print(f'The type of the output is {type(sorted_x)}')
print(f'The number of items in the output is {len(sorted_x)}')
#print(sorted_x[10:10862])

