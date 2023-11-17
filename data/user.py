from dotenv import load_dotenv
import os
from utils.helper import abs_path_to_file

load_dotenv(abs_path_to_file('.env.spotify_credentials'))


class User:
    id: str = '31nwo7eysucx5p2fv3nksjmlrzfu'
    name: str = 'Leia Organa'
    login: str = os.getenv('LOGIN')
    password: str = os.getenv('PASSWORD')
    client_id: str = os.getenv('CLIENT_ID')
    client_secret: str = os.getenv('CLIENT_SECRET')