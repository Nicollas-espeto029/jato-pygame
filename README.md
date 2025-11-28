🚀 Jogo de Nave – Pygame

Um jogo simples no estilo arcade desenvolvido em Python + Pygame, onde você controla um jato e precisa desviar de tiros inimigos, acumulando pontos e tentando superar o seu próprio recorde (highscore).
__________

📸 Visão Geral do Projeto

Este projeto utiliza:

Sprites e imagens armazenadas em /images

Efeitos sonoros e música em /SFX

Sistema de highscore salvo no arquivo highscore.txt
__________

🛠️ Tecnologias Utilizadas

Python 3.13+

Pygame

Manipulação de arquivos (para salvar highscore)

pathlib para gerenciamento seguro de diretórios

Ambiente virtual (venv)
__________

📁 Estrutura do Projeto
project/
│── images/
│── SFX/
│── venv/
│── highscore.txt
└── teste_pygame.py
__________

▶️ Como Executar o Projeto
1. Criar o ambiente virtual (opcional, mas recomendado)
python -m venv venv

2. Ativar o ambiente virtual

Windows:

venv\Scripts\activate


Linux/Mac:

source venv/bin/activate

3. Instalar as dependências
pip install pygame

4. Executar o jogo
python teste_pygame.py
__________

🎮 Funcionalidades do Jogo

Controle de um jato pelo jogador

Movimentação aleatória dos tiros inimigos

Sistema de pontuação baseado em sobrevivência

Highscore salvo automaticamente em arquivo

Música de fundo e efeitos sonoros

FPS estável a 60
__________

📦 Assets

Imagens do jato e inimigos: images/

Efeitos sonoros e música: SFX/

Highscore persistente: highscore.txt
__________

💡 Melhorias Futuras

Adicionar animações de explosão

Criar menu inicial (Start / Exit)

Implementar power-ups

Criar novos tipos de inimigos

Adicionar ranking com vários jogadores
__________

✨ Autor

Desenvolvido por Nicollas De Oliveira Micossi.
