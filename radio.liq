set("log.level", 3)

# Source de secours
src_blank = blank()

# Playlist locale
src_musics = playlist("/opt/eaim/radio/musics_ipfs.m3u", reload_mode="watch", mode="random")

# Fallback en cas de problème
musics = fallback(track_sensitive=false, [src_musics, src_blank])

# Playlist des paroles de sagesse
src_wisdoms = playlist("/opt/eaim/radio/wisdoms_ipfs.m3u", reload_mode="watch", mode="random")

# Insertion aléatoire de wisdoms : lecture toutes les 60 à 180 secondes
wisdoms = delay(20., src_wisdoms)

#wisdoms_loop = loop(wisdoms_with_delay)

# Mixage audio : superposition (add) des deux sources normalisées
mixed = add([normalize(musics), normalize(wisdoms)])

# Diffusion vers Icecast
output.icecast(%mp3,
  host = "localhost",
  port = 8001,
  password = "hackme",
  mount = "eaim",
  name = "Ma webradio test",
  description = "Test depuis Liquidsoap",
  genre = "test",
  url = "http://localhost:8001",
  mixed
)