# bpm-searcher
This repository has the code used for [bpm-searcher](https://bpm-searcher.herokuapp.com/).  
[bpm-searcher](https://bpm-searcher.herokuapp.com/) can search bpm of a given song by querying Spotify API.  

# Spotify chart API
This repository also offers simple Spotify chart API which shows the charts in https://spotifycharts.com/regional.
You can get this chart information in JSON as the following example.
The first element of the array represents the top of the ranking.
```
GET https://bpm-searcher.herokuapp.com/api/ranking
```

```json
[
  {
    "album_name": "F*CK LOVE 3: OVER YOU",
    "artist": "The Kid LAROI",
    "bpm": 169.928,
    "danceability": 0.591,
    "energy": 0.764,
    "image_url": "https://i.scdn.co/image/ab67616d0000b2738e6551a2944764bc8e33a960",
    "key": 1,
    "mode": 1,
    "preview_url": "https://p.scdn.co/mp3-preview/dd4d8d66b97b6edcb5358135e72620715e1449f9?cid=12f045556f09486ba2ca641e0f062fa0",
    "song_name": "STAY (with Justin Bieber)",
    "spotify_id": "5PjdY0CKGZdEuoNab3yDmX"
  },
  {
    "album_name": "MONTERO",
    "artist": "Lil Nas X",
    "bpm": 150.087,
    "danceability": 0.741,
    "energy": 0.691,
    "image_url": "https://i.scdn.co/image/ab67616d0000b273be82673b5f79d9658ec0a9fd",
    "key": 10,
    "mode": 0,
    "preview_url": "https://p.scdn.co/mp3-preview/c1cb40d748692992bd5e476fc17ffe16f31016e3?cid=12f045556f09486ba2ca641e0f062fa0",
    "song_name": "INDUSTRY BABY (feat. Jack Harlow)",
    "spotify_id": "5Z9KJZvQzH6PFmb8SNkxuk"
  },
  ...
]
```