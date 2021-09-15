import requests
import zipfile 
import requests
from io import BytesIO

u = requests.get("http://www.pythonchallenge.com/pc/def/channel.zip")

def extract_zip(input_zip):
    input_zip = zipfile.ZipFile(input_zip)
    return {i: input_zip.read(i).decode() for i in input_zip.namelist()}


def DownloadSubs(series_name, season_number):
    serie = series_name.replace(" ", "%20")
    for season_n in range(1, season_number + 1):
        url = f"http://www.tvsubtitles.net/files/seasons/{serie}%20-%20season%20{season_n}.en.zip"
        req = requests.get(url, allow_redirects=True)
        f = BytesIO(req.content)
        files = extract_zip(f)


DownloadSubs("Lost", 4)
