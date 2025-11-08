import pygame
import random
import sys

pygame.init()

# Configurações da janela
LARGURA, ALTURA = 480, 640
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🚀 Jato Desviando dos Tiros")

# Clock e fonte
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 28, bold=True)

# Carrega imagens
fundo = pygame.image.load("images/galaxy.png")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

img_jato = pygame.image.load("images/airplane.png")
img_jato = pygame.transform.scale(img_jato, (60, 50))

img_tiro = pygame.image.load("images/tiro.png")
img_tiro = pygame.transform.scale(img_tiro, (15, 25))

img_inimigo = pygame.image.load("images/inimigo.png")
img_inimigo = pygame.transform.scale(img_inimigo, (60, 50))

# --- Classes ---
class Jato(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_jato
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA // 2
        self.rect.bottom = ALTURA - 30
        self.velocidade = 6

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < LARGURA:
            self.rect.x += self.velocidade

class TiroInimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_tiro
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, LARGURA - self.rect.width)
        self.rect.y = -20
        self.velocidade = random.randint(4, 8)

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA:
            self.kill()

# --- Função principal ---
def jogo():
    todos = pygame.sprite.Group()
    tiros_inimigos = pygame.sprite.Group()
    jogador = Jato()
    todos.add(jogador)

    pontuacao = 0
    rodando = True

    while rodando:
        clock.tick(60)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Criar tiros inimigos
        if random.random() < 0.03:
            tiro = TiroInimigo()
            todos.add(tiro)
            tiros_inimigos.add(tiro)

        # Atualizações
        todos.update()

        # Colisões
        if pygame.sprite.spritecollide(jogador, tiros_inimigos, False):
            rodando = False

        # Pontuação
        pontuacao += 1

        # Desenhar
        janela.blit(fundo, (0, 0))
        todos.draw(janela)
        texto = fonte.render(f"Pontos: {pontuacao}", True, (255, 255, 255))
        janela.blit(texto, (10, 10))
        pygame.display.flip()

    tela_game_over(pontuacao)

# --- Tela de Game Over ---
def tela_game_over(pontuacao):
    while True:
        janela.blit(fundo, (0, 0))
        texto1 = fonte.render("💥 GAME OVER 💥", True, (255, 70, 70))
        texto2 = fonte.render(f"Pontuação: {pontuacao}", True, (255, 255, 255))
        texto3 = fonte.render("Pressione [ESPACO] para jogar de novo", True, (200, 200, 200))
        texto4 = fonte.render("ou [ESC] para sair", True, (200, 200, 200))
        janela.blit(texto1, (100, 200))
        janela.blit(texto2, (150, 260))
        janela.blit(texto3, (25, 320))
        janela.blit(texto4, (120, 360))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogo()  # Reinicia o jogo
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# --- Início ---
jogo()
