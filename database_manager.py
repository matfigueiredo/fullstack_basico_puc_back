from sqlalchemy import create_engine, text
import logging
from typing import Union

class DatabaseManager:
    def __init__(self, database_url: str = "sqlite:///boostme.db"):        
        self.engine = create_engine(database_url, pool_recycle=3600)
        self.logger = logging.getLogger(__name__)
        
    def init_db(self):
        """Initialize database tables."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS challenge_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                challenge_id INTEGER NOT NULL,
                date DATE NOT NULL DEFAULT CURRENT_DATE,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (challenge_id) REFERENCES challenges(id)
            )
            """
        ]
        
        for query in queries:
            self.execute_query(query)
            
    def seed_db(self):
        """Populate database with initial data."""

        categories = ["Saúde", "Produtividade", "Criatividade", "Bem-estar", "Educação", 
                      "Fitness", "Desenvolvimento Pessoal", "Alimentação", "Meditação", "Leitura"]

        challenges_by_category = {
            "Saúde": [
                ("Beba mais água", "Beba pelo menos 2 litros de água ao longo do dia.", "Saúde"),
                ("Durma melhor", "Desligue todos os aparelhos eletrônicos 1 hora antes de dormir.", "Saúde"),
                ("Alongamento matinal", "Faça 10 minutos de alongamento logo ao acordar.", "Saúde"),
                ("Postura correta", "Verifique e corrija sua postura a cada hora durante o trabalho.", "Saúde"),
                ("Caminhada leve", "Faça uma caminhada de 15 minutos após o almoço.", "Saúde")
            ],
            "Produtividade": [
                ("Técnica Pomodoro", "Trabalhe por 25 minutos e descanse por 5 minutos, repetindo o ciclo.", "Produtividade"),
                ("Lista de tarefas", "Escreva suas 3 tarefas mais importantes para o dia logo pela manhã.", "Produtividade"),
                ("Zero notificações", "Desligue as notificações do celular durante 2 horas de trabalho.", "Produtividade"),
                ("Organização de e-mails", "Reserve 20 minutos para organizar sua caixa de entrada.", "Produtividade"),
                ("Planejamento semanal", "Dedique 30 minutos para planejar sua semana no domingo.", "Produtividade")
            ],
            "Criatividade": [
                ("Desenho livre", "Desenhe por 15 minutos sem julgar o resultado.", "Criatividade"),
                ("Escrita criativa", "Escreva uma história curta baseada em uma palavra aleatória.", "Criatividade"),
                ("Fotografia diária", "Tire uma foto de algo que achou interessante hoje.", "Criatividade"),
                ("Música nova", "Escute um gênero musical que você normalmente não ouve.", "Criatividade"),
                ("Brainstorming", "Anote 20 ideias para resolver um problema atual.", "Criatividade")
            ],
            "Bem-estar": [
                ("Gratidão diária", "Anote 3 coisas pelas quais você é grato hoje.", "Bem-estar"),
                ("Desconexão digital", "Fique 2 horas sem usar nenhum dispositivo eletrônico.", "Bem-estar"),
                ("Contato com a natureza", "Passe 20 minutos em um parque ou jardim.", "Bem-estar"),
                ("Autocompaixão", "Pratique falar consigo mesmo como falaria com um bom amigo.", "Bem-estar"),
                ("Respiração consciente", "Faça 10 respirações profundas quando se sentir estressado.", "Bem-estar")
            ],
            "Educação": [
                ("Aprendizado de idioma", "Estude um novo idioma por 15 minutos.", "Educação"),
                ("Documentário educativo", "Assista a um documentário sobre um tema que desconhece.", "Educação"),
                ("Leitura técnica", "Leia um artigo científico ou técnico da sua área.", "Educação"),
                ("Podcast informativo", "Ouça um podcast educativo durante o deslocamento.", "Educação"),
                ("Curso online", "Dedique 30 minutos para avançar em um curso online.", "Educação")
            ],
            "Fitness": [
                ("Treino HIIT", "Faça 15 minutos de exercícios de alta intensidade.", "Fitness"),
                ("Yoga básico", "Pratique 20 minutos de yoga seguindo um vídeo online.", "Fitness"),
                ("Agachamentos", "Realize 3 séries de 15 agachamentos ao longo do dia.", "Fitness"),
                ("Subir escadas", "Use as escadas em vez do elevador durante todo o dia.", "Fitness"),
                ("Flexões adaptadas", "Faça 3 séries de flexões (adaptadas ao seu nível).", "Fitness")
            ],
            "Desenvolvimento Pessoal": [
                ("Leitura de autoajuda", "Leia 10 páginas de um livro de desenvolvimento pessoal.", "Desenvolvimento Pessoal"),
                ("Definição de metas", "Estabeleça uma meta específica para o próximo mês.", "Desenvolvimento Pessoal"),
                ("Feedback construtivo", "Peça feedback sincero para alguém de confiança.", "Desenvolvimento Pessoal"),
                ("Habilidade nova", "Dedique 30 minutos para aprender uma nova habilidade.", "Desenvolvimento Pessoal"),
                ("Reflexão diária", "Reflita sobre seus comportamentos e decisões do dia.", "Desenvolvimento Pessoal")
            ],
            "Alimentação": [
                ("Refeição sem distrações", "Faça uma refeição sem usar celular ou assistir TV.", "Alimentação"),
                ("Experimentar alimento novo", "Inclua um alimento que nunca experimentou em sua refeição.", "Alimentação"),
                ("Preparo de marmita", "Prepare marmitas saudáveis para 3 dias da semana.", "Alimentação"),
                ("Redução de açúcar", "Substitua doces por frutas durante um dia inteiro.", "Alimentação"),
                ("Hidratação consciente", "Beba um copo de água antes de cada refeição.", "Alimentação")
            ],
            "Meditação": [
                ("Meditação guiada", "Faça 10 minutos de meditação guiada por um aplicativo.", "Meditação"),
                ("Atenção plena", "Pratique mindfulness durante uma atividade rotineira.", "Meditação"),
                ("Escaneamento corporal", "Faça um escaneamento corporal de 5 minutos antes de dormir.", "Meditação"),
                ("Meditação da manhã", "Medite por 5 minutos logo após acordar.", "Meditação"),
                ("Caminhada meditativa", "Faça uma caminhada de 15 minutos prestando atenção em cada passo.", "Meditação")
            ],
            "Leitura": [
                ("Leitura diária", "Leia 20 páginas de um livro antes de dormir.", "Leitura"),
                ("Poesia", "Leia um poema e reflita sobre seu significado.", "Leitura"),
                ("Clube do livro", "Convide amigos para discutir um livro que todos leram.", "Leitura"),
                ("Biografia inspiradora", "Comece a ler a biografia de alguém que admira.", "Leitura"),
                ("Artigo de opinião", "Leia um artigo de opinião sobre um tema atual.", "Leitura")
            ]
        }
        
        all_challenges = []
        for category_challenges in challenges_by_category.values():
            all_challenges.extend(category_challenges)
        
        for challenge in all_challenges:
            self.execute_query(
                "INSERT INTO challenges (title, description, category) VALUES (:title, :description, :category)",
                {"title": challenge[0], "description": challenge[1], "category": challenge[2]}
            )

    def query_to_dict(self, result) -> list[dict]:
        return [dict(row._mapping) for row in result]

    def execute_query(self, query, params=None, order_by=None, order_direction='ASC', limit=None, offset=None, auto_unpack=True) -> Union[list[dict], dict, bool]:
        try:
            is_select = query.strip().upper().startswith('SELECT')
            
            if is_select:
                if limit is not None:
                    query = f"{query} LIMIT {limit}"
                    
                if order_by:
                    query = f"{query} ORDER BY {order_by} {order_direction}"
                    
                if offset is not None:
                    query = f"{query} OFFSET {offset}"
                
            try:
                with self.engine.connect() as connection:
                    result = connection.execute(text(query), params or {})
                    if is_select:
                        results = self.query_to_dict(result)
                        if auto_unpack and len(results) == 1:
                            return results[0]
                        return results
                    else:
                        connection.commit()
                        return True
            except Exception as e:
                self.logger.error(f"Error executing query: {str(e)}")
                raise Exception(f"Error executing query: {str(e)}")
                
        except Exception as e:
            self.logger.error(f"Error in execute_query: {str(e)}")
            raise