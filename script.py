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


def srt_total(directory):
    totaltext = ""
    for filename in os.listdir(directory):
        if "DVD" in filename or "3x" in filename: 
            try:
                file = pysrt.open(f'{directory}/{filename}')
                totaltext += file.text
            except UnicodeDecodeError:
                print(f'Decode error on file {filename}')         
                next
        else:
            next
    return totaltext


def main(serie, seasons):
    download_extract(serie, seasons)
    text = srt_total(f"./{serie}")
    List_tokens = tok(text)
    return List_tokens

###The function doesn't check if the zip files have already been extracted
###Until a checker is added, remember to cancel the folder

result = main("Lost", 5)

print(f'The type of the output is {type(result)}')
print(f'The number of items in the output is {len(result)}')

