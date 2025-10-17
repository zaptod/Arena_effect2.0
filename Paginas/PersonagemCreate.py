"""
Criador de Personagens
Interface para criar novos personagens
"""
import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bases_de_dados.Banco_de_dados_personagens import personagens_db
from bases_de_dados.Banco_de_dados_comportamentais import comportamentos_db

def criar_personagem_popup(screen, fonts=None):
	"""Popup para criar novo personagem"""
	# Usa fonts fornecido ou cria padrão
	if fonts is None:
		font = pygame.font.SysFont(None, 28)
		font_small = pygame.font.SysFont(None, 20)
	else:
		font = fonts.get('medium', pygame.font.SysFont(None, 28))
		font_small = fonts.get('small', pygame.font.SysFont(None, 20))
	
	clock = pygame.time.Clock()
	popup = pygame.Surface((500, 500))
	attr_names = ['nome', 'tamanho', 'velocidade', 'massa', 'cor']
	attr_values = {'nome': '', 'tamanho': 20, 'velocidade': 3, 'massa': 5, 'cor': (0,255,0)}
	selected_attr = 0
	selected_comps = set()
	running_popup = True
	popup_x, popup_y = 150, 50
	input_active = False
	input_text = ''
	
	while running_popup:
		popup.fill((60,60,80))
		popup.blit(font.render('Criar Novo Personagem', True, (255,255,255)), (140, 20))
		
		# Atributos
		for i, attr in enumerate(attr_names):
			value = attr_values[attr]
			y = 70 + i*40
			color = (255,255,0) if i == selected_attr else (255,255,255)
			
			if input_active and i == selected_attr and attr == 'nome':
				txt = font.render(f"{attr}: {input_text}|", True, color)
			else:
				txt = font.render(f"{attr}: {value}", True, color)
			popup.blit(txt, (50, y))
		
		# Comportamentos
		popup.blit(font.render('Comportamentos:', True, (255,255,255)), (50, 300))
		for j, comp in enumerate(comportamentos_db):
			y = 340 + j*30
			sel = comp['id'] in selected_comps
			color = (0,200,0) if sel else (200,200,200)
			txt = font_small.render(f"{comp['nome']}", True, color)
			popup.blit(txt, (70, y))
		
		# Botão confirmar (desenha no popup)
		btn_confirm_local = pygame.Rect(180, 450, 140, 30)
		pygame.draw.rect(popup, (70,130,180), btn_confirm_local)
		popup.blit(font.render('Salvar', True, (255,255,255)), (btn_confirm_local.x+30, btn_confirm_local.y+5))
		
		# Botão real na tela para detectar clique
		btn_confirm = pygame.Rect(popup_x+180, popup_y+450, 140, 30)
		
		screen.blit(popup, (popup_x, popup_y))
		pygame.display.flip()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running_popup = False
			elif event.type == pygame.KEYDOWN:
				if input_active:
					if event.key == pygame.K_RETURN:
						attr_values['nome'] = input_text
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
						if isinstance(attr_values[attr], int):
							attr_values[attr] += 1
					elif event.key == pygame.K_LEFT:
						attr = attr_names[selected_attr]
						if isinstance(attr_values[attr], int):
							attr_values[attr] = max(1, attr_values[attr] - 1)
					elif event.key == pygame.K_RETURN and attr_names[selected_attr] == 'nome':
						input_active = True
						input_text = str(attr_values.get('nome', ''))
					elif event.key == pygame.K_ESCAPE:
						running_popup = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# Clique nos comportamentos
				for j, comp in enumerate(comportamentos_db):
					y = 340 + j*30
					rect_comp = pygame.Rect(popup_x+70, popup_y+y, 200, 28)
					if rect_comp.collidepoint(event.pos):
						if comp['id'] in selected_comps:
							selected_comps.remove(comp['id'])
						else:
							selected_comps.add(comp['id'])
				
				# Botão salvar
				if btn_confirm.collidepoint(event.pos):
					# Verifica arquivos na pasta personagens para encontrar IDs existentes
					personagens_dir = os.path.join(os.path.dirname(__file__), '..', 'personagens')
					ids_existentes = set()
					
					if os.path.exists(personagens_dir):
						for filename in os.listdir(personagens_dir):
							if filename.startswith('personagem') and filename.endswith('.py'):
								try:
									num = int(filename.replace('personagem', '').replace('.py', ''))
									ids_existentes.add(num)
								except ValueError:
									pass
					
					# Procura o primeiro ID disponível (reutiliza IDs de personagens deletados)
					novo_id = 1
					while novo_id in ids_existentes:
						novo_id += 1
					
					nome_arquivo = f"personagem{novo_id}.py"
					caminho = os.path.join(os.path.dirname(__file__), '..', 'personagens', nome_arquivo)
					cor_valor = attr_values['cor']
					
					# Garante que cor seja sempre uma tupla de inteiros
					if isinstance(cor_valor, str):
						try:
							cor_valor = tuple(map(int, cor_valor.strip('()').split(',')))
						except Exception:
							cor_valor = (0, 255, 0)
					elif not isinstance(cor_valor, tuple):
						cor_valor = (0, 255, 0)
					
					# Código do personagem (usando concatenação para evitar problemas com aspas triplas)
					personagem_code = f"""import pygame

class Personagem:
    def __init__(self, nome, id, tamanho, velocidade, massa, cor, comportamentos, x, y):
        self.nome = {repr(attr_values['nome'])}
        self.id = id
        self.tamanho = {attr_values['tamanho']}
        self.velocidade = {attr_values['velocidade']}
        self.massa = {attr_values['massa']}
        self.cor = {repr(cor_valor)}
        self.forca = velocidade * massa
        self.comportamentos = comportamentos
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.vida_maxima = 100
        self.vida_atual = 100
        self.vivo = True
    
    def receber_dano(self, dano):
        if self.vivo:
            self.vida_atual -= dano
            if self.vida_atual <= 0:
                self.vida_atual = 0
                self.vivo = False
        return self.vivo
    
    def curar(self, quantidade):
        if self.vivo:
            self.vida_atual = min(self.vida_atual + quantidade, self.vida_maxima)
    
    def update(self):
        pass
    
    def draw(self, screen):
        if self.vivo:
            pygame.draw.circle(screen, self.cor, (int(self.x), int(self.y)), self.tamanho)
    
    def check_collision(self, other):
        dist = ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
        return dist < self.tamanho + other.tamanho
    
    def handle_collision(self, other):
        pass
    
    def check_wall_collision(self):
        pass

def criar_personagem(personagem_id, x, y):
    return Personagem(
        nome={repr(attr_values['nome'])},
        id={novo_id},
        tamanho={attr_values['tamanho']},
        velocidade={attr_values['velocidade']},
        massa={attr_values['massa']},
        cor={repr(cor_valor)},
        comportamentos={list(selected_comps)},
        x=x,
        y=y
    )
"""
					
					try:
						# Cria a pasta personagens se não existir
						os.makedirs(os.path.dirname(caminho), exist_ok=True)
						
						# Salva o arquivo
						with open(caminho, 'w', encoding='utf-8') as f:
							f.write(personagem_code)
						
						# Atualiza o banco de dados
						novo_personagem = {
							'id': novo_id,
							'nome': attr_values['nome'],
							'ativo': True,
							'tamanho': attr_values['tamanho'],
							'velocidade': attr_values['velocidade'],
							'massa': attr_values['massa'],
							'cor': cor_valor,
							'comportamentos': list(selected_comps)
						}
						personagens_db.append(novo_personagem)
						
						print(f"✅ Personagem '{attr_values['nome']}' criado com ID {novo_id}")
						running_popup = False
					except Exception as e:
						print(f"❌ Erro ao criar personagem: {e}")
						running_popup = False
		
		clock.tick(60)
