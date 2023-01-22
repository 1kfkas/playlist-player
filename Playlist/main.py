import mp3_player

# Playlist

playlist_url = str(input("Insert your playlist url: "));
playlist_url = "https://www.youtube.com/playlist?list=PLTRNoDrjZ3DIXjiPZmaaq4JieLnkKAsDi";

while True:
    mp3_player.Start(playlist_url);
