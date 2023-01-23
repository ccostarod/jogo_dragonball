#importação do pygame, das classes contidas no arquivo classes.py e do módulo randint.
import pygame
from classes import Goku
from classes import Freeza
from classes import Kamehameha
from classes import Nuvens
from classes import Sol
from classes import Arvores
from classes import Botao
from random import randint

pygame.init() #Iniciando o Pygame.

#Constantes da tela, adição da tela, e adição do nome:
largura = 700
altura = 500
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('DragonBall: A Batalha no Céu.')

#cores utilizadas:
azul = (135,206,235)
preto = (0,0,0)

#Criação de alguns grupos com uma função do pygame.
personagem_grupo = pygame.sprite.Group()
inimigos_grupo = pygame.sprite.Group()
kamehameha_grupo = pygame.sprite.Group()
arvore_grupo = pygame.sprite.Group()
#Adição de todas as classes aos grupos criados:
for i in range(3):
    arvore = Arvores()
    personagem_grupo.add(arvore)
for i in range(4):
    nuvem = Nuvens()
    personagem_grupo.add(nuvem)
sol = Sol(personagem_grupo)
goku = Goku(personagem_grupo)
freeza = Freeza(personagem_grupo, inimigos_grupo)
kamehameha = Kamehameha()

#Outras váriaveis:
relogio = pygame.time.Clock()
pontos_freeza = 0
pontos = 0

#Carregamento das imagens utilizadas aqui:
background = pygame.image.load('imagens/capa_jogo_com_tutorial.jpg')
tutorial = pygame.image.load('imagens/tutorial.jpg')
img_play_botao = pygame.image.load('imagens/start_imagem.png').convert_alpha()
img_tutorial_botao = pygame.image.load('imagens/tutorial_botao.png').convert_alpha()
img_sair_botao = pygame.image.load('imagens/sair_tecla.png')
goku_pontos = pygame.image.load('imagens/goku_pontos.png')
goku_pontos = pygame.transform.scale(goku_pontos,(50,50))
freeza_pontos = pygame.image.load('imagens/freeza_pontos.png')
freeza_pontos = pygame.transform.scale(freeza_pontos, (43,43))

#Função de texto:
def exibemsg(msg, tamanho, cor):
    fonte = pygame.font.SysFont('Comicsansms', tamanho, True, False)
    mensagem = f'{msg:0>2}'
    texto_format = fonte.render(mensagem, True, cor)
    return texto_format
#Função para reiniciar o jogo (reinicia alguns atributos, como os pontos, algumas flags, e algumas posições de certas sprites.):
def reiniciar_jogo(): 
    global pontos, colidiu, pontos_freeza, kamehameha, tiro, alternativa2, alternativa
    tiro = True
    pontos = 0
    freeza.pontos = 0
    colidiu = False
    alternativa2 = False
    alternativa = False
    kamehameha.kill()
    sol.rect.x = largura
    nuvem.rect.x = largura
    arvore.rect.x = largura
    freeza.rect.x = largura
    goku.rect.y = 110
    goku.sound_morte.stop()
    freeza.velocidade_freeza = 3.0
#Carregamento da música de fundo e do som de clique:
musica_fundo = pygame.mixer.music.load('sons/abertura_dbz.mp3') 
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.01)
clique_som = pygame.mixer.Sound('sons/clique_som.wav')
clique_som.set_volume(0.1)

#Definindo os botões na classe Botao:
botao_inicial = Botao(30, 40, img_play_botao) 
botao_tutorial = Botao(30, 40, img_tutorial_botao)
botao_sair = Botao(30, 40, img_sair_botao)

#Condições para rodar o jogo:
gameLoop = False
tela_inicial_loop = True 
tela_tutorial_lopp = False
colidiu = False 
alternativa = False #Concede Derrota.
alternativa2 = False #Concede Vitória.
tiro = True #Flag para colocar delay no tiro.

#Loops de tela inicial e de tela de tutorial:
while tela_inicial_loop: #Loop para mostrar a tela inicial
    tela.blit(background,(0,0)) #Colocar a tela inicial na tela.
    botao_inicial.draw(250, 300) #Função para desenhar o botão de play
    botao_tutorial.draw(250, 380) #Função para desenhar o botão de de tutorial
    relogio.tick(100)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #Evento para fechar jogo na tela inicial
            tela_inicial_loop = False
            gameLoop = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE: #Evento para iniciar jogo caso aperte espaço
                clique_som.play()
                tela_inicial_loop = False
                gameLoop = True
                reiniciar_jogo() 
            if event.key == pygame.K_q: #Evento para abrir tela de tutorial caso aperte Q
                clique_som.play()
                tela_tutorial_lopp = True
                tela_inicial_loop = False
                while tela_tutorial_lopp: #Loop para mostrar a tela de tutorial
                    tela.blit(tutorial,(0,0))
                    botao_sair.draw(10, 400)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: #Evento para fechar jogo na tela de tutorial
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYUP: 
                            if event.key == pygame.K_q: #Evento para fechar tela de tutorial caso aperte Q novamente.
                                clique_som.play()
                                tela_inicial_loop = True
                                tela_tutorial_lopp = False
                    pygame.display.flip() #Atualiza o loop da tela de tutorial
    pygame.display.flip() #Atualiza o Loop da tela inicial

    #Loop principal de jogo:
    while gameLoop:
        tela.fill(azul) #Preenchimento de tela que representa o céu.
        relogio.tick(100) #Tick utilizado no jogo, atribuido a variável relogio.
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #Evento responsável pelo fechamento do jogo.
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and colidiu == False and alternativa2 == False: 
                if event.key == pygame.K_SPACE and tiro == True: #Evento responsável pelo disparo do kamehameha (apenas quando não tiver game over, ou seja, colidiu == False).
                    tiro = False #Tiro se torna False, logo não dá executar a ação várias vezes seguidas.
                    kamehameha = Kamehameha(personagem_grupo, kamehameha_grupo)
                    kamehameha.rect.center = goku.rect.midright
                    kamehameha.sound_disparo.play()
            #Caso haja colisão ou vitória, aí sim será possível reiniciar o jogo com a tecla R ou fechar com a tecla X:
            if event.type == pygame.KEYDOWN:
                if colidiu == True or alternativa2 == True: #Só acontecerá os eventos abaixo se colidiu for True ou se ele conseguiu obter os pontos para vitória.
                    if event.key == pygame.K_r:  #Evento Responsável para reiniciar o jogo a partir da tecla R
                        reiniciar_jogo()
                        clique_som.play()
                    if event.key == pygame.K_x: #Evento responsável pela volta da tela inicial  a partir da tecla X
                        clique_som.play()
                        gameLoop = False
                        tela_inicial_loop = True
                        goku.sound_morte.stop()
        #Desenho as sprites na tela:
        personagem_grupo.draw(tela)
        #Colisão entre Goku e Freeza e todas as consequências dela:    
        colisoes = pygame.sprite.spritecollide(goku, inimigos_grupo, False, pygame.sprite.collide_mask)
        if colisoes and colidiu == False or freeza.pontos == 5: #Caso haja colisão ou uma certa quantidade de Freeza's passem (nesse caso 5), o jogo para de atualizar as sprites.
            freeza.pontos = 0  #Para o som parar de tocar quando for igual a 5.
            goku.sound_morte.play()
            colidiu = True #Flag para tornar possível o próximo IF.
            alternativa = True
        if colidiu == True or pontos >= 50: #Carregamento do 'game over' ou do 'you win':
            if alternativa: #Caso tenha colidido com o Freeza ou deixado 5 passarem (game over).
                tela.fill(preto)
                game_over = pygame.image.load('imagens/game_over_img.png')
                tela.blit(game_over,(largura//2 - 179, altura//2 - 100))
                restart = pygame.image.load('imagens/tecla_reiniciar.png')
                tela.blit(restart,(largura//2 - 150, altura//2 + 60))
                fechar = pygame.image.load('imagens/menu_tecla.png')
                tela.blit(fechar,(largura//2 - 150, altura//2 + 140))
            if alternativa2: #Caso tenha matado todos os clones de Freeza. (game win)
                tela.fill(preto)
                you_win = pygame.image.load('imagens/you_win.png')
                tela.blit(you_win,(largura//2 - 179, altura//2 - 100))
                restart = pygame.image.load('imagens/tecla_reiniciar.png')
                tela.blit(restart,(largura//2 - 150, altura//2 + 60))
                fechar = pygame.image.load('imagens/menu_tecla.png')
                tela.blit(fechar,(largura//2 - 150, altura//2 + 140))
        else: #Condições caso não haja colisão ou vitória:
            personagem_grupo.update() #Atualizo os personagens
            texto_pontos = exibemsg(pontos, 40,(0,0,0)) 
            texto_pontos_freeza = exibemsg(freeza.pontos, 40,(255,0,0)) 
            tela.blit(goku_pontos, (277, 8)) #Continuo exibindo a cabeça do Goku, que indica os pontos dele.
            tela.blit(texto_pontos, (280, 50)) #Continuo exibindo o texto de pontos do goku.
            tela.blit(freeza_pontos, (392, 15)) #Continuo exibindo a cabeça do Freeza, que indica os pontos dele.
            tela.blit(texto_pontos_freeza, (390, 50)) #Continuo exibindo o texto de pontos do Freeza.
        #Colisão de tiro e a condição que ela causa no Freeza:
        colisao_tiro = pygame.sprite.groupcollide(kamehameha_grupo, inimigos_grupo, True, False, pygame.sprite.collide_mask)
        if colisao_tiro:
            tiro = True #Possibilita atirar de novo caso o Freeza seja atingido.
            #Sistema para aumentar velocidade de Freeza:
            freeza.velocidade_freeza += 0.2
            if freeza.velocidade_freeza >= 7.0:
                freeza.velocidade_freeza = 7.0
            pontos += 1 #Aumento dos pontos do Goku caso haja colisão entre o disparo e Freeza.
            #Condições para o Freeza voltar após levar um tiro:
            freeza.rect.x = largura 
            freeza.rect.y = randint(50, 400)
        #Possibilita atirar de novo caso o Freeza passe pelo limite da tela:
        if freeza.rect.x == largura: 
            tiro = True
        #Caso o jogador chegue a certa quantidade de pontos, o jogo acaba e ele ganha.
        if pontos == 50:
            alternativa2 = True
            som_vitoria = pygame.mixer.Sound('sons/efeito_vitoria.wav')
            som_vitoria.set_volume(0.01)
            som_vitoria.play()
            pontos = 51 #Som de vitória parar (por isso a condição para ganhar é: 'pontos >= 50')
        #Atualização da tela do jogo:
        pygame.display.flip()