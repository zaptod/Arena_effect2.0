

import os
import importlib.util

agentes_db = []
agentes_dir = os.path.join(os.path.dirname(__file__), '..', 'agentes')
for filename in os.listdir(agentes_dir):
	if filename.endswith('.py'):
		filepath = os.path.join(agentes_dir, filename)
		spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
		mod = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(mod)
		# Tenta criar um agente de exemplo para o banco
		if hasattr(mod, 'criar_agente'):
			agente = mod.criar_agente(agent_id=1, x=0, y=0)
			agentes_db.append({
				'id': agente.id,
				'nome': agente.nome,
				'ativo': True,
				'tamanho': agente.tamanho,
				'velocidade': agente.velocidade,
				'massa': agente.massa,
				'cor': agente.cor,
				'comportamentos': agente.comportamentos
			})