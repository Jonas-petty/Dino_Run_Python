import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

musica_de_fundo = pygame.mixer.music.load('Alceu Valença - Anunciação - Karaokê.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


gravidade = 0

largura = 640
altura = 480

azul = (0, 161, 254)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Super Mário Recife')

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'sprites.png')).convert_alpha()

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'death_sound.wav'))
som_colisao.set_volume(1)

som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'score_sound.wav'))
som_pontuacao.set_volume(1)

colidiu = False

escolha_obstaculo = choice([0, 1])

pontos = 0

velocidade_jogo = 10

def velocidade():
    if pontos <= 50:
        velocidade_jogo = 10
    else:
        velocidade_jogo = 50    


def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

def reiniciar_jogo():
    global pontos, velocidade_jogo, colidiu, escolha_obstaculo
    pontos = 0
    velocidade_jogo = 10
    colidiu = False
    dino.rect.y = altura - 74 - 96 // 2
    dino.pulo = False
    pau.rect.x = largura
    pombo.rect.x = largura
    escolha_obstaculo = choice([0, 1])
    pygame.mixer.music.play(-1)


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'jump_sound.wav'))
        self.som_pulo.set_volume(1)
        self.imagens_jonas = []
        for i in range(6):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_jonas.append(img)

        self.index_lista = 0
        self.image = self.imagens_jonas[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = altura - 74 - 96 // 2
        self.rect.center = [100, 500]
        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self):
        if self.pulo:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 20
        # else:
        #     if self.rect.y < self.pos_y_inicial:
        #         self.rect.y += 20
        #     else:
        #         self.rect.y = self.pos_y_inicial

        if self.rect.y > self.pos_y_inicial:
            self.rect.y = self.pos_y_inicial

        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_jonas[int(self.index_lista)]


class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32 * 12, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = largura - randrange(30, 300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= velocidade_jogo


class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32 * 10, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.rect.y = altura - 64
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -= 10


class Pau(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dog = []
        for i in range(8, 10):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 2.5, 32 * 2.5))
            self.imagens_dog.append(img)
        self.index_lista = 0
        self.image = self.imagens_dog[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.rect.center = (largura, altura - 60)
        self.rect.x = largura

    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= velocidade_jogo

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_dog[int(self.index_lista)]


class Pombo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_pombo = []
        for i in range(6, 8):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_pombo.append(img)
        self.index_lista = 0
        self.image = self.imagens_pombo[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.rect.center = (largura, 300)
        self.rect.x = largura

    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= velocidade_jogo

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_pombo[int(self.index_lista)]


todas_as_sprites = pygame.sprite.Group()
dino = Dino()
todas_as_sprites.add(dino)

for i in range(4):
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)

#for i in range(largura * 2 // 64):
    #chao = Chao(i)
    #todas_as_sprites.add(chao)

pau = Pau()
todas_as_sprites.add(pau)

pombo = Pombo()
todas_as_sprites.add(pombo)

grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(pau)
grupo_obstaculos.add(pombo)

relogio = pygame.time.Clock()


def fundo():
    if pontos >= 100:
        imagem_fundo = pygame.image.load('MarcoZero.bmp').convert()
        imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))
        tela.blit(imagem_fundo, (0, 0))
        todas_as_sprites.draw(tela)
        
    if 0 <= pontos <= 100:
        imagem_fundo = pygame.image.load('moeda.bmp').convert()
        imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))
        tela.blit(imagem_fundo, (0, 0))
        todas_as_sprites.draw(tela)


while True:

    relogio.tick(30)
    tela.fill(azul)
    fundo()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and colidiu is False:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    gravidade = -15
                    dino.rect.y -= 10
                    # gravidade = -15
                    # dino.pular()

            if event.key == K_r and colidiu is True:
                reiniciar_jogo()

    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask)

    gravidade += 1
    dino.rect.y += gravidade

    if pau.rect.topright[0] <= 0 or pombo.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0, 1])
        pau.rect.x = largura
        pombo.rect.x = largura
        pau.escolha = escolha_obstaculo
        pombo.escolha = escolha_obstaculo

    if colisoes and colidiu is False:
        som_colisao.play()
        colidiu = True

    if colidiu is True:
        if pontos % 100 == 0:
            pontos += 1
        game_over = exibe_mensagem('GAME OVER', 40, (255, 255, 255))
        tela.blit(game_over, (largura//2, altura//2))
        restart = exibe_mensagem('Precione r para reiniciar', 20, (255, 255, 255))
        tela.blit(restart, (largura//2, (altura//2) + 60))
        pygame.mixer.music.stop()

    else:
        pontos += 0.2
        todas_as_sprites.update()
        texto_pontos = exibe_mensagem("%.0f" % pontos, 50, (255, 255, 255))

    pontos = round(pontos, 2)

    if pontos % 100 == 0.0:
        som_pontuacao.play()
        velocidade_jogo += 5
        print("Adicionou 5")

    tela.blit(texto_pontos, (largura/2, 30))

    pygame.display.flip()