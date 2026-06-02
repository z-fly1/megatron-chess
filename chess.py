import pygame as p
from engine import GameState

WIDTH = HEIGHT = 512
DIMENTION = 8
SQ_SIZE = WIDTH / DIMENTION

MAX_FPS = 15

IMAGES = []

p.init()


def loadImages():
    peices = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bB", "bN", "bK", "bQ"]

    for peice in peices:
        IMAGES[peice] = p.transform.scale(p.image.load("imgs/"+ peice + ".png"), (SQ_SIZE, SQ_SIZE))