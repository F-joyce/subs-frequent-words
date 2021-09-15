import os
import os.path
import requests
import zipfile
import pysrt
import nltk
from nltk import word_tokenize as tok
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from collections import defaultdict
from pprint import pprint

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
        
        print(url)
        req = requests.get(url, allow_redirects=True)
        print('done')
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
    D = defaultdict(int)
    for word in list_tokens:
        if is_english(word):
            D[word] += 1
    return D

def sort_dic(dictionary):
    #copiata da SO, non capisco come funzioni
    sorted_d = sorted(dictionary.items(), key=lambda kv: kv[1])
    # rev_sorted = sorted_d[::-1]
    return sorted_d


def main(serie, seasons):
    download_extract(serie, seasons)
    text = srt_total(f"./{serie}")
    List_tokens = tok(text)
    dict_tok = token_dict(List_tokens)
    sorted_list = sort_dic(dict_tok)
    
    return sorted_list

def is_english(w):
    if wordnet.synsets(w):
        return True
    return False



# [ (instance, True) ]
def lemmatize(w, lemmatizers):
    r = w
    for lemmatizer, check_dict in lemmatizers:
        temp = lemmatizer(w)
        if check_dict:
            if is_english(temp):
                r = temp
        else:
            r = temp
    return r





#if files already downloaded, skip a passage
def main_quick(serie):
    text = srt_total(f"./{serie}")
    List_tokens = tok(text)

    stemmers = [ (WordNetLemmatizer().lemmatize, False), (PorterStemmer().stem, True) ]
    stemmed_tokens = [lemmatize(w, stemmers) for w in List_tokens]
    english_stopwords = stopwords.words('english')
    interesting_words = [w for w in stemmed_tokens if w not in english_stopwords]

    dict_tok = token_dict(interesting_words)
    print(type(dict_tok))
    sorted_list = sort_dic(dict_tok)
    print(type(sorted_list))
    
    return sorted_list

###The function doesn't check if the zip files have already been extracted
###Until a checker is added, remember to cancel the folder

if __name__ == '__main__':
    result = main_quick("Lost")

    print(f'The type of the output is {type(result)}')
    print(f'The number of items in the output is {len(result)}')
    pprint(result)

# Choose between season/episode(s)


