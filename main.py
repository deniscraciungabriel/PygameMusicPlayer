import pygame
from pygame import mixer
import os
import random

pygame.init()

pygame.display.set_caption("Illegal Spotify")

# values
WIDTH = 800
HEIGHT = 600
running = True
playing = False
path = "C:\\Users\\Den\\Desktop\\programmazioni\\Python\\proggetti\\music player\\songs"
font = pygame.font.SysFont("comicsans", 50)
TextHeight = font.size("Hi")
lastposition = 0
songplaying = 0
Circle_x = 680
Circle_y = 550

# images
next = pygame.image.load("next.png")
LilPlay = pygame.transform.scale(pygame.image.load("play.png"), (TextHeight[1] - 5, TextHeight[1] - 5))
LilPause = pygame.transform.scale(pygame.image.load("pause.png"), (TextHeight[1] - 5, TextHeight[1] - 5))
play = pygame.transform.scale(LilPlay, (64, 64))
pause = pygame.image.load("pause1.png")
next2 = pygame.transform.rotate(next, 180)
bigplay = pygame.transform.scale(play, (68, 68))
bigpause = pygame.transform.scale(pause, (68, 68))
bignext = pygame.transform.scale(next, (68, 68))
bignext2 = pygame.transform.scale(next2, (68, 68))
bigLilplay = pygame.transform.scale(LilPlay, (TextHeight[1] - 3, TextHeight[1] - 3))
bigLilpause = pygame.transform.scale(LilPause, (TextHeight[1] - 3, TextHeight[1] - 3))
icon = pygame.image.load("icona.png")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(icon)


def Load_music():
    songs = []
    for filename in os.listdir(path):
        songs.append(os.path.join(path, filename))
    return songs


songs = Load_music()


def DrawButtons(pos):
    if not playing:
        screen.blit(play, (368, 518))
    else:
        screen.blit(pause, (368, 518))
    screen.blit(next, (440, 518))
    screen.blit(next2, (285, 518))
    x = 700
    y = 9.5
    for i in songs:
        if not playing:
            if LilPlay.get_rect(topleft=(x, y)).collidepoint(pos):
                screen.blit(bigLilplay, (x, y))
            screen.blit(LilPlay, (x, y))

        else:
            screen.blit(LilPlay, (x, y))
            pygame.draw.rect(screen, (150, 150, 150),
                             (700, 32.5 * int((lastposition - 8.25) // 32.5) + 8.25, 32.5, 32.5))
            screen.blit(LilPause, (700, 32.5 * int((lastposition - 8.25) // 32.5) + 8.25))
        if LilPlay.get_rect(topleft=(x, 32.5 * int((lastposition - 8.25) // 32.5) + 8.25)).collidepoint(pos):
            screen.blit(bigLilpause, (x, 32.5 * int((lastposition - 8.25) // 32.5) + 8.25))
        if LilPlay.get_rect(topleft=(x, y)).collidepoint(pos):
            if y < 32.5 * int((lastposition - 8.25) // 32.5) + 8.25 - 1 or y > 32.5 * int(
                    (lastposition - 8.25) // 32.5) + 8.25 + 3:
                screen.blit(bigLilplay, (x, y))
        y += TextHeight[1] - 2.5


def ShowSongs():
    x = 7
    y = 7
    for song in songs:
        text = font.render(str(song)[72:-4], True, (0, 0, 0), None)
        screen.blit(text, (x, y))
        y += 33


def ZoomButtons(pos, event):
    global play
    global next
    global pause
    global next2
    global LilPlay
    x = 700
    y = 9.5

    if event.type == pygame.MOUSEMOTION:
        if play.get_rect(topleft=(368, 518)).collidepoint(pos):
            play = bigplay
        else:
            play = pygame.transform.scale(play, (64, 64))
        if playing:
            if pause.get_rect(topleft=(368, 518)).collidepoint(pos):
                pause = bigpause
            else:
                pause = pygame.transform.scale(pause, (64, 64))
        if next.get_rect(topleft=(440, 518)).collidepoint(pos):
            next = bignext
        else:
            next = pygame.transform.scale(next, (64, 64))
        if next2.get_rect(topleft=(285, 518)).collidepoint(pos):
            next2 = bignext2
        else:
            next2 = pygame.transform.scale(next2, (64, 64))


def PressLilplay(pos, event):
    global playing
    global lastposition
    global songplaying
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pos[0] >= 700 and pos[0] <= 730 and pos[1] > 8.25 and pos[1] < 500:
            mixer.music.load(songs[int((pos[1] - 8.25) // 32.5)])
            songplaying = int((pos[1] - 8.25) // 32.5)
            mixer.music.play(0, 0.0)
            playing = True
            lastposition = pos[1]


def PressPause(event):
    global playing
    if playing:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause.get_rect(topleft=(368, 518)).collidepoint(pos):
                mixer.music.pause()
                playing = False
    else:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause.get_rect(topleft=(368, 518)).collidepoint(pos):
                mixer.music.unpause()
                playing = True


def PressSkip(event):
    global songplaying
    if playing:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if next.get_rect(topleft=(440, 518)).collidepoint(pos):
                songplaying += 1
                mixer.music.load(songs[songplaying])
                mixer.music.play(0, 0.0)


class Volume():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def Draw(self):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 10, 0)
        pygame.draw.line(screen, (0, 0, 0), (620, 550), (720, 550), 3)

    def SetVolume(self, event, pos):
        global Circle_x
        events = pygame.mouse.get_pressed()
        if events == (1, 0, 0):
            if pos[0] >= 620 and pos[0] <= 720 and pos[1] >= 497 and pos[1] <= 553:
                Circle_x = int(pos[0])
        mixer.music.set_volume((Circle_x-620)/100)



while running:
    volume = Volume(Circle_x, Circle_y)
    screen.fill((0, 0, 0))
    pos = pygame.mouse.get_pos()
    pygame.draw.rect(screen, (150, 150, 150), (0, 500, 800, 100))
    pygame.draw.rect(screen, (150, 150, 150), (5, 5, 790, 490))
    DrawButtons(pos)
    ShowSongs()
    volume.Draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ZoomButtons(pos, event)
        PressLilplay(pos, event)
        PressPause(event)
        PressSkip(event)
        volume.SetVolume(event, pos)
    pygame.display.update()
