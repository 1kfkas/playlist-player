import sys, os, os.path, requests, pygame, random
from os import path
from PIL import Image
from pytube import YouTube
from pytube import Playlist
from pydub import AudioSegment
from pygame.locals import *

###############

pause = False;
w = 0;
h = 0;

random_range = random.randrange;

img_dir = './Images/';
audio_dir = './Audio/';

if sys.platform.startswith('win32'):
    img_dir = '.\Images\\';
    audio_dir = '.\Audio\\';

img_dir_exists = os.path.isdir(img_dir);
audio_dir_exists = os.path.isdir(audio_dir);

if not img_dir_exists:
    paD = requests.get('https://raw.githubusercontent.com/JaoKFkas/framework/main/Framework/MP3/Images/pause.png');
    plD = requests.get('https://raw.githubusercontent.com/JaoKFkas/framework/main/Framework/MP3/Images/play.png');
    os.mkdir(img_dir);
    paDFile = open(img_dir+"pause.png", "wb");
    plDFile = open(img_dir+"play.png", "wb");
    paDFile.write(paD.content);
    plDFile.write(plD.content);
    paDFile.close();
    plDFile.close();

if not audio_dir_exists:
    os.mkdir(audio_dir);

###############

def Download_Thumbnail(video):
    print('\nBaixando Thumbnail...');
    response = requests.get(video.thumbnail_url);
    file = open(img_dir+"image.png", "wb");
    file.write(response.content);
    file.close();
    print('Thumbnail Baixada!\n');

def Download_Music(videoURL):
    print('Baixando Música...');
    yt = YouTube(videoURL);
    stream = yt.streams.filter(only_audio=True, file_extension='webm').first();
    print(stream);
    stream.download(audio_dir, 'audio.webm');
    print('Música Baixada!\n\nConvertendo Música...');
    webm_audio = AudioSegment.from_file(audio_dir+'audio.webm', format="webm");
    webm_audio.export(audio_dir+'audio.ogg', format="ogg");
    os.remove(audio_dir+'audio.webm');
    print('Música Convertida!');

###########################
    
def Set_Pause(bol):
    pause = bol;

def Get_Pause():
    return pause;

def PauseMusic():
    pygame.mixer.music.pause();
    
def ResumeMusic():
    pygame.mixer.music.unpause();
    
def StopMusic():
    pygame.mixer.music.stop();

def Load(display, spr, pl, pa):
    display.blit(spr, (64, 0));

    if Get_Pause():
        display.blit(pl, (64+w/2-24, h+16));
    else:
        display.blit(pa, (64+w/2-24, h+16));

###############################

def stopRunning():
    pygame.mixer.quit();
    pygame.display.quit();
    pygame.quit();
    #os.remove(img_dir+"image.png");
    #os.remove(audio_dir+"audio.ogg");
    #sys.exit();

#################

def Start(URL):
    searchType = URL;

    p = Playlist(searchType);
    i = random_range(p.length);
    video = p.videos[i];
    videoURL = p.video_urls[i];

    duration = video.length;

    print(video.title);
    print(videoURL);
    print(duration);

    Download_Thumbnail(video);
    Download_Music(videoURL);

    pygame.init();
    pygame.display.init();
    pygame.mixer.init();

    clock = pygame.time.Clock();
    pygame.display.set_caption(video.title);

    img = Image.open(img_dir+"image.png");

    w = img.width;
    h = img.height;

    display = pygame.display.set_mode((w+128, h+64));

    sound = pygame.mixer.music.load(audio_dir+"audio.ogg");
    pygame.mixer.music.play();
    pygame.display.set_caption(video.title);

    imageFile = open(img_dir+'image.png');
    playFile = open(img_dir+'play.png');
    pauseFile = open(img_dir+'pause.png');

    spr = pygame.image.load(imageFile).convert();
    pl = pygame.image.load(playFile).convert_alpha();
    pa = pygame.image.load(pauseFile).convert_alpha();

    print('\nPronto para iniciar!\n');

    running = True;

    while running:
    
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT or pygame.mixer.music.get_pos() == -1:
                running = False;
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False;
            
                if event.key == pygame.K_SPACE:
                    global pause
                    if Get_Pause():
                        print("a")
                        pause = False;
                        ResumeMusic();
                    else:
                        print("b")
                        pause = True;
                        PauseMusic();
            
        clock.tick(60);

        display.fill((102, 102, 102));

        Load(display, spr, pl, pa);

        pygame.display.flip();

    imageFile.close();
    playFile.close();
    pauseFile.close();

    stopRunning();
