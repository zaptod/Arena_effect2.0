
regras_db = {
	'gravidade': 0,  # Sem gravidade no ambiente 2D
	'friccao': 0.98,  # Fricção para desacelerar movimento
	'colisao_elastica': True,  # Colisões elásticas entre personagens
	'dano_colisao': 5,  # Dano por colisão
	'tempo_simulacao': 300,  # Tempo de simulação em segundos (0 = infinito)
	'respawn_enabled': False,  # Personagens respawnam após morte
	'limite_personagens': 10,  # Número máximo de personagens simultâneos
	'velocidade_base': 3,  # Velocidade base dos personagens
	'tamanho_arena': (800, 600),  # Dimensões da arena
	'regras_vitoria': 'ultimo_sobrevivente',  # 'ultimo_sobrevivente', 'tempo', 'pontos'
}
