import os
import os.path
import requests


def DownloadSubs(serie_name, seasons_number):
    serie = serie_name.replace(" ", "%20")
    for season in range(1, seasons_number+1):
        if os.path.isfile(f'{serie_name}-season-{season}.zip'): 
        season_n = season
        url = f"http://www.tvsubtitles.net/files/seasons/{serie}%20-%20season%20{season_n}.en.zip"
        
        req = requests.get(url, allow_redirects=True)
        open(f'{serie_name}-season-{season}.zip', 'wb').write(req.content)


DownloadSubs("Lost", 4)