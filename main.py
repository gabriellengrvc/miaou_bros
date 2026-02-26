import pygame as p
import sys

#initialisation de pygame 
p.init()
clock = p.time.Clock()
width, height = 800,600
terre_hauteur = 50
terre_y = height - terre_hauteur
screen = p.display.set_mode((width, height))
p.display.set_caption("Miau bros")
font = p.font.Font('PressStart2P-Regular.ttf', 30)

#images
chat_image = p.image.load('chat.png')
chat_image = p.transform.scale(chat_image, (70, 70))
fond_image = p.image.load('fond.png')
fond_width = fond_image.get_width() * height // fond_image.get_height()
fond_image = p.transform.scale(fond_image, (fond_width, height))
terre_image = p.image.load('terre.png')
terre_image = p.transform.scale(terre_image, (fond_width, terre_hauteur))
plateforme_image1 = p.image.load("plateforme1.png")
plateforme_image1 = p.transform.scale(plateforme_image1, (520, 172))
plateforme_image2 = p.image.load("plateforme2.png")
plateforme_image2 = p.transform.scale(plateforme_image2, (236, 50))
plateforme_image3 = p.image.load("plateforme3.png")
plateforme_image4 = p.image.load("plateforme4.png")
plateforme_image5 = p.image.load("plateforme5.png")
plateforme_image6 = p.image.load("plateforme6.png")
plateforme_image6 = p.transform.scale(plateforme_image6, (700, 172))
plateforme_image7 = p.image.load("plateforme7.png")
plateforme_image7 = p.transform.scale(plateforme_image7, (400, 135))
nuages_image = p.image.load('nuages.png')
nuages_image = p.transform.scale(nuages_image,(fond_width, height))
nuages2_image = p.image.load('nuages2.png')
nuages2_image = p.transform.scale(nuages2_image,(fond_width, height))
eau_image = p.image.load('eau.png')
eau_image = p.transform.scale(eau_image, (fond_width, height))

#le chat
class Chat:
    def __init__(self, x, y):
        self.original_image = chat_image
        self.image = self.original_image
        self.world_x = float(x)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.vitesse = 5
        self.gravity = 0.8
        self.saute_niveau = -15
        self.sur_terre = False
        self.sautes_restants = 2
        self.rotation = False
        self.angle = 0

    def move_left(self):
        self.world_x -= self.vitesse

    def move_right(self):
        self.world_x += self.vitesse

    def update(self, plateformes):
        self.rect.x = int(self.world_x)
        self.vel_y += self.gravity
        self.rect.y += int(self.vel_y)

        for plat in plateformes:
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0:  # falling
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.sautes_restants = 2
                    self.rotation = False
                    self.angle = 0
                elif self.vel_y < 0:  # jumping up
                    self.rect.top = plat.rect.bottom
                    self.vel_y = 0

        if self.rect.bottom >= terre_y:
            self.rect.bottom = terre_y
            self.vel_y = 0
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
            
    def saute(self):
        if self.sautes_restants > 0:
            if self.sautes_restants == 1: 
                self.vel_y = self.saute_niveau * 1.2
                self.rotation = True
            else:
                self.vel_y = self.saute_niveau
            self.sautes_restants -= 1

    def draw(self, surface, camera_x):
        screen_x = int(self.world_x - camera_x)
        self.rect.x = screen_x
        surface.blit(self.image, self.rect)
            
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
    chat = Chat(50, height // 2)
    world_width = fond_width  
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
    plateformes = [plateforme1, plateforme2, plateforme3, plateforme4, plateforme5,plateforme6,plateforme7]
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == p.KEYDOWN and event.key == p.K_SPACE:
                chat.saute()
        keys = p.key.get_pressed()
        if keys[p.K_LEFT]:
            chat.move_left()
        if keys[p.K_RIGHT]:
            chat.move_right()
        chat.world_x = clamp(chat.world_x, 0, world_width - chat.rect.width)
        chat.update(plateformes)
        camera_x = chat.world_x + chat.rect.width/2 - width/2
        camera_x = clamp(camera_x, 0, world_width - width)
        screen.blit(fond_image, (-camera_x, 0))
        screen.blit(nuages2_image, (-camera_x * 0.3, 0))
        screen.blit(nuages_image, (-camera_x * 0.5, 0))
        screen.blit(eau_image, (-camera_x, height - 530))
        screen.blit(terre_image, (-camera_x, height - terre_hauteur))
        for plat in plateformes:
            plat.draw(screen, camera_x)
        chat.draw(screen, camera_x)
        clock.tick(60)
        p.display.flip()

    p.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()
