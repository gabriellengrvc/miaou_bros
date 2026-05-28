import pygame as p
import sys
import random

# INITIALISATION
p.init()
clock = p.time.Clock()
largeur, hauteur = 800,600
screen = p.display.set_mode((largeur, hauteur))
p.display.set_caption("Miaou bros")
font_30 = p.font.Font('PressStart2P-Regular.ttf', 30)
font_60 = p.font.Font("PressStart2P-Regular.ttf", 60)

# LES CONSANTES
terre_hauteur = 50
terre_y = hauteur - terre_hauteur
eau_y = terre_y - 30
fond_largeur = 4200

# LA MUSIQUE
p.mixer.music.load("Midnight Sun.mp3")
p.mixer.music.play(-1)

# LES IMAGES
chat_image = p.image.load('images/marche1.png')
chat_assis_image = p.image.load('images/animation1.png')
chat_saut_image = p.image.load('images/saut.png')
chat_saut_image = p.transform.scale(chat_saut_image, (85, 67))
fond1_image = p.image.load('images/fond.png')
fond1_image = p.transform.scale(fond1_image, (4200,600))
fond2_image = p.image.load('images/fond_2.png')
fond2_image = p.transform.scale(fond2_image, (4200,600))
terre1_image = p.image.load('images/terre.png')
terre2_image = p.image.load('images/grass_2.png')
plateforme_image1 = p.image.load("plateformes/plateforme1.png")
plateforme_image1 = p.transform.scale(plateforme_image1, (520, 172))
plateforme_image2 = p.image.load("plateformes/plateforme2.png")
plateforme_image3 = p.image.load("plateformes/plateforme3.png")
plateforme_image4 = p.image.load("plateformes/plateforme4.png")
plateforme_image5 = p.image.load("plateformes/plateforme5.png")
plateforme_image6 = p.image.load("plateformes/plateforme6.png")
plateforme_image6 = p.transform.scale(plateforme_image6, (700, 172))
plateforme_image7 = p.image.load("plateformes/plateforme7.png")
plateforme_image7 = p.transform.scale(plateforme_image7, (400, 135))
plateforme_image8 = p.image.load("plateformes/plateforme_2_1.png")
plateforme_image8 = p.transform.scale(plateforme_image8, (515, 172))
plateforme_image9 = p.image.load("plateformes/plateforme_2_2.png")
plateforme_image9 = p.transform.scale(plateforme_image9, (230, 39))
plateforme_image10 = p.image.load("plateformes/plateforme_2_3.png")
plateforme_image10 = p.transform.scale(plateforme_image10, (38, 40))
plateforme_image11 = p.image.load("plateformes/plateforme_2_4.png")
plateforme_image11 = p.transform.scale(plateforme_image11, (190, 65))
plateforme_image12 = p.image.load("plateformes/plateforme_2_5.png")
plateforme_image12 = p.transform.scale(plateforme_image12, (320, 64))
plateforme_image13 = p.image.load("plateformes/plateforme_2_6.png")
plateforme_image13 = p.transform.scale(plateforme_image13, (400, 135))
nuages_image = p.image.load('images/nuages.png')
nuages2_image = p.image.load('images/nuages2.png')
eau1_image = p.image.load('images/eau.png')
eau2_image = p.image.load('images/lava.png')
images_animation = [p.transform.scale(p.image.load('images/animation1.png'),(74,88)),
                    p.transform.scale(p.image.load('images/animation2.png'),(74,88)),
                    p.transform.scale(p.image.load('images/animation3.png'),(74,88)),
                    p.transform.scale(p.image.load('images/animation4.png'),(74,88))]
images_marche = [p.transform.scale(p.image.load('images/marche1.png'),(80,88)),
                 p.transform.scale(p.image.load('images/marche2.png'),(82,88))]
image_enemy = p.image.load("images/ennemi.png")
image_enemy2 = p.image.load("images/ennemi2.png")
image_accueil = p.image.load("images/accueil.png")
image_bouton_start = p.image.load("images/bouton_start.png")
image_bouton_restart = p.image.load("images/bouton_restart.png")

# LA CLASSE CHAT
class Chat:
    def __init__(self, x, y):
        
        #positionnement
        self.debut_x = x
        self.debut_y = y
        self.world_x = x
        
        #images du chat
        self.image_saut2 = chat_saut_image
        self.image_marche = images_marche
        self.image_saut1 = images_marche[0]
        self.image = images_animation[1]
        self.image_animation = images_animation
        self.i = 0
        
        #rotation du chat
        self.diff_x = 0
        self.diff_y = 0
        self.angle = 0
        chat_taille = self.image.get_rect()
        self.chat_centre_x = chat_taille.center[0]
        self.chat_centre_y = chat_taille.center[1]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rotation = False
        
        #deplacement 
        self.deplacement_x = 0.0
        self.deplacement_y = 0.0
        self.vitesse = 4
        self.gravite = 0.8
        self.intensite_saute = -15.0
        self.sautes_restants = 2
        
        #paramètres
        self.niveau = 1
        self.droite = True
        self.gagne = False 

    def mettre_a_jour(self, plateformes, enemys):
        
        #mouvement horizontal et collision
        self.world_x += self.deplacement_x
        self.rect.x = int(self.world_x)
        for plat in plateformes:
            if self.rect.colliderect(plat.rect):
                if self.deplacement_x > 0:
                    self.rect.right = plat.rect.left 
                    self.world_x = self.rect.x
                elif self.deplacement_x < 0:
                    self.rect.left = plat.rect.right
                    self.world_x = self.rect.x
        
        #mouvement vertical et collision
        self.deplacement_y += self.gravite
        self.rect.y += int(self.deplacement_y)
        for plat in plateformes:
            if self.rect.colliderect(plat.rect):
                if self.deplacement_y > 0:
                    self.rect.bottom = plat.rect.top
                    self.deplacement_y = 0
                    self.sautes_restants = 2 #pour que le chat puisse sauter après 
                    self.rotation = False #pour arrêter l'animation de rotation
                    self.angle = 0 #pour réinitialiser angle de rotation
                elif self.deplacement_y < 0:
                    self.rect.top = plat.rect.bottom
                    self.deplacement_y = 0 
        
        #animations du chat 
        if self.deplacement_x > 0:
            self.i += 1
            if self.i < 15:
                self.image = self.image_marche[0]
            elif self.i < 30:
                self.image = self.image_marche[1]
            else:
                self.i = 0
            self.droite = True
        if self.deplacement_x < 0:
            self.i += 1
            if self.i < 15:
                self.image = p.transform.flip(self.image_marche[0], True, False)
            elif self.i < 30:
                self.image = p.transform.flip(self.image_marche[1], True, False)
            else:
                self.i = 0
            self.droite = False
        if self.deplacement_x == 0 and self.droite == True:
            self.i += 1
            if self.i < 15:
                self.image = self.image_animation[0]
            elif self.i < 30:
                self.image = self.image_animation[1]
            elif self.i < 45:
                self.image = self.image_animation[2]
            elif self.i < 60:
                self.image = self.image_animation[3]
            elif self.i < 75:
                self.image = self.image_animation[2]
            elif self.i < 90:
                self.image = self.image_animation[1]
            else:
                self.i = 0
        if self.deplacement_x == 0 and self.droite == False:
            self.i += 1
            if self.i < 15:
                self.image = p.transform.flip(self.image_animation[0], True, False)
            elif self.i < 30:
                self.image = p.transform.flip(self.image_animation[1], True, False)
            elif self.i < 45:
                self.image = p.transform.flip(self.image_animation[2], True, False)
            elif self.i < 60:
                self.image = p.transform.flip(self.image_animation[3], True, False)
            elif self.i < 75:
                self.image = p.transform.flip(self.image_animation[2], True, False)
            elif self.i < 90:
                self.image = p.transform.flip(self.image_animation[1], True, False)
            else:
                self.i = 0
        if self.sautes_restants == 1 and self.deplacement_x > 0:
            self.image = self.image_saut2
        if self.sautes_restants == 1 and self.deplacement_x < 0:
            self.image = p.transform.flip(self.image_saut2, True, False)
        
        #rotation lorsque le chat fait un double saut
        if self.rotation:
            self.angle += 10
            if self.angle >= 360:
                self.angle = 0
                self.rotation = False
            self.image = p.transform.rotate(chat_saut_image, self.angle)
            chat_rot_taille = self.image.get_rect()
            chat_rot_centre_x = chat_rot_taille.center[0]
            chat_rot_centre_y = chat_rot_taille.center[1]
            self.diff_x = int(chat_rot_centre_x - self.chat_centre_x)
            self.diff_y = int(chat_rot_centre_y - self.chat_centre_y)
        else:
            self.diff_x = 0
            self.diff_y = 0
            
        #les respawn 
        if self.rect.bottom >= eau_y:
            if self.niveau == 2: 
                self.niveau = 1
                self.vitesse = 4
            self.reinitialiser()
        elif self.rect.right >= fond_largeur:
            if self.niveau == 1:
                self.niveau = 2
                self.vitesse = 6
                self.reinitialiser()
            else:
                self.gagne = True
        for enemy in enemys:
            if self.rect.colliderect(enemy.rect):
                self.niveau = 1
                self.vitesse = 4
                self.reinitialiser()
                enemy.reinitialiser(self.debut_x)
            
    def saute(self): 
        if self.sautes_restants > 0:
            if self.sautes_restants == 1:
                self.deplacement_y = self.intensite_saute * 1.2
                self.rotation = True
            else:
                self.deplacement_y = self.intensite_saute
            self.sautes_restants -= 1
    
    def affiche(self, surface, camera_x):

        #notre système de coordonnées:
        #world_x est la position réelle dans le monde (0 à fond_largeur)
        #camera_x est la position du bord gauche de la caméra dans de l'écran
        #screen_x est la position à l'écran = world_x - camera_x
        #on convertit coordonnées monde en coordonnées écran
        screen_x = int(self.world_x - camera_x)
        #quand le chat tourne, l'image agrandit, on soustrait diff_x et diff_y pour que le chat reste centré au même endroit pendant la rotation
        surface.blit(self.image, (screen_x - self.diff_x, self.rect.y - self.diff_y))

    def reinitialiser(self):
        self.world_x = self.debut_x
        self.rect.x = self.debut_x
        self.rect.y = self.debut_y
        self.deplacement_x = 0
        self.deplacement_y = 0
        self.sautes_restants = 2
        self.angle = 0
        self.rotation = False
        self.gagne = False
        
# LA CLASSE PLATEFORME
class Plateforme:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def affiche(self, surface, camera_x):
        #lorsque la camera_x augmente, les plateformes se déplacent vers la gauche
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

# LA CLASSE ENNEMI 
class Enemy():
    def __init__(self, chat_pos):
        self.image = image_enemy
        self.rect = self.image.get_rect()
        #l'ennemi apparaît aléatoirement au moins 100px devant le chat et au max 800px devant le chat 
        #entre minimum 400px et maximum 3800ox du monde pour éviter qui'ils apparaissent tout au début/à la fin
        spawn = chat_pos + random.randint(100,800)
        if spawn < 400:
            spawn = 400
        elif spawn > 3800:
            spawn = 3800
        self.rect.x = spawn
        self.rect.y = random.randint(-600, -400)
        self.vitesse_y = 5
        self.vitesse_x = 0
        
    def mettre_a_jour(self, plateformes, chat_pos, niveau):
        if niveau == 1:
            self.image = image_enemy
        else:
            self.image = image_enemy2
        self.rect.y += self.vitesse_y
        for plat in plateformes: #ennemi suit le chat
            if self.rect.colliderect(plat.rect): 
                #si le chat est à droite il va à droite
                if chat_pos > self.rect.x:
                    self.vitesse_x = 2
                #si gauche il va à gauche
                elif chat_pos < self.rect.x:
                    self.vitesse_x = -2
                #si l'ennemi et chat partage la même position il s'arrête
                else:
                    self.vitesse_x = 0
                self.rect.bottom = plat.rect.top
                self.rect.x += self.vitesse_x
        
    def check_status(self, chat_pos):
        if self.rect.bottom>=eau_y:
            self.reinitialiser(chat_pos)
                
    def reinitialiser(self, chat_pos):
        self.image = image_enemy
        self.rect = self.image.get_rect()
        spawn = chat_pos + random.randint(100,800)
        if spawn < 400:
            spawn = 400
        elif spawn > 3800:
            spawn = 3800
        self.rect.x = spawn
        self.rect.y = random.randint(-600, -400)
        self.vitesse_y = 5
        self.vitesse_x = 0                             
        
    def affiche(self, surface, camera_x):
        #on convertit coordonnées monde en coordonnées écran
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))    

# LA CLASSE BOUTON
class Bouton:
    def __init__(self, image, position):
        self.image = p.transform.scale(image, (283, 134))
        self.rect = self.image.get_rect(center=position)

    def etat_bouton(self):
        return self.rect.collidepoint(p.mouse.get_pos())

bouton_start = Bouton(image_bouton_start, (634, 434))

# L'ECRAN D'ACCUEIL
def accueil():
    while True:
        screen.blit(image_accueil, (0, 0))
        titre_accueil = font_60.render("Miaou Bros", True, (255,255,255))
        screen.blit(titre_accueil, (largeur // 2  - titre_accueil.get_width() // 2, 100))

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if bouton_start.etat_bouton():
                    return
        
        screen.blit(bouton_start.image, bouton_start.rect)
        p.display.flip()
        clock.tick(30)
    
bouton_restart = Bouton(image_bouton_restart, (largeur//2, hauteur//2 - 50))

# L'ECRAN VICTOIRE
def victoire(surface):
    overlay = p.Surface((largeur, hauteur))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(160) #overlay semi-transparent
    surface.blit(overlay, (0, 0))
    titre_victoire = font_30.render("YOU WIN!", True, (255, 220, 50))
    surface.blit(titre_victoire, (largeur//2 - titre_victoire.get_width()//2, 200))
    screen.blit(bouton_restart.image, bouton_restart.rect)
                
# LA BOUCLE PRINCIPALE
def main():
    chat = Chat(50, 300)
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
    plateforme14 = Plateforme(0, 0, plateforme_image8)
    plateforme14.rect.bottom = terre_y
    plateforme15 = Plateforme(670, 100, plateforme_image9)
    plateforme16 = Plateforme(1070, 350, plateforme_image10)
    plateforme17 = Plateforme(1320, 0, plateforme_image11)
    plateforme17.rect.bottom = terre_y 
    plateforme18 = Plateforme(1600, 300, plateforme_image12)
    plateforme19 = Plateforme(2300, 0, plateforme_image13)
    plateforme19.rect.bottom = terre_y
    plateforme20 = Plateforme(2820, 200, plateforme_image12)
    plateforme21 = Plateforme(3370, 380, plateforme_image11)
    plateforme22 = Plateforme(3430, 700, plateforme_image9)
    plateforme23 = Plateforme(3700, 0, plateforme_image8)
    plateforme23.rect.bottom = terre_y
    plateformes2 = [plateforme14, plateforme15, plateforme16, plateforme17, plateforme18, plateforme19, plateforme20, plateforme21, plateforme22, plateforme23]

    enemys_niveau1 = [Enemy(50)] #crée un ennemi à un emplacement aléatoire devant le chat (qui se trouve à 50px au début)
    enemys_niveau2= [Enemy(50), Enemy(50)] #crée 2 ennemis à un emplacement aléatoire devant le chat
        
    running = True
   
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if chat.gagne:
                if event.type == p.MOUSEBUTTONDOWN:
                    if bouton_restart.etat_bouton():
                        return 
            if not chat.gagne:
                if event.type == p.KEYDOWN:
                    if event.key == p.K_LEFT:
                        chat.deplacement_x = -chat.vitesse
                    elif event.key == p.K_RIGHT:            
                        chat.deplacement_x = chat.vitesse
                    elif event.key == p.K_SPACE:
                        chat.saute()
                if event.type == p.KEYUP:
                    if event.key == p.K_LEFT:
                        chat.deplacement_x = 0
                    elif event.key == p.K_RIGHT:
                        chat.deplacement_x = 0
        
        if not chat.gagne:              
            if chat.niveau == 1:
                fond_image = fond1_image
                terre_image = terre1_image
                eau_image = eau1_image
                plateformes_actives = plateformes
                enemys_actifs = enemys_niveau1
            if chat.niveau == 2:
                fond_image = fond2_image
                terre_image = terre2_image
                eau_image = eau2_image
                plateformes_actives = plateformes2
                enemys_actifs = enemys_niveau2
            chat.mettre_a_jour(plateformes_actives, enemys_actifs)
            
            #on limite le déplacement du chat dans le monde
            if chat.world_x < 0:
                chat.world_x = 0
            if chat.world_x > fond_largeur - chat.rect.width:
                chat.world_x = fond_largeur - chat.rect.width

        #camera_x est la position de la caméra dans le monde, on limite la camera_x pour éviter zones vides à gauche ou à droite du fond
        camera_x = chat.world_x + chat.rect.width/2 - largeur/2
        if camera_x < 0:
            camera_x = 0
        if camera_x > fond_largeur - largeur:
            camera_x = fond_largeur - largeur
        
        #lorsque la camera_x augmente, les éléments se déplacent vers la gauche, créant l'illusion que le chat se déplace vers la droite
        screen.blit(fond_image, (-camera_x, 0))
        screen.blit(eau_image, (-camera_x, hauteur - 530))
        screen.blit(terre_image, (-camera_x, terre_y))
        
        #les nuages se déplacent plus lentement que le fond pour créer un effet cool 
        if chat.niveau == 1:
            screen.blit(nuages2_image, (-camera_x * 0.3, 0))
            screen.blit(nuages_image, (-camera_x * 0.5, 0))
        
        for plat in plateformes_actives:
            plat.affiche(screen, camera_x)
                
        chat_pos=chat.world_x
        
        for enemy in enemys_actifs:
            enemy.check_status(chat_pos)
            enemy.mettre_a_jour(plateformes_actives, chat_pos, chat.niveau)
            enemy.affiche(screen, camera_x)
        
        chat.affiche(screen, camera_x)
        titre = font_30.render("Miaou Bros", True, (255,255,255))
        screen.blit(titre, (largeur // 2 - titre.get_width() // 2 , 20))
        
        if chat.gagne:
            victoire(screen)
        
        p.display.flip()
        clock.tick(60)

    p.quit()
    sys.exit()
    
if __name__ == "__main__":
    while True: 
        accueil()
        main()
