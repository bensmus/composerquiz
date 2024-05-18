import random
import requests
from dotenv import load_dotenv
import os
import inquirer
import vlc

load_dotenv()
open_opus_url = 'https://api.openopus.org/'

epochs = [
    'Medieval',
    'Renaissance',
    'Baroque',
    'Classical',
    'Early Romantic',
    'Romantic',
    'Late Romantic',
    '20th Century',
    'Post-War',
    '21st Century',
]

def fetch_composers(epoch: str) -> list[dict]:
    '''Use Open Opus to fetch composers from a certain epoch
    from the list of essential composers.'''
    assert epoch in epochs, 'Invalid epoch'
    essential_composers_method = 'composer/list/rec.json'
    response = requests.get(open_opus_url + essential_composers_method)
    essential_composers: list = response.json()['composers']
    return list(filter(
        lambda composer: composer['epoch'] == epoch, 
        essential_composers))

def fetch_similar_composers(count: int) -> list[dict]:
    '''Sample count composers from similar epochs'''
    # Use enough epochs to be able to sample count composers. 
    # Sometimes more than one epoch is necessary, for example
    # there is only 1 21st Century composer that is recommended:
    # John Adams. 
    epochs_cpy = list(epochs)
    epoch_index = random.randint(0, len(epochs_cpy) - 1)
    epoch = epochs_cpy[epoch_index]
    composers = []
    while True:
        composers += fetch_composers(epoch)
        epochs_cpy.pop(epoch_index)
        if len(composers) >= count:
            return random.sample(composers, count)
        # Determine next epoch:
        if epoch_index == len(epochs_cpy):     
            epoch_index -= 1
        epoch = epochs_cpy[epoch_index]

def fetch_random_work(composer: dict) -> str:
    essential_works_method = f"work/list/composer/{composer['id']}/genre/Recommended.json"
    response = requests.get(open_opus_url + essential_works_method)
    if response.json()['status']['success'] == 'false':
        all_works_method = f"work/list/composer/{composer['id']}/genre/all.json"
        response = requests.get(open_opus_url + all_works_method)
    works: list = response.json()['works']
    return random.choice(works)

def get_spotify_token() -> str:
    spotify_token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(spotify_token_url, {
        'grant_type': 'client_credentials',
        'client_id': os.getenv('client_id'),
        'client_secret': os.getenv('client_secret'),
    })
    return response.json()['access_token']

def search_tracks(query, access_token) -> list:
    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {access_token}' 
    }
    params = {
        'q': f'{query}',
        'type': 'track'
    }
    response = requests.get(search_url, headers=headers, params=params)
    return response.json()['tracks']['items']

def find_preview_url(tracks) -> str:
    for track in tracks:
        if preview_url := track['preview_url']:
            return preview_url
    raise RuntimeError("No preview url found")

real_composer, *decoy_composers = fetch_similar_composers(4)
work = fetch_random_work(real_composer)
token = get_spotify_token()
real_composer_name = real_composer['name']
decoy_composer_names = [composer['name'] for composer in decoy_composers]
query = f"{work['title']} by {real_composer['name']}"
tracks = search_tracks(query, token)

input("Hit 'Enter' to start audio")
player = vlc.MediaPlayer(find_preview_url(tracks))
player.play()

questions = [
    inquirer.List(
        'composer',
        message='Select the composer',
        choices=random.sample([real_composer_name]+decoy_composer_names, 4) # Shuffle.
    )
]

selected_composer_name = inquirer.prompt(questions)['composer']
if selected_composer_name == real_composer_name:
    print(f"Correct! {query}")
else:
    print(f"Wrong! {query}")
