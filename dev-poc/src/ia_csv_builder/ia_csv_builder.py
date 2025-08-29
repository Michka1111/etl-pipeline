from ollama import Client

from .extractor import RawHTMLExtractor
from .pyecs_prompt_factory import *

class IACSVBuilder:
    def __init__(self, model: str ='llama3.1', host='http://localhost:11434'):
        self.olm_client = Client(host=host)
        self.olm_model = model
        self.olm_messages = []
        self.csv_text = ""  # Dernière version du CSV généré
        self.extractor = RawHTMLExtractor()

    def start_csv(self, prompt_intro):
        self.olm_messages = [{
            "role": "user"
            , "content": prompt_intro
            # , "options": {'temperature': 0}  # Make responses more deterministic
        }]
        response = self.olm_client.chat(model=self.olm_model, messages=self.olm_messages)
        self.csv_text = response.message.content
        return self.csv_text

    def follow_up(self, prompt_followup):
        self.olm_messages.append({"role": "user", "content": prompt_followup})
        response = self.olm_client.chat(model=self.olm_model, messages=self.olm_messages)
        self.csv_text = response.message.content
        return self.csv_text

    def get_csv(self):
        return self.csv_text

    def reset(self):
        self.olm_messages = []
        self.csv_text = ""

    def enrich_prompt_with_raw_sources(self, espn_url, cbs_url):
        espn_raw = self.extractor.get_raw_text(espn_url)
        # cbs_raw = # self.extractor.get_raw_text(cbs_url)
        # Copié-collé de la sélection intéressante de la page CBSSPORT.
        cbs_raw = """
<Hahaaaa !>
"""

        prompt = f"""
Tu es un assistant expert en structuration de données NFL.

Voici les contenus bruts extraits de deux sources officielles pour la semaine PREWK2 :

🔹 ESPN :
{espn_raw}

🔹 CBS Sports :
{cbs_raw}

À partir de ces données, génère non pas un fichier mais un texte contenant la liste CSV avec les colonnes suivantes :
Date, Home Team, Away Team, Score, Stadium
"""
        return prompt

    def enrich_prompt_with_html_files(self, nfl_week_code, espn_path, cbs_path):
        # Création de l'entité pour la NFL Week traitée
        week = NFLWeek(nfl_week_code)
        # Instanciation des Systèmes PYECS
        html_loader = HTMLLoaderSystem()
        prompt_builder = PromptBuilderSystem()

        # Chargement des HTML Contents
        html_component = html_loader.load(week, espn_path, cbs_path)
        prompt_component = prompt_builder.build(html_component)
        prompt = prompt_component.prompt_text
        
        return prompt