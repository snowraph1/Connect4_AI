import os
import pygame
import math
from pygame.locals import *
from enum import Enum

pygame.init()
pygame.font.init()

X = 800
Y = 800

display_surface = pygame.display.set_mode((X, Y ))

noir = (0, 0, 0)
blanc = (255, 255, 255)

jeu_path = os.path.dirname(__file__)

images_path = os.path.join(jeu_path, "Resources\Images")

jetonJaune = pygame.image.load(os.path.join(images_path, "Jaune.png"))
jetonJaune = pygame.transform.scale(jetonJaune, (100, 100))

jetonRouge = pygame.image.load(os.path.join(images_path, "Rouge.png"))
jetonRouge = pygame.transform.scale(jetonRouge, (100, 100))

fond = pygame.image.load(os.path.join(images_path, "Fond.png"))
fond = pygame.transform.scale(fond, (800, 800))

cercles = pygame.image.load(os.path.join(images_path, "Cercles.png"))
cercles = pygame.transform.scale(cercles, (800, 800))

class Couleur(Enum):
    JAUNE = 1
    ROUGE = 2

class Jeton :
    def __init__(self, image, position, couleur):
        self.image = image
        self.position = position
        self.couleur = couleur

    def info(self):
        print("Couleur : " + self.couleur.name + ", Position : (" + str(self.getPosition()[0]) + ", " + str(self.getPosition()[1]) + ")")
        
    def getImage(self): 
        return self.image
    
    def setPosition(self, pos):
        self.position[0] = pos[0] - self.image.get_width() / 2
        self.position[1] = pos[1] - self.image.get_height() / 2
        
    def getVraiPosition(self):
        return self.position
    
    def getPosition(self):
        return [self.position[0] + self.image.get_width() / 2, self.position[1] + self.image.get_height() / 2]


jeu = [[Jeton(None, [0, 0], None) for i in range(6)] for j in range(7)]

compteurMove = 0

# Range 1 : 133     Range 2 : 242          Entre les rangées : 108

# Colonne 1 : 76    Colonne 2 : 184        Entre les colonnes : 108

def GetColoneSelected ():
    x,y = pygame.mouse.get_pos()
    
    col = math.floor(float(x + 85) / 108)
    
    if col < 0 or col > 7 :
        return 0
    
    return col

def PlacerJeton (col, couleur):
    jeton = None
    
    if couleur == Couleur.JAUNE:
        jeton = jetonJaune
    else:
        jeton = jetonRouge
    
    range = VerifierColonne(col)
    
    if range > -1:
        jeu[col - 1][range] = Jeton(jeton, [(col - 1) * 108 + 26, range * 108 + 83], couleur)
        #print("Jeton placé")
        TestGagnant(col - 1, range, couleur)
        return True
    return False
    
def VerifierColonne(col):
    for x in range(5, -1, -1):
        if jeu[col - 1][x].getImage() == None:
            return x
    return -1

def PrintJeu():
    print("")
    for y in range(6):
        ligne = ""
        for x in range(7):
            if (jeu[x][y].getImage() != None):
                ligne += str(jeu[x][y].couleur.value) + " "
            else:
                ligne += "0 "
        print(ligne)
    print("")

def RedemarrerJeu():
    for y in range(6):
        for x in range(7):
            jeu[x][y] = Jeton(None, None, None)
    compteurMove = 0
    print("Nouvelle partie")

def Button(gauche, dessus, largeur, hauteur, texte, police):
    smallfont = pygame.font.SysFont('Corbel', police)
    text = smallfont.render(texte , True , blanc)
    pygame.draw.rect(display_surface, (102, 102, 102), pygame.Rect(gauche,dessus, text.get_width(), text.get_height()))
    display_surface.blit(text , (0,0))

def TestGagnant(x, y, couleur):
    if TestVertical(x, couleur) or TestHorizontal(y, couleur) or TestDiagonal(x, y, couleur):
        print("")
        print("WIN")
        print("")
    
def TestVertical(x, couleur):
    compteur = 0
    for y in range(5, -1, -1):
        if jeu[x][y].getImage() != None:
            if jeu[x][y].couleur == couleur:
                compteur += 1
                
    if compteur >= 4:
        return True
    else:
        return False
    
def TestHorizontal(y, couleur):
    compteur = 0
    for x in range(6, -1, -1):
        if jeu[x][y].getImage() != None:
            if jeu[x][y].couleur == couleur:
                compteur += 1
            else:
                compteurMove = 0
                
    if compteur >= 4:
        return True
    else:
        return False
    
def TestHorizontal(y, couleur):
    compteur = 0
    for x in range(6, -1, -1):
        if jeu[x][y].getImage() != None:
            if jeu[x][y].couleur == couleur:
                compteur += 1
            else:
                compteur = 0
                
    if compteur >= 4:
        return True
    else:
        return False
    
def TestDiagonal(x, y, couleur):
    compteur = 0
    for i in range(3):
        print(str(i - x) + " " + str(i - y))
        if jeu[x - i][y - i].getImage() != None:
            print(jeu[x - i][y - i].couleur)
            if jeu[x - i][y - i].couleur == couleur:
                PlacerJeton(x, Couleur.JAUNE)
                
    if compteur >= 4:
        return True
    else:
        return False

while True :
    display_surface.fill(noir)

    Button(0, 0, 180, 180, "Recommencer", 30)
    
    for y in range(6):
        for x in range(7):
            if jeu[x][y].getImage() != None:
                display_surface.blit(jeu[x][y].getImage(), (jeu[x][y].position[0], jeu[x][y].position[1]))

    display_surface.blit(fond, (0, 0))
    display_surface.blit(cercles, (0, 0))

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()           
            quit()
        
        if event.type == pygame.MOUSEBUTTONDOWN :
            x,y = pygame.mouse.get_pos()
            
            if (y > 50) :       
                if compteurMove % 2 == 0:
                    if PlacerJeton(GetColoneSelected(), Couleur.JAUNE):
                        compteurMove += 1
                else:
                    if PlacerJeton(GetColoneSelected(), Couleur.ROUGE):
                        compteurMove += 1
                        
                PrintJeu()
            else:
                RedemarrerJeu()
        
        pygame.display.update()
