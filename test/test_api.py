import requests

base_url='http://127.0.0.1:5000'

def post_actor(actor: str):
    r = requests.post(base_url + '/actor', json={
        "actor": actor
    })

    return r.json()['status']

def test_post_actor():
    assert post_actor('скриптонит') is False

def get_actor(actor: str):
    r = requests.get(base_url + '/actor/' + actor)
    return r.json()['actor']

def test_get_actor():
    assert get_actor('ABBA') == 'ABBA'

def post_song(actor: str, song: str):
    r = requests.post(base_url + '/actor', json={
        "actor": actor
    })

    r = requests.post(base_url + '/song', json={
        "actor_name": actor,
        "songname": song
    })

    return r.json()['status']

def test_post_song():
    assert post_song(actor='баста', song='моя игра') is False

def get_song(song:str):
    r = requests.get(base_url + '/song/' + str(song))
    return r.json()['name']

def test_get_song():
    assert get_song('hahaha') == 'hahaha'

