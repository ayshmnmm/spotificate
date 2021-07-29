from flask import Flask, render_template, session, redirect, request, make_response
import spotipy.util as util
import spotipy, requests, os
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from bs4 import BeautifulSoup
import string
from collections import Counter
from itertools import chain
import lyricsgenius
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

app = Flask(__name__)
app.secret_key = os.environ.get('SECKEY', 'insert random string123') # random secret key

## ------ To run locally set localrun to True and use your client id and secret ----------------
localrun = False
cid = os.environ.get('CLID', 'ss') # spotify client id
secret = os.environ.get('SECR', 'bb') # spotify client secret

## --- also ensure http://127.0.0.1:5000/callback is there in your app's redirect uris

# Redirect http to https
@app.before_request
def before_request():
    if not localrun and (not request.is_secure and app.env != "development"):
        return redirect(request.url.replace("http://", "https://", 1), code=301)
    else:
        pass

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Used to supply assets to page
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
API_BASE = 'https://accounts.spotify.com'

if localrun :
    REDIRECT_URI = "http://127.0.0.1:5000/callback" # ensure this redirect uri is added in your app dashboard
else :
    REDIRECT_URI = "https://spotificate.herokuapp.com/callback" # Must be present in the app dashboard redirect uris

SCOPE = 'user-library-read,user-read-recently-played,user-top-read'
SHOW_DIALOG = False

genius = lyricsgenius.Genius("lomao32evendthis",verbose=False)
stop_words = stopwords.words('english')
stopwords_dict = Counter(stop_words)
stopwords_dict.update({'im':1,'chorus':1,'prechorus':1,'verse':1,'ive':1,'urlcopyembedcopy':1,'youre':1})

@app.route("/callback")
def api_callback():
    session.clear()
    code = request.args.get('code')
    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":REDIRECT_URI,
        "client_id":cid,
        "client_secret":secret
        })
    res_body = res.json()
    session["toke"] = res_body.get("access_token")
    return redirect("cloud")

def cleaned_lyrics(song,artist):
    try:
        lyrics = str(genius.search_song(song,artist).lyrics).replace(u'\u200c','').strip()
    except:
        return("no lyrics")
    
    text = str(lyrics.translate(str.maketrans('', '', string.punctuation))).lower()
    text = ' '.join([word for word in text.split() if word not in stopwords_dict])

    return(text)

@app.route("/cloud")
def go():
    try :
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager,auth=session['toke'])
        results = sp.current_user_recently_played(limit=10)
        cleaned = []
        for song in results["items"]:
            cleaned.append([song['track']['name'],song['track']['artists'][0]['name']])
        temp = []
        total_text = ""
        for i in cleaned:
            total_text = total_text + cleaned_lyrics(i[0],i[1]) + " "
        counting = Counter((total_text.lower().split()))
        most_common = (counting.most_common(30))
        normalised_f = []
        for i in most_common:
            normalised_f.append(i[1])
        normalised_f = [((float(i)/max(normalised_f))*300)+10 for i in normalised_f]
        for i in range(len(most_common)):
            temp.append({"word":most_common[i][0],"freq":normalised_f[i]})
        
        return render_template("cloud.html",name=sp.current_user()['display_name'],data=temp)
    except Exception as e:
        print('-----------error : ',e)
        auth_url = f'{API_BASE}/authorize?client_id={cid}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
        return redirect(auth_url)

@app.route("/notrickroll")
def rickroll() :
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
