settings.init.allow_root := true
#log.file.path.set("basic-radio.log")

#Silence
src_blank =  blank()

#Playlist musics
src_musics = playlist(
  mode="random",
  reload_mode="watch",
  "musics_ipfs.m3u"
)
musics = fallback(track_sensitive=false, [src_musics, src_blank])

#Playlist wisdoms
src_wisdoms = playlist(
  mode="random",
  reload_mode="watch",
  "wisdoms_ipfs.m3u"
)

wisdoms = fallback(track_sensitive=false, [src_wisdoms, src_blank])

mix = add([delay(180., wisdoms), musics])

# Envoi au stream ou à la sortie
output.icecast(
  %mp3,
  host="163.172.162.144",
  port=8001,
  password="hackme",
  mount="/eaim",
  mix
)
