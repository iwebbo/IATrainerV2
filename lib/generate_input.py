from crewai import Agent, Task, Crew
from langchain.chat_models import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = "NA"

# ✅ Connexion à Ollama (Mistral ou autre modèle LLM)
llm = ChatOpenAI(
    model="mistral",
    base_url="http://localhost:11434/v1"
)
# 🔹 Création de l'agent qui génère des phrases naturelles
phrase_generator_agent = Agent(
    name="Phrase Generator",
    role="Expert en NLP",
    goal="Générer des phrases pertinentes et naturelles pour la recherche en fonction de mots-clés.",
    backstory="Un modèle LLM avancé entraîné pour produire des requêtes optimisées pour le web scraping et la recherche documentaire.",
    verbose=True,
     llm=llm
)

# 🔹 Tâche pour l’agent : générer des phrases basées sur un ou deux mots-clés
def generate_search_phrases(mot_cle1, mot_cle2=None, nombre=5):
    """Lance l'agent CrewAI pour générer des phrases de recherche pertinentes"""
    
    keywords = f"{mot_cle1}" if not mot_cle2 else f"{mot_cle1} et {mot_cle2}"

    task = Task(
        description=(
            f"À partir des mots-clés '{keywords}', génère {nombre} phrases "
            "naturelles et pertinentes pour une recherche web ou un scraping d'information."
            "Retourne les phrases sous forme d'une liste numérotée, séparée par des sauts de ligne."
        ),
        agent=phrase_generator_agent,
    )

    # Création de l'équipe avec une seule tâche
    crew = Crew(agents=[phrase_generator_agent], tasks=[task])
    result = crew.kickoff()  # Lancement de la génération via CrewAI

    # Vérifie si le résultat est bien une chaîne de texte et le découpe en lignes
    if isinstance(result, str):
        phrases = result.strip().split("\n")  # Découpe les phrases par ligne
        return [phrase.strip("-. ") for phrase in phrases if phrase.strip()]  # Nettoie les caractères spéciaux
    
    return [result]  # Au cas où le LLM retourne autre chose

def save_phrases_to_file(phrases, filename="inputs.txt"):
    """Sauvegarde les phrases générées dans un fichier texte"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for phrase in phrases:
                file.write(f"{phrase}\n")
        print(f"Wordlist save to '{filename}'")
        return True
    except Exception as e:
        print(f"Issue with save file: {e}")
        return False


if __name__ == "__main__":
    # Demande les mots-clés à l'utilisateur
    mot_cle1 = input("Enter first keyword : ").strip()
    mot_cle2 = input("Enter second keyword(optional) : ").strip() or None

    # Génération des phrases via CrewAI
    phrases = generate_search_phrases(mot_cle1, mot_cle2, nombre=20)

    # Affichage des phrases générées
    print("Keyword list generated :")
    for phrase in phrases:
        print(f"- {phrase}")

    save_phrases_to_file(phrases)
        # Add to input tkt dans lib :OK 
        # add generate from AgentIA prompt research to main2.py : OK 
        # test input generate + recherche : OK 
        # voir comment créer un front à partir de la 
