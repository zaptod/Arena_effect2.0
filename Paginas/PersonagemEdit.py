
import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bases_de_dados.Banco_de_dados_comportamentais import comportamentos_db

def edit_personagem(personagem, screen, fonts=None):
	"""Edita um personagem existente"""
	# Se fonts não foi passado, cria fonts padrão
	if fonts is None:
		font = pygame.font.SysFont(None, 28)
	else:
		font = fonts.get('medium', pygame.font.SysFont(None, 28))
	
	clock = pygame.time.Clock()
	editing = True
	attr_names = ['nome', 'tamanho', 'velocidade', 'massa', 'cor']  # id não editável
	selected_attr = 0
	input_active = False
	input_text = ''
	while editing:
		screen.fill((50,50,70))
		for i, attr in enumerate(attr_names):
			value = personagem.get(attr, '')
			y = 50 + i*40
			color = (255,255,0) if i == selected_attr else (255,255,255)
			if input_active and i == selected_attr and attr == 'nome':
				txt = font.render(f"{attr}: {input_text}|", True, color)
			else:
				txt = font.render(f"{attr}: {value}", True, color)
			screen.blit(txt, (50, y))
		txt = font.render("Use setas cima/baixo para selecionar, esquerda/direita para alterar, Enter para editar texto. ID não editável.", True, (200,200,200))
		screen.blit(txt, (50, 300))
		screen.blit(font.render("Comportamentos:", True, (255,255,255)), (50, 350))
		for j, comp in enumerate(comportamentos_db):
			y = 380 + j*30
			sel = comp['id'] in personagem.get('comportamentos', [])
			color = (0,200,0) if sel else (200,200,200)
			txt = font.render(f"{comp['nome']}", True, color)
			screen.blit(txt, (70, y))
		# Botão Salvar
		btn_salvar = pygame.Rect(screen.get_width()//2 - 80, screen.get_height() - 70, 160, 50)
		pygame.draw.rect(screen, (70,130,180), btn_salvar)
		txt_salvar = font.render("Salvar", True, (255,255,255))
		screen.blit(txt_salvar, (btn_salvar.x+40, btn_salvar.y+10))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				editing = False
			elif event.type == pygame.KEYDOWN:
				if input_active:
					if event.key == pygame.K_RETURN:
						personagem['nome'] = input_text
						input_active = False
					elif event.key == pygame.K_BACKSPACE:
						input_text = input_text[:-1]
					elif event.key == pygame.K_ESCAPE:
						input_active = False
					else:
						if len(input_text) < 20 and event.unicode.isprintable():
							input_text += event.unicode
				else:
					if event.key == pygame.K_DOWN and selected_attr < len(attr_names)-1:
						selected_attr += 1
					elif event.key == pygame.K_UP and selected_attr > 0:
						selected_attr -= 1
					elif event.key == pygame.K_RIGHT:
						attr = attr_names[selected_attr]
						if isinstance(personagem.get(attr), int):
							personagem[attr] += 1
					elif event.key == pygame.K_LEFT:
						attr = attr_names[selected_attr]
						if isinstance(personagem.get(attr), int):
							personagem[attr] -= 1
					elif event.key == pygame.K_RETURN and attr_names[selected_attr] == 'nome':
						input_active = True
						input_text = str(personagem.get('nome', ''))
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = event.pos
				# Clique nos comportamentos
				for j, comp in enumerate(comportamentos_db):
					y = 380 + j*30
					rect = pygame.Rect(70, y, 200, 28)
					if rect.collidepoint(event.pos):
						if comp['id'] in personagem.get('comportamentos', []):
							personagem['comportamentos'].remove(comp['id'])
						else:
							personagem.setdefault('comportamentos', []).append(comp['id'])
				# Clique no botão Salvar
				if btn_salvar.collidepoint(event.pos):
					personagens_dir = os.path.join(os.path.dirname(__file__), '..', 'personagens')
					personagem_id = personagem.get('id')
					nome_arquivo = f"personagem{personagem_id}.py"
					caminho = os.path.join(personagens_dir, nome_arquivo)
					try:
						import re
						with open(caminho, 'r', encoding='utf-8') as f:
							linhas = f.readlines()
						# Coleta os valores editados
						valores = {
							'nome': personagem.get('nome',''),
							'tamanho': personagem.get('tamanho',20),
							'velocidade': personagem.get('velocidade',3),
							'massa': personagem.get('massa',5),
							'cor': personagem.get('cor',(0,255,0)),
						}
						with open(caminho, 'w', encoding='utf-8') as f:
							for linha in linhas:
								# Atualiza campos no construtor
								for campo in ['nome','tamanho','velocidade','massa','cor']:
									padrao = rf'self\.{campo}\s*=\s*.*'
									if re.search(padrao, linha):
										indent = linha[:linha.find(f'self.{campo}')]
										valor = valores[campo]
										if campo == 'cor':
											if isinstance(valor, str):
												try:
													valor = tuple(map(int, valor.strip('()').split(',')))
												except Exception:
													valor = (0, 255, 0)
										f.write(f"{indent}self.{campo} = {repr(valor)}\n")
										break
								else:
									# Atualiza argumentos na função criar_personagem
									if 'Personagem(' in linha:
										nova_linha = linha
										for campo in ['nome','tamanho','velocidade','massa','cor']:
											valor = valores[campo]
											if campo == 'cor': valor = str(valor)
											nova_linha = re.sub(rf'{campo}\s*=\s*[\"\"][^\"\"]*[\"\"]|{campo}\s*=\s*[^,\)]+', f"{campo}={repr(valor)}", nova_linha)
										f.write(nova_linha)
									else:
										f.write(linha)
					except Exception:
						pass
					# Recarrega personagens e volta para carrossel
					import Paginas.personagensP
					Paginas.personagensP.recarregar_personagens()
					editing = False
		pygame.display.flip()
		clock.tick(60)