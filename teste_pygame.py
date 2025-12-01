import pygame
import random
import sys
from pathlib import Path

pygame.init()
FPS = 60
BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "images"
HIGH_SCORE_PATH = BASE_DIR / "highscore.txt"
SFX_DIR = BASE_DIR / "SFX"
SFX_VOLUME = 1.0
BGM_VOLUME = 0.20
BGM_FILE = SFX_DIR / "naruto-battle-theme.mp3"

def init_audio():
    try:
        pygame.mixer.init()
    except Exception:
        return lambda: None
    try:
        if BGM_FILE.exists():
            try:
                pygame.mixer.music.load(str(BGM_FILE))
                pygame.mixer.music.set_volume(BGM_VOLUME)
                pygame.mixer.music.play(-1)
            except Exception:
                pass
        files = [p for p in sorted(SFX_DIR.glob("*.mp3")) if p.name.lower() != "naruto-battle-theme.mp3"]
        sounds = []
        for p in files:
            try:
                s = pygame.mixer.Sound(str(p))
                s.set_volume(SFX_VOLUME)
                sounds.append(s)
            except Exception:
                continue
        if not sounds:
            return lambda: None
        def play():
            random.choice(sounds).play()
        return play
    except Exception:
        return lambda: None

LARGURA, ALTURA = 640, 640
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🚀 Jato Desviando dos Tiros")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 28, bold=True)

fundo = pygame.image.load(str(ASSETS / "vila.jpg")).convert()
fundo = pygame.transform.smoothscale(fundo, (LARGURA, ALTURA))

img_jato = pygame.image.load(str(ASSETS / "Chaves_soq_png.png")).convert_alpha()
img_jato = pygame.transform.smoothscale(img_jato, (60, 50))

img_tiro = pygame.image.load(str(ASSETS / "sad-removebg-preview.png")).convert_alpha()
img_tiro = pygame.transform.smoothscale(img_tiro, (27, 31))

# --- Classes ---
class Jato(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_jato
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA // 2
        self.rect.bottom = ALTURA - 30
        self.velocidade = 6
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        teclas = pygame.key.get_pressed()
        boost = 4 if (teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]) else 0
        vel = self.velocidade + boost
        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= vel
        if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and self.rect.right < LARGURA:
            self.rect.x += vel
        if (teclas[pygame.K_UP] or teclas[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= vel
        if (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) and self.rect.bottom < ALTURA:
            self.rect.y += vel

class TiroInimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_tiro
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, LARGURA - self.rect.width)
        self.rect.y = -20
        self.velocidade = random.randint(4, 8)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA:
            self.kill()

# --- Função principal ---
def jogo(highscore, play_death):
    todos = pygame.sprite.Group()
    tiros_inimigos = pygame.sprite.Group()
    jogador = Jato()
    todos.add(jogador)

    pontuacao = 0
    rodando = True
    paused = False
    start_ticks = pygame.time.get_ticks()

    while rodando:
        clock.tick(FPS)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    paused = not paused
                    try:
                        if paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    except Exception:
                        pass
                if evento.key == pygame.K_ESCAPE:
                    try:
                        pygame.mixer.music.stop()
                    except Exception:
                        pass
                    pygame.quit()
                    sys.exit()

        if not paused:
            elapsed = pygame.time.get_ticks() - start_ticks
            spawn_prob = min(0.03 + pontuacao * 0.00002 + (elapsed / 100000), 0.2)
            if random.random() < spawn_prob:
                tiro = TiroInimigo()
                tiro.velocidade = min(tiro.velocidade + pontuacao // 400, 16)
                todos.add(tiro)
                tiros_inimigos.add(tiro)

        if not paused:
            todos.update()

        if not paused:
            if pygame.sprite.spritecollide(jogador, tiros_inimigos, False, pygame.sprite.collide_mask):
                try:
                    play_death()
                except Exception:
                    pass
                rodando = False

        if not paused:
            pontuacao += 1

        janela.blit(fundo, (0, 0))
        todos.draw(janela)
        texto = fonte.render(f"Pontos: {pontuacao}", True, (255, 255, 255))
        janela.blit(texto, (10, 10))
        texto_recorde = fonte.render(f"Recorde: {highscore}", True, (255, 255, 255))
        janela.blit(texto_recorde, (10, 42))
        fps_val = int(clock.get_fps())
        texto_fps = fonte.render(f"FPS: {fps_val}", True, (200, 200, 200))
        janela.blit(texto_fps, (LARGURA - 150, 10))
        if paused:
            overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            janela.blit(overlay, (0, 0))
            t1 = fonte.render("PAUSE", True, (255, 230, 0))
            t2 = fonte.render("Pressione [P] para continuar", True, (200, 200, 200))
            janela.blit(t1, (LARGURA // 2 - t1.get_width() // 2, ALTURA // 2 - 40))
            janela.blit(t2, (LARGURA // 2 - t2.get_width() // 2, ALTURA // 2))
        pygame.display.flip()

    return pontuacao

# --- Tela de Game Over ---
def tela_game_over(pontuacao, highscore):
    while True:
        janela.blit(fundo, (0, 0))
        texto1 = fonte.render("💥 GAME OVER 💥", True, (255, 70, 70))
        texto2 = fonte.render(f"Pontuação: {pontuacao}", True, (255, 255, 255))
        texto2b = fonte.render(f"Recorde: {highscore}", True, (255, 255, 255))
        texto3 = fonte.render("Pressione [ESPACO] para jogar de novo", True, (200, 200, 200))
        texto4 = fonte.render("ou [ESC] para sair", True, (200, 200, 200))
        gap = fonte.get_height() + 18
        start_y = ALTURA // 2 - int(gap * 1.8)
        cx = LARGURA // 2
        janela.blit(texto1, (cx - texto1.get_width() // 2, start_y))
        janela.blit(texto2, (cx - texto2.get_width() // 2, start_y + gap))
        janela.blit(texto2b, (cx - texto2b.get_width() // 2, start_y + gap * 2))
        janela.blit(texto3, (cx - texto3.get_width() // 2, start_y + gap * 3))
        janela.blit(texto4, (cx - texto4.get_width() // 2, start_y + gap * 4))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def load_highscore():
    try:
        with open(HIGH_SCORE_PATH, "r", encoding="utf-8") as f:
            s = f.read().strip()
            return int(s) if s else 0
    except Exception:
        return 0

def save_highscore(score):
    try:
        with open(HIGH_SCORE_PATH, "w", encoding="utf-8") as f:
            f.write(str(score))
    except Exception:
        pass

def main():
    high = load_highscore()
    play_death = init_audio()
    while True:
        pontuacao = jogo(high, play_death)
        if pontuacao > high:
            save_highscore(pontuacao)
            high = pontuacao
        reiniciar = tela_game_over(pontuacao, high)
        if not reiniciar:
            break
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
