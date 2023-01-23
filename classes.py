import pygame 
from random import randint
from random import randrange
largura = 700
altura = 500
tela = pygame.display.set_mode((largura, altura))
sprite_sheet = pygame.image.load('imagens/dinoSpritesheet.png')
velocidade_jogo = 3
class Goku(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
    
        self.image = pygame.image.load("imagens/goku_do_jogo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,[110,110])
        self.rect = pygame.Rect(40,40,110,110)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocidade = 2
        self.aceleração = 0.2
        self.sound_morte = pygame.mixer.Sound('sons/som_morte.wav')
        self.sound_morte.set_volume(0.04)

    def update(self):
        controle = pygame.key.get_pressed()
        if controle[pygame.K_w]:
            self.velocidade -= self.aceleração
        if controle[pygame.K_s]:
            self.velocidade += self.aceleração
        else:
            self.velocidade *= 0.95
        self.rect.y += self.velocidade
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocidade = 0
        if self.rect.bottom > 500:
            self.rect.bottom = 500
            self.velocidade = 0
        
class Freeza(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.largura = 700
        self.image = pygame.image.load("imagens/freeza_do_jogo.png")
        self.image = pygame.transform.scale(self.image, [100, 100])
        self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (self.largura, randint(100, 400))
        self.pontos = 0
        self.velocidade_freeza = 3.0

    def update(self, *args):
        self.rect.x -= self.velocidade_freeza
        if self.rect.topright[0] < 0:
            self.pontos += 1
            self.rect.x = self.largura
            self.rect.y = randint(100, 400)

class Kamehameha(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.largura = 700
        self.image = pygame.image.load('imagens/kamehameha_do_jogo.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 4
        self.sound_disparo = pygame.mixer.Sound('sons/LASER_BU.WAV')
        self.sound_disparo.set_volume(0.008)

    def update(self, *args):
        self.rect.x += self.speed
        if self.rect.topleft[0] > self.largura:
            self.kill()

class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7 * 32,0),(32,32)) #Multiplico por 7 pois a nuvem está na pos. 7 da spritesheet
        self.image = pygame.transform.scale(self.image,(32*3,32*3))
        self.rect = self.image.get_rect()
        self.rect.x = largura - randrange(90, 300, 90)
        
    def update(self):
        if self.rect.topright[0] < 0: #Condição para a nuvem após sair pela esquerda, voltar pela direita.
            self.rect.x = largura
            self.rect.y = randrange(50, 200, 90) #Sorteio das posições das nuvens após a nuvem sair pela esquerda e voltar pela direita
        self.rect.x -= velocidade_jogo #Faz a nuvem se movimentar para a esquerda

class Sol(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load('imagens/sol.png')
        self.image = pygame.transform.scale(self.image,(80,80))
        self.rect = self.image.get_rect()
        self.rect.x = largura
        self.rect.y = 50
        self.velocidade_sol = 1

    def update(self):
        if self.rect.topright[0] < 0: #Condição para o sol após sair pela esquerda, voltar pela direita.
            self.rect.x = largura
        self.rect.x -= self.velocidade_sol
       
class Arvores(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load('imagens/arvore.png')
        self.image = pygame.transform.scale(self.image,(100,100))
        self.rect = self.image.get_rect()
        self.rect.x = largura - randrange(90, 300, 90)
        self.rect.y = 430
    
    def update(self):
        if self.rect.topright[0] < 0: #Condição para a árvore após sair pela esquerda, voltar pela direita.
            self.rect.x = largura
        self.rect.x -= velocidade_jogo #Faz a árvore se movimentar para a esquerda      
class Botao(pygame.sprite.Sprite):
    def __init__(self, largura, altura, imagem):
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.topleft = (largura, altura)
        self.clique = False
    def draw(self, x, y):
        tela.blit(self.image, (x, y))