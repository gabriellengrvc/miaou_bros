import pygame as p
import sys

#initialisation de pygame 
p.init()
clock = p.time.Clock()
largeur, hauteur = 800,600
screen = p.display.set_mode((largeur, hauteur))
p.display.set_caption("Miau bros")
font = p.font.Font('PressStart2P-Regular.ttf', 30)

#variables
terre_hauteur = 50
terre_y = hauteur - terre_hauteur
eau_y = terre_y - 30

#images
chat_image = p.image.load('images/chat.png')
chat_image = p.transform.scale(chat_image, (70, 70))
fond_image = p.image.load('images/fond.png')
fond_largeur = fond_image.get_width() * hauteur // fond_image.get_height()
fond_image = p.transform.scale(fond_image, (fond_largeur, hauteur))
terre_image = p.image.load('images/terre.png')
terre_image = p.transform.scale(terre_image, (fond_largeur, terre_hauteur))
plateforme_image1 = p.image.load("plateformes/plateforme1.png")
plateforme_image1 = p.transform.scale(plateforme_image1, (520, 172))
plateforme_image2 = p.image.load("plateformes/plateforme2.png")
plateforme_image2 = p.transform.scale(plateforme_image2, (236, 50))
plateforme_image3 = p.image.load("plateformes/plateforme3.png")
plateforme_image4 = p.image.load("plateformes/plateforme4.png")
plateforme_image5 = p.image.load("plateformes/plateforme5.png")
plateforme_image6 = p.image.load("plateformes/plateforme6.png")
plateforme_image6 = p.transform.scale(plateforme_image6, (700, 172))
plateforme_image7 = p.image.load("plateformes/plateforme7.png")
plateforme_image7 = p.transform.scale(plateforme_image7, (400, 135))
nuages_image = p.image.load('images/nuages.png')
nuages_image = p.transform.scale(nuages_image,(fond_largeur, hauteur))
nuages2_image = p.image.load('images/nuages2.png')
nuages2_image = p.transform.scale(nuages2_image,(fond_largeur, hauteur))
eau_image = p.image.load('images/eau.png')
eau_image = p.transform.scale(eau_image, (fond_largeur, hauteur))

#le chat
class Chat:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.original_image = chat_image
        self.image = self.original_image
        self.world_x = float(x)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.deplacement_x = 0
        self.deplacement_y = 0
        self.vitesse = 5
        self.gravite = 0.8
        self.saute_niveau = -15
        self.sur_terre = False
        self.sautes_restants = 2
        self.rotation = False
        self.angle = 0

    def update(self, plateformes):
        self.world_x += self.deplacement_x
        self.rect.x = int(self.world_x)
        #Utilisation de la gravité
        self.rect.y += int(self.deplacement_y)
        self.deplacement_y += self.gravite

        for plat in plateformes:
            if self.rect.colliderect(plat.rect):
                if self.deplacement_y > 0:  # falling
                    self.rect.bottom = plat.rect.top
                    self.deplacement_y = 0
                    self.sautes_restants = 2
                    self.rotation = False
                    self.angle = 0
                elif self.deplacement_y < 0:  # jumping up
                    self.rect.top = plat.rect.bottom
                    self.deplacement_y = 0

        if self.rect.bottom >= terre_y:
            self.rect.bottom = terre_y
            self.deplacement_y = 0
            self.sautes_restants = 2
            self.rotation = False
            self.angle = 0

        if self.rotation:
            self.angle += 10
            if self.angle >= 360:
                self.angle=0
                self.rotation = False
            old_center = self.rect.center
            self.image = p.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=old_center)
        else:
            self.image = self.original_image

        if self.rect.bottom >= eau_y:
            self.reset()
            
    def saute(self):
        if self.sautes_restants > 0:
            if self.sautes_restants == 1: 
                self.deplacement_y = self.saute_niveau * 1.2
                self.rotation = True
            else:
                self.deplacement_y = self.saute_niveau
            self.sautes_restants -= 1

    def draw(self, surface, camera_x):
        screen_x = int(self.world_x - camera_x)
        surface.blit(self.image, (screen_x, self.rect.y))

    def reset(self):
        self.world_x = self.start_x
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.deplacement_y = 0
        self.sautes_restants = 2
        self.rotation = False
        self.angle = 0
            
#les plateformes 
class Plateforme:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

#boucle principale du jeu
def main():
    chat = Chat(50, hauteur // 2)
    world_largeur = fond_largeur  
    plateforme1 = Plateforme(0, 0, plateforme_image1)
    plateforme1.rect.bottom = terre_y 
    plateforme2 = Plateforme(550, 300, plateforme_image2)
    plateforme3 = Plateforme(815, 250, plateforme_image3)
    plateforme4 = Plateforme(875, 0, plateforme_image4)
    plateforme4.rect.bottom = terre_y 
    plateforme5 = Plateforme(1154, 0, plateforme_image5)
    plateforme5.rect.bottom = terre_y
    plateforme6 = Plateforme(1600, 0, plateforme_image6)
    plateforme6.rect.bottom = terre_y
    plateforme7 = Plateforme(3900, 0, plateforme_image7)
    plateforme7.rect.bottom = terre_y
    plateforme8 = Plateforme(2400, 200, plateforme_image2)
    plateforme9 = Plateforme(2900, 150, plateforme_image3)
    plateforme10 = Plateforme(3200, 400, plateforme_image4)
    plateforme11 = Plateforme(3500, 290, plateforme_image3)
    plateforme12 = Plateforme(3650, 260, plateforme_image3)
    plateforme13 = Plateforme(3800, 240, plateforme_image3)
    plateformes = [plateforme1, plateforme2, plateforme3, plateforme4, plateforme5,plateforme6,plateforme7, plateforme8, plateforme9, plateforme10, plateforme11, plateforme12, plateforme13]
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_LEFT:
                    chat.deplacement_x = -chat.vitesse
                elif event.key == p.K_RIGHT:
                    chat.deplacement_x = chat.vitesse
                elif event.key == p.K_SPACE:
                    chat.saute()
            if event.type == p.KEYUP:
                if event.key == p.K_LEFT or event.key == p.K_RIGHT:
                    chat.deplacement_x = 0
        chat.update(plateformes)
        chat.world_x = clamp(chat.world_x, 0, world_largeur - chat.rect.width)
        camera_x = chat.world_x + chat.rect.width/2 - largeur/2
        camera_x = clamp(camera_x, 0, world_largeur - largeur)
        screen.blit(fond_image, (-camera_x, 0))
        screen.blit(nuages2_image, (-camera_x * 0.3, 0))
        screen.blit(nuages_image, (-camera_x * 0.5, 0))
        screen.blit(eau_image, (-camera_x, hauteur - 530))
        screen.blit(terre_image, (-camera_x, hauteur - terre_hauteur))
        for plat in plateformes:
            plat.draw(screen, camera_x)
        chat.draw(screen, camera_x)
        titre = font.render("Miaou Bros", True, (255,255,255))
        screen.blit(titre, (largeur // 2 - titre.get_width() // 2 , 20))
        p.display.flip()
        clock.tick(60)

    p.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()
