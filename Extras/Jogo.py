import os
# Configura o Pygame para rodar em segundo plano (sem janela física)
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import numpy as np
import gradio as gr
import random

# Inicializa o Pygame na memória
pygame.init()
pygame.font.init()

LARGURA, ALTURA = 400, 400
TAMANHO_BLOCO = 20
fonte = pygame.font.SysFont("Arial", 20, bold=True)
tela = pygame.Surface((LARGURA, ALTURA))

# Estado inicial do jogo
def resetar_jogo():
    global cobra, direcao, comida, pontos, game_over
    # Começa no centro
    cobra = [[200, 200], [180, 200], [160, 200]]
    direcao = "Direita"
    comida = gerar_comida(cobra)
    pontos = 0
    game_over = False

def gerar_comida(corpo_cobra):
    while True:
        x = random.randint(0, (LARGURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
        y = random.randint(0, (ALTURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
        if [x, y] not in corpo_cobra:
            return [x, y]

# Inicializa as variáveis globais do jogo
resetar_jogo()

def renderizar_jogo():
    """Desenha o estado atual do jogo e retorna como uma imagem NumPy"""
    # Fundo azul escuro
    tela.fill((30, 30, 50))

    if game_over:
        # Tela de Game Over
        texto_go = fonte.render("GAME OVER!", True, (255, 50, 50))
        texto_score = fonte.render(f"Pontos Finais: {pontos}", True, (255, 255, 255))
        tela.blit(texto_go, (LARGURA // 2 - texto_go.get_width() // 2, ALTURA // 2 - 30))
        tela.blit(texto_score, (LARGURA // 2 - texto_score.get_width() // 2, ALTURA // 2 + 10))
    else:
        # Desenha a Comida (Vermelha)
        pygame.draw.rect(tela, (255, 50, 50), (comida[0], comida[1], TAMANHO_BLOCO, TAMANHO_BLOCO))

        # Desenha a Cobra (Verde)
        for i, bloco in enumerate(cobra):
            # Cabeça um pouco mais clara que o corpo
            cor = (0, 255, 100) if i == 0 else (0, 200, 80)
            pygame.draw.rect(tela, cor, (bloco[0], bloco[1], TAMANHO_BLOCO, TAMANHO_BLOCO))

        # Desenha a Pontuação no canto superior esquerdo
        texto_pontos = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
        tela.blit(texto_pontos, (10, 10))

    # Converte a superfície do Pygame para o formato de imagem do Gradio
    frame = pygame.surfarray.array3d(tela)
    frame = np.transpose(frame, (1, 0, 2))
    return frame

def mover(comando):
    """Atualiza a lógica do Pygame com base no botão clicado"""
    global cobra, direcao, comida, pontos, game_over

    if game_over:
        return renderizar_jogo()

    # Previne que a cobra dê uma volta de 180° sobre si mesma
    opostos = {"Cima": "Baixo", "Baixo": "Cima", "Esquerda": "Direita", "Direita": "Esquerda"}
    if comando != opostos.get(direcao):
        direcao = comando

    # Calcula a nova posição da cabeça
    cabeca_x, cabeca_y = cobra[0]
    if direcao == "Cima":
        cabeca_y -= TAMANHO_BLOCO
    elif direcao == "Baixo":
        cabeca_y += TAMANHO_BLOCO
    elif direcao == "Esquerda":
        cabeca_x -= TAMANHO_BLOCO
    elif direcao == "Direita":
        cabeca_x += TAMANHO_BLOCO

    nova_cabeca = [cabeca_x, cabeca_y]

    # Colisão com as bordas da tela
    if cabeca_x < 0 or cabeca_x >= LARGURA or cabeca_y < 0 or cabeca_y >= ALTURA:
        game_over = True
        return renderizar_jogo()

    # Colisão com o próprio corpo
    if nova_cabeca in cobra:
        game_over = True
        return renderizar_jogo()

    # Move a cobra inserindo a nova cabeça
    cobra.insert(0, nova_cabeca)

    # Verifica se comeu a fruta
    if nova_cabeca == comida:
        pontos += 1
        comida = gerar_comida(cobra)
    else:
        # Se não comeu, remove a cauda para manter o tamanho
        cobra.pop()

    return renderizar_jogo()

def reiniciar():
    """Reseta o jogo e devolve o frame inicial"""
    resetar_jogo()
    return renderizar_jogo()

# --- Configuração da Interface Gráfica do Gradio ---
with gr.Blocks() as app:
    gr.Markdown("# Jogo da Cobrinha com Pygame + Gradio 🐍")
    gr.Markdown("Clique nos botões de direção para mover a cobra e pegar as frutas.")

    with gr.Row():
        # Exibe a imagem gerada pelo Pygame
        tela_imagem = gr.Image(value=renderizar_jogo(), label="Tela do Jogo")

        # Painel de controle
        with gr.Column():
            gr.Markdown("### Controles")
            btn_cima = gr.Button("⬆️ Cima")
            with gr.Row():
                btn_esq = gr.Button("⬅️ Esquerda")
                btn_dir = gr.Button("➡️ Direita")
            btn_baixo = gr.Button("⬇️ Baixo")
            
            gr.Markdown("---")
            btn_reiniciar = gr.Button("🔄 Reiniciar Jogo", variant="primary")

    # Mapeia os cliques dos botões para a lógica de jogo
    btn_cima.click(fn=mover, inputs=gr.State("Cima"), outputs=tela_imagem)
    btn_baixo.click(fn=mover, inputs=gr.State("Baixo"), outputs=tela_imagem)
    btn_esq.click(fn=mover, inputs=gr.State("Esquerda"), outputs=tela_imagem)
    btn_dir.click(fn=mover, inputs=gr.State("Direita"), outputs=tela_imagem)
    btn_reiniciar.click(fn=reiniciar, inputs=None, outputs=tela_imagem)

# Inicia a aplicação
app.launch(share=True)