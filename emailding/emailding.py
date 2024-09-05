import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

# Laad de waarden uit het .env bestand
load_dotenv()

# Haal de client ID, client secret, redirect URI en email wachtwoord uit het .env bestand
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
EMAIL_WACHTWOORD = os.getenv('EMAIL_WACHTWOORD')

# Bereik waar je toegang tot wilt hebben
scope = "user-top-read"

# Authenticatie met OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))

# Haal de top artiesten op van de gebruiker
results = sp.current_user_top_artists(limit=5)

# Verzamel de namen van de top 5 artiesten in één string
top_artists = ", ".join([artist['name'] for artist in results['items']])

# Print de samengestelde string met alle top artiesten
print(f"Je top 5 artiesten zijn: {top_artists}")

def send_email():
    # E-mail account credentials
    sender_email = "florian.lenders10@gmail.com"
    receiver_email = "florian.lenders10@gmail.com"
    password = EMAIL_WACHTWOORD  # Gebruik de geladen waarde uit de .env

    # SMTP server configuratie
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Maak de e-mail aan met de top 5 artiesten
    message_content = f"Hallo,\n\nJe top 5 artiesten op Spotify zijn:\n{top_artists}\n\nGroetjes!"
    message = MIMEText(message_content)
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Je Top 5 Spotify Artiesten"

    # Verbind met de server en stuur de e-mail
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email,"uqyk svod xwqd ygln")
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("E-mail verzonden!")
    except Exception as e:
        print(f"Er is een fout opgetreden: {e}")
    finally:
        server.quit()

# Roep de functie aan om de e-mail te verzenden
send_email()
