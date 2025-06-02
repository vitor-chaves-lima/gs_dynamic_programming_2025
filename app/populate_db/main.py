import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from logic.config import get_config

import domain.model.base
import domain.model.user
import domain.model.question
import domain.model.answer
import domain.model.user_score
import domain.model.user_answer

from domain.model.question import Question
from domain.model.answer import Answer

async def add_questions():
    print("Adicionando perguntas")

    config = get_config()
    engine = create_async_engine(config.DATABASE_URL())

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        perguntas = [
            {
                "titulo": "Qual a principal causa de incêndios no Brasil?",
                "respostas": [
                    {"texto": "Raios", "correta": False},
                    {"texto": "Descuido humano", "correta": True},
                    {"texto": "Calor excessivo", "correta": False},
                    {"texto": "Animais", "correta": False}
                ]
            },
            {
                "titulo": "Como evitar incêndio em casa?",
                "respostas": [
                    {"texto": "Deixar panela no fogo", "correta": False},
                    {"texto": "Verificar gás antes de sair", "correta": True},
                    {"texto": "Usar várias extensões", "correta": False},
                    {"texto": "Deixar fósforo na cozinha", "correta": False}
                ]
            },
            {
                "titulo": "Quando é mais perigoso fazer queimadas?",
                "respostas": [
                    {"texto": "Tempo chuvoso", "correta": False},
                    {"texto": "Tempo seco com vento", "correta": True},
                    {"texto": "De madrugada", "correta": False},
                    {"texto": "No frio", "correta": False}
                ]
            },
            {
                "titulo": "Se ver fogo no mato, o que fazer?",
                "respostas": [
                    {"texto": "Tentar apagar sozinho", "correta": False},
                    {"texto": "Chamar os bombeiros", "correta": True},
                    {"texto": "Ignorar se for pequeno", "correta": False},
                    {"texto": "Jogar combustível", "correta": False}
                ]
            },
            {
                "titulo": "Como limpar terreno para evitar fogo?",
                "respostas": [
                    {"texto": "Deixar mato alto", "correta": False},
                    {"texto": "Tirar folhas secas", "correta": True},
                    {"texto": "Só plantar eucalipto", "correta": False},
                    {"texto": "Nunca cortar grama", "correta": False}
                ]
            },
            {
                "titulo": "Depois de fazer fogueira, deve:",
                "respostas": [
                    {"texto": "Deixar apagar sozinha", "correta": False},
                    {"texto": "Molhar bem as cinzas", "correta": True},
                    {"texto": "Cobrir com folhas", "correta": False},
                    {"texto": "Ir embora logo", "correta": False}
                ]
            },
            {
                "titulo": "Melhor forma de apagar fogo pequeno:",
                "respostas": [
                    {"texto": "Ventilador", "correta": False},
                    {"texto": "Água", "correta": True},
                    {"texto": "Papel", "correta": False},
                    {"texto": "Óleo", "correta": False}
                ]
            },
            {
                "titulo": "Criança pode brincar com fósforo?",
                "respostas": [
                    {"texto": "Com adulto perto", "correta": False},
                    {"texto": "Nunca", "correta": True},
                    {"texto": "Só fora de casa", "correta": False},
                    {"texto": "Só de dia", "correta": False}
                ]
            },
            {
                "titulo": "Pode queimar lixo no quintal?",
                "respostas": [
                    {"texto": "Sempre", "correta": False},
                    {"texto": "Não, é perigoso", "correta": True},
                    {"texto": "Só papel", "correta": False},
                    {"texto": "Quando chove", "correta": False}
                ]
            },
            {
                "titulo": "Por que vento é perigoso no fogo?",
                "respostas": [
                    {"texto": "Apaga o fogo", "correta": False},
                    {"texto": "Espalha mais rápido", "correta": True},
                    {"texto": "Molha tudo", "correta": False},
                    {"texto": "Não afeta", "correta": False}
                ]
            },
            {
                "titulo": "Plantas perto de churrasqueira:",
                "respostas": [
                    {"texto": "Podem ser secas", "correta": False},
                    {"texto": "Devem ficar longe", "correta": True},
                    {"texto": "Não precisam de água", "correta": False},
                    {"texto": "Só artificiais", "correta": False}
                ]
            },
            {
                "titulo": "Número para chamar bombeiros:",
                "respostas": [
                    {"texto": "190", "correta": False},
                    {"texto": "193", "correta": True},
                    {"texto": "192", "correta": False},
                    {"texto": "911", "correta": False}
                ]
            }
        ]

        try:
            for i, pergunta in enumerate(perguntas, 1):
                print(f"Inserindo pergunta {i}...")

                question = Question(
                    title=pergunta["titulo"],
                    description="Prevenção de incêndios",
                    points=1,
                    difficulty_level="easy",
                    category="queimadas"
                )

                session.add(question)

                await session.flush()

                for j, resp in enumerate(pergunta["respostas"]):
                    answer = Answer(
                        question_id=question.id,
                        text=resp["texto"],
                        is_correct=resp["correta"],
                        order_position=j + 1
                    )

                    session.add(answer)

            await session.commit()
            print(f"{len(perguntas)} perguntas adicionadas.")

        except Exception as e:
            await session.rollback()
            print(f"Erro durante a inserção: {e}")
            raise


async def main():
    print("Adicionar perguntas sobre queimadas")
    print("-" * 35)

    response = input("Confirma? (y/n): ")
    if response.lower() not in ['y', 'yes']:
        print("Cancelado.")
        return

    await add_questions()


if __name__ == "__main__":
    asyncio.run(main())
