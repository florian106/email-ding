import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
EMAIL_WACHTWOORD = os.getenv('EMAIL_WACHTWOORD')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, EMAIL_WACHTWOORD, SENDER_EMAIL, RECEIVER_EMAIL]):
    raise ValueError("Niet alle benodigde omgevingsvariabelen zijn ingesteld.")

scope = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope=scope))

def get_top_artists():
    try:
        results = sp.current_user_top_artists(limit=5)
        top_artists = "\n".join([f"{idx + 1}: {artist['name']}" for idx, artist in enumerate(results['items'])])
        return top_artists
    except Exception as e:
        print(f"Fout bij het ophalen van top artiesten: {e}")
        return None

def get_top_tracks():
    try:
        results = sp.current_user_top_tracks(limit=5)
        top_tracks = [track['id'] for track in results['items']]
        return top_tracks
    except Exception as e:
        print(f"Fout bij het ophalen van top nummers: {e}")
        return None

def recommend_songs(top_tracks):
    try:
        if not top_tracks:
            return None
        recommendations = sp.recommendations(seed_tracks=top_tracks, limit=5)
        recommended_songs = "\n".join([f"{track['name']} van {track['artists'][0]['name']}" for track in recommendations['tracks']])
        return recommended_songs
    except Exception as e:
        print(f"Fout bij het ophalen van aanbevelingen: {e}")
        return None

def send_email(top_artists, recommended_songs):
    if not top_artists:
        return
    if not recommended_songs:
        return

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    message_content = (f"Hallo,\n\nJe top 5 artiesten op Spotify zijn:\n{top_artists}\n\n"
                       f"Aanbevolen nummers op basis van je top tracks:\n{recommended_songs}\n\nGroetjes!")
    
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = RECEIVER_EMAIL
    message['Subject'] = "Je Spotify Top 5 Artiesten en Aanbevolen Nummers"
    message.attach(MIMEText(message_content, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_WACHTWOORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        print("E-mail verzonden!")
    except Exception as e:
        print(f"Er is een fout opgetreden bij het verzenden van de e-mail: {e}")
    finally:
        server.quit()

top_artists = get_top_artists()
top_tracks = get_top_tracks()
recommended_songs = recommend_songs(top_tracks)
send_email(top_artists, recommended_songs)
