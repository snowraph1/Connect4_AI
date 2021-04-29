import os
import pygame
import math
from pygame.locals import *
from enum import Enum
import random
import copy

#https://medium.com/analytics-vidhya/artificial-intelligence-at-play-connect-four-minimax-algorithm-explained-3b5fc32e4a4f

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

gameOver = False

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

def PlacerJeton (col, couleur, tableau):
    jeton = None
    
    if couleur == Couleur.JAUNE:
        jeton = jetonJaune
    else:
        jeton = jetonRouge
    
    rangee = VerifierColonne(col, tableau)
    
    if rangee > -1:
        tableau[col - 1][rangee] = Jeton(jeton, [(col - 1) * 108 + 26, rangee * 108 + 83], couleur)
        #print("Jeton placé")
        TestGagnant(col - 1, rangee, couleur, tableau)
        return True
    return False
    
def VerifierColonne(col, tableau):
    for x in range(5, -1, -1):
        if tableau[col - 1][x].getImage() == None:
            return x
    return -1

def PrintJeu(tableau):
    print("")
    for y in range(6):
        ligne = ""
        for x in range(7):
            if (tableau[x][y].getImage() != None):
                ligne += str(tableau[x][y].couleur.value) + " "           
            else:
                ligne += "0 "
        print(ligne)
    print("")

def RedemarrerJeu():
    for y in range(6):
        for x in range(7):
            jeu[x][y] = Jeton(None, None, None)
    compteurMove = 0
    gameOver = False
    print("Nouvelle partie")

def Button(gauche, dessus, largeur, hauteur, texte, police):
    smallfont = pygame.font.SysFont('Corbel', police)
    text = smallfont.render(texte , True , blanc)
    pygame.draw.rect(display_surface, (102, 102, 102), pygame.Rect(gauche,dessus, text.get_width(), text.get_height()))
    display_surface.blit(text , (0,0))

def TestGagnant(x, y, couleur, tableau):
    if TestVertical(x, couleur, tableau) or TestHorizontal(y, couleur, tableau) or TestDiagonal(x, y, couleur, tableau):
        if (tableau == jeu):
            print("")
            gameOver = True
            print("WIN " + str(couleur))
        return True
    
def TestVertical(x, couleur, tableau):
    compteur = 0
    for y in range(5, -1, -1):
        if tableau[x][y].getImage() != None:
            if tableau[x][y].couleur == couleur:
                compteur += 1
                if compteur >= 4:
                    return True
            else:
                compteur = 0
        else:
            compteur = 0

    return False
    
def TestHorizontal(y, couleur, tableau):
    compteur = 0
    for x in range(6, -1, -1):
        if tableau[x][y].getImage() != None:
            if tableau[x][y].couleur == couleur:
                compteur += 1            
                if compteur >= 4:
                    return True
            else:
                compteur = 0
        else:
            compteur = 0

    return False
    
def TestDiagonal(x, y, couleur, tableau):
    test = [[None for i in range(6)] for j in range(7)]
    
    compteur = 0
    
    for i in range(8):
        xPos = x + (i - 4)
        yPos = y + (i - 4)
        if (xPos >= 0 and xPos < 7 and yPos >= 0 and yPos < 6):
            test[xPos][yPos] = 1
            if (tableau[xPos][yPos].getImage() != None):
                #print("yo " + str(tableau[xPos][yPos].couleur))
                if (tableau[xPos][yPos].couleur == couleur):
                    compteur += 1
                else:
                    compteur = 0
            else:
                compteur = 0
                
        if (compteur >= 4):
            return True

    compteur = 0
    
    for i in range(8):
        xPos = x - (i - 4)
        yPos = y + (i - 4)
        if (xPos >= 0 and xPos < 7 and yPos >= 0 and yPos < 6):
            test[xPos][yPos] = 2
            if (tableau[xPos][yPos].getImage() != None):
                if (tableau[xPos][yPos].couleur == couleur):
                    compteur += 1
                    if (compteur >= 4):
                        return True
                else:
                    compteur = 0
            else:
                compteur = 0
                
        if (compteur >= 4):
            return True
    """                
    print("Test ") 
    for y in range(6):
        ligne = ""
        for x in range(7):
            if (test[x][y] != None):
                ligne += str(test[x][y]) + " "           
            else:
                ligne += "0 "
        print(ligne)
    print("")
    """
        
    return False

def ColonneRandom ():
    return random.randrange(7) + 1

def premierNiveau(profondeur, joueur):
    tableau = [[Jeton(None, [0, 0], None) for i in range(6)] for j in range(7)]
    
    for y in range(6):
        for x in range(7):
            if (jeu[x][y].getImage() != None):
                tableau[x][y] = jeu[x][y]
                  
    for x in range(profondeur):
        oldX = None
        oldY = None
        
        for i in range(8):
            rangee = VerifierColonne(i, tableau)       
            if rangee > -1:
                if oldX != None and oldY != None:
                    tableau[oldX][oldY] = Jeton(None, [0, 0], None)
                    
                PlacerJeton(i, Couleur.ROUGE, tableau)
                oldX = i - 1
                oldY = rangee
                 
                if TestGagnant(i - 1, rangee, Couleur.ROUGE, tableau):
                    if i == 0:
                        i = 7
                    return i
                         
                if oldX != None and oldY != None:
                    tableau[oldX][oldY] = Jeton(None, [0, 0], None)
                    
                PlacerJeton(i, Couleur.JAUNE, tableau)
                oldX = i - 1
                oldY = rangee
                 
                if TestGagnant(i - 1, rangee, Couleur.JAUNE, tableau):
                    if i == 0:
                        i = 7
                    return i
        #PrintJeu(tableau)
    return ColonneRandom()

def deuxiemeNiveau(profondeur, couleur):
    
    tableau = [[Jeton(None, [0, 0], None) for i in range(6)] for j in range(7)]
    
    for y in range(6):
        for x in range(7):
            if (jeu[x][y].getImage() != None):
                tableau[x][y] = jeu[x][y]
                
    tabScore = [0, 0, 0, 0, 0, 0, 0]
                
    MiniMax(tableau, 6, couleur, tabScore)
    
    print("fini " + str(tabScore) + " " + str(max(range(len(tabScore)), key=tabScore.__getitem__)))

    return max(range(len(tabScore)), key=tabScore.__getitem__) + 1

def MiniMax(tableau, profondeur, couleur, tabScore) :
    if profondeur == 0:
        return
    
    oldX = None
    oldY = None
        
    for i in range(7):
        if oldX != None and oldY != None:
            tableau[oldX][oldY] = Jeton(None, [0, 0], None)
        rangee = VerifierColonne(i + 1, tableau)       
        if rangee > -1:          
            tempCouleur = None
            tempJeton = None
            
            if couleur == Couleur.JAUNE:                                          
                tempCouleur = couleur.ROUGE
                tempJeton = jetonRouge
            else:
                tempCouleur = couleur.JAUNE
                tempJeton = jetonJaune
                
            oldX = i
            oldY = rangee
            
            tableau[oldX][oldY] = Jeton(tempJeton, [0, 0], tempCouleur)
            
            if couleur == Couleur.JAUNE:                                          
                if TestGagnant(oldX, rangee, Couleur.ROUGE, tableau):
                    tabScore[i] += 10 * profondeur
            else:
                if TestGagnant(oldX, rangee, Couleur.JAUNE, tableau):
                    tabScore[i] += 5 * profondeur
                                 
            MiniMax(tableau, profondeur - 1, tempCouleur, tabScore)
            
    if oldX != None and oldY != None:
        tableau[oldX][oldY] = Jeton(None, [0, 0], None)
    
def troisiemeNiveau(profondeur, couleur):
    tableau = [[Jeton(None, [0, 0], None) for i in range(6)] for j in range(7)]
    
    for y in range(6):
        for x in range(7):
            if (jeu[x][y].getImage() != None):
                tableau[x][y] = jeu[x][y]
                  
    for x in range(profondeur):
        oldX = None
        oldY = None
        
        for i in range(8):
            rangee = VerifierColonne(i, tableau)       
            if rangee > -1:
                if oldX != None and oldY != None:
                    tableau[oldX][oldY] = Jeton(None, [0, 0], None)
                    
                PlacerJeton(i, Couleur.ROUGE, tableau)
                oldX = i - 1
                oldY = rangee
                 
                if TestGagnant(i - 1, rangee, Couleur.ROUGE, tableau):
                    if i == 0:
                        i = 7
                    return i
                         
                if oldX != None and oldY != None:
                    tableau[oldX][oldY] = Jeton(None, [0, 0], None)
                    
                PlacerJeton(i, Couleur.JAUNE, tableau)
                oldX = i - 1
                oldY = rangee
                 
                if TestGagnant(i - 1, rangee, Couleur.JAUNE, tableau):
                    if i == 0:
                        i = 7
                    return i
        #PrintJeu(tableau)
    return deuxiemeNiveau(profondeur, couleur)
"""
def MoveGagnant(tableau, couleur):
    nouveauTableau = [[Jeton(None, [0, 0], None) for i in range(6)] for j in range(7)]
    
    for y in range(6):
        for x in range(7):
            if (tableau[x][y].cou != None):
                nouveauTableau[x][y] = tableau[x][y]
                
    for i in range(8):
        rangee = VerifierColonne(i, tableau)
        PlacerJeton(i, couleur, tableau)
        if (TestGagnant)
"""

def verifierMoveGagnant(couleur, tableau):
    oldX = None
    oldY = None
        
    for i in range(7):
        if oldX != None and oldY != None:
            tableau[oldX][oldY] = Jeton(None, [0, 0], None)
        rangee = VerifierColonne(i + 1, tableau)       
        if rangee > -1:          
            tempCouleur = None
            tempJeton = None
            
            if couleur == Couleur.JAUNE:                                          
                tempCouleur = couleur.ROUGE
                tempJeton = jetonRouge
            else:
                tempCouleur = couleur.JAUNE
                tempJeton = jetonJaune
                
            oldX = i
            oldY = rangee
            
            tableau[oldX][oldY] = Jeton(tempJeton, [0, 0], tempCouleur)
                                                    
            if TestGagnant(oldX, rangee, couleur, tableau):
                return True  
            
    if oldX != None and oldY != None:
        tableau[oldX][oldY] = Jeton(None, [0, 0], None)
        
    return False

def donnerScore (compteur, compteurEnnemi, compteurVide):
    score = 0
    
    if (compteur == 4):
        score += 100     
    
    if (compteur == 3):
        score += 5
        
    if (compteur == 2):
        score += 2
            
    if (compteurEnnemi):
        score -= 4
        
    return score


def ScoreTableau(tableau, couleur):
    score = 0
    
    compteur = 0
    compteurEnnemi = 0
    compteurVide = 0
    
    ennemi = None
    
    if couleur == Couleur.JAUNE:
        ennemi = Couleur.ROUGE
    else:
        ennemi = Couleur.JAUNE
    
    for x in range(7):
        compteur = 0
        compteurEnnemi = 0
        compteurVide = 0
        
        for y in range(6):
            if tableau[x][y].couleur == couleur:
                compteur += 1
            elif tableau[x][y].couleur == ennemi:
                compteurEnnemi += 1
            else:
                compteurVide += 1
                
        score += donnerScore(compteur, compteurEnnemi, compteurVide)
    
    for x in range(7):
        compteur = 0
        compteurEnnemi = 0
        compteurVide = 0
        
        for y in range(6):
            if tableau[x][y].couleur == couleur:
                compteur += 1
            elif tableau[x][y].couleur == ennemi:
                compteurEnnemi += 1
            else:
                compteurVide += 1
                
        score += donnerScore(compteur, compteurEnnemi, compteurVide)
            
    for y in range(6):
        for x in range(7):
            compteurEnnemi = 0
            compteur = 0
            compteurVide = 0
            
            for i in range(8):
                xPos = x + (i - 4)
                yPos = y + (i - 4)
                if (xPos >= 0 and xPos < 7 and yPos >= 0 and yPos < 6):
                    if tableau[xPos][yPos].couleur == couleur:
                        compteur += 1
                    elif tableau[xPos][yPos].couleur == ennemi:
                        compteurEnnemi += 1
                    else:
                        compteurVide += 1

            score += donnerScore(compteur, compteurEnnemi, compteurVide)
             
    for y in range(6):
        for x in range(7):
            compteurEnnemi = 0
            compteur = 0
            compteurVide = 0
            
            for i in range(8):
                xPos = x - (i - 4)
                yPos = y + (i - 4)
                if (xPos >= 0 and xPos < 7 and yPos >= 0 and yPos < 6):
                    if tableau[xPos][yPos].couleur == couleur:
                        compteur += 1
                    elif tableau[xPos][yPos].couleur == ennemi:
                        compteurEnnemi += 1
                    else:
                        compteurVide += 1
                        
            score += donnerScore(compteur, compteurEnnemi, compteurVide)
    
    return score

def EstDernierMove(tableau):
    if TestGagnantFinal(tableau) != None:
        return True
    else:
        return False
    
def TestGagnantFinal(tableau):
    for y in range(6):
        for x in range(7):
            if (tableau[x][y].couleur != None):
                if TestGagnant(x, y, Couleur.ROUGE, tableau):
                    return Couleur.ROUGE
                
                if TestGagnant(x, y, Couleur.JAUNE, tableau):
                    return Couleur.JAUNE
    return None 

    
def BonMiniMax(tableau, profondeur, maximize, alpha, beta) :
    if EstDernierMove(tableau) or profondeur == 0:
        if EstDernierMove(tableau):
            if TestGagnantFinal(tableau) == Couleur.ROUGE:
                return None, 1000000
            if TestGagnantFinal(tableau) == Couleur.JAUNE:
                return None, -1000000
            else:
                return None, 0 
        else:
            return None, ScoreTableau(tableau, Couleur.ROUGE)
    
    if maximize:        
        bestScore = -math.inf
        colonne = 0
            
        for i in range(7):
            rangee = VerifierColonne(i + 1, tableau)       
            if rangee > -1:          
                tempCouleur = None
                tempJeton = None
                    
                x = i
                y = rangee
                
                tableau[x][y] = Jeton(jetonRouge, [0, 0], Couleur.ROUGE)
                
                nouvColonne, score = BonMiniMax(tableau, profondeur - 1, False, alpha, beta)
                
                tableau[x][y] = Jeton(None, [0, 0], None)
                
                #print("mazimize " + str(score))
                
                if bestScore < score:
                    colonne = i
                    bestScore = score
                    
                alpha = max(alpha, bestScore)
                if alpha >= beta:
                    break
                
        return colonne, bestScore
    else:
        bestScore = math.inf
        colonne = 0
            
        for i in range(7):
            rangee = VerifierColonne(i + 1, tableau)       
            if rangee > -1:          
                tempCouleur = None
                tempJeton = None
                
                x = i
                y = rangee
                
                tableau[x][y] = Jeton(jetonJaune, [0, 0], Couleur.JAUNE)
                             
                nouvColonne, score = BonMiniMax(tableau, profondeur - 1, True, alpha, beta)
                
                tableau[x][y] = Jeton(None, [0, 0], None)   
                
                if bestScore > score:
                    colonne = i
                    bestScore = score
                    
                beta = min(beta, bestScore)
                if alpha >= beta:
                    break
                
        return colonne, bestScore

def quatriemeNiveau (profondeur, couleur):

    tableau = [[Jeton(None, [0, 0], None) for i in range(6)] for j in range(7)]
    
    for y in range(6):
        for x in range(7):
            if (jeu[x][y].getImage() != None):
                tableau[x][y] = jeu[x][y]
                
    colonne, score = BonMiniMax(tableau, 6, True, -math.inf, math.inf)
    
    print(str(colonne) + " " + str(score))
    if colonne != None:
        return colonne + 1
    else:
        return -1

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
            if gameOver == False:
                x,y = pygame.mouse.get_pos()
                
                if (y > 50) :       
                    if compteurMove % 2 == 0:
                        if PlacerJeton(GetColoneSelected(), Couleur.JAUNE, jeu):
                            compteurMove += 1
                            if gameOver == False:
                                colonne = quatriemeNiveau(1, Couleur.ROUGE)
                                if colonne != -1:
                                    PlacerJeton(colonne, Couleur.ROUGE, jeu)
                                    compteurMove += 1                                          
                    #else:
                    #    if PlacerJeton(ColonneRandom(), Couleur.ROUGE):
                    #        compteurMove += 1
                            
                    #PrintJeu()
                else:
                    RedemarrerJeu()
        
        pygame.display.update()
