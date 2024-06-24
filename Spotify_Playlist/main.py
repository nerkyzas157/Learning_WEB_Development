from bs4 import BeautifulSoup  # type: ignore
import requests  # type: ignore
from dotenv import dotenv_values  # type: ignore
import spotipy  # type: ignore
from spotipy.oauth2 import SpotifyClientCredentials  # type: ignore

# Getting user's input for the date
date = input(
    "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
)

# Using user's input to get soup
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
html = response.text
soup = BeautifulSoup(html, "html.parser")

# Creating song list
titles = soup.find_all(name="h3", id="title-of-a-story", class_="u-line-height-125")
songs_list = []
for i in titles:
    songs_list.append(i.getText().strip())

# Getting spotify credentials
config = dotenv_values(".env")
spotify_client_id = config["SPOTIFY_CLIENT_ID"]
spotify_client_secret = config["SPOTIFY_CLIENT_SECRET"]

# Authenticating via OAuth
sp = spotipy.oauth2.SpotifyOAuth(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret,
    redirect_uri="http://example.com",
    cache_path="Spotify_Playlist\\token.json",
    scope="playlist-modify-public",
)

# Getting Access Token:
sp.get_access_token(as_dict=False)

# Pulling information for the current user
client = spotipy.client.Spotify(oauth_manager=sp)
user_id = client.current_user()["id"]

# Extracting song URIs
year = date.split("-")[0]

spotify_songs = []
for song in songs_list:
    spotify_songs.append(
        client.search(f"track: {song}, year: {year}", limit=1, offset=0, type="track")[
            "tracks"
        ]["items"][0]["uri"]
    )

# Creating a playlist
playlist = client.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard 100",
    public=True,
    collaborative=False,
    description=f"Top 100 songs that took place on {date}.",
)
playlist_id = playlist["id"]

# Adding the songs
client.user_playlist_add_tracks(
    user=user_id, playlist_id=playlist_id, tracks=spotify_songs, position=None
)

# TODO: Implement Google Forms, for users to enter their preferred dates and emails
# TODO: Implement SMTP, to notify users with their new Spotify playlists
