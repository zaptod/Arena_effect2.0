

import os
import importlib.util

personagens_db = []
personagens_dir = os.path.join(os.path.dirname(__file__), '..', 'personagens')
for filename in os.listdir(personagens_dir):
	if filename.endswith('.py'):
		filepath = os.path.join(personagens_dir, filename)
		spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
		mod = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(mod)
		# Tenta criar um personagem de exemplo para o banco
		if hasattr(mod, 'criar_personagem'):
			personagem = mod.criar_personagem(personagem_id=1, x=0, y=0)
			personagens_db.append({
				'id': personagem.id,
				'nome': personagem.nome,
				'ativo': True,
				'tamanho': personagem.tamanho,
				'velocidade': personagem.velocidade,
				'massa': personagem.massa,
				'cor': personagem.cor,
				'comportamentos': personagem.comportamentos
			})