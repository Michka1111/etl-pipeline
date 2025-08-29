
# ENTITY
class NFLWeek:
    def __init__(self, in_week_code: str):
        self.week_code = in_week_code
        pass

    def __repr__(self):
        return f"<NFLWeek>"  # #{self.week_number}>"

# COMPONENTS
class HTMLSourcePathComponent:
    def __init__(self, in_ep, in_cp):
        self.espn_path = in_ep
        self.cbs_path  = in_cp

class HTMLSourceComponent:
    def __init__(self, espn_html_source_code: str, cbs_html_source_code: str):
        self.espn_html_src = espn_html_source_code
        self.cbs_html_src = cbs_html_source_code


class PromptComponent:
    def __init__(self, prompt_text: str):
        self.prompt_text = prompt_text

# SYSTEMS
from pathlib import Path
from bs4 import BeautifulSoup

class HTMLLoaderSystem:
    def load(self, week: NFLWeek, in_espn_path: Path, in_cbs_path: Path) -> HTMLSourceComponent:
        # Chemins génériques écrasés chaque semaine
        # _espn_path = "src/data_in/NFL_WEEK_ESPN.html"
        # _cbs_path = "src/data_in/NFL_WEEK_CBSSPORT.html"
        
        html_spc = HTMLSourcePathComponent(in_ep= in_espn_path, in_cp=in_cbs_path)
        
        _espn_path = html_spc.espn_path
        _cbs_path  = html_spc.cbs_path
        
        with open(_espn_path, 'r', encoding='utf-8') as f:
            espn_html_content = f.read()
        with open(_cbs_path, 'r', encoding='utf-8') as f:
            cbs_html_content = f.read()
            
        _html_sc = HTMLSourceComponent(espn_html_content, cbs_html_content)

        return _html_sc


class PromptBuilderSystem:
    
    def build(self, html_component: HTMLSourceComponent) -> PromptComponent:
        _espn_html_src = html_component.espn_html_src
        _cbs_html_src = html_component.cbs_html_src
        #espn_raw_text = BeautifulSoup(_espn_html_src, 'html.parser').get_text(separator='\n', strip=True)
        #cbs_raw_text = BeautifulSoup(_cbs_html_src, 'html.parser').get_text(separator='\n', strip=True)

        prompt = f"""
Tu es un assistant expert en structuration de données NFL.

Voici ci-après les contenus bruts extraits d'une des sources officielles "ESPN" pour la semaine NFL.
Indication : Dans un groupe de données de rencontre NFL, le sous-groupe de l'équipe Away est en premier.
Indication : Dans un groupe de données de rencontre NFL, le sous-groupe de l'équipe Home est en second.

🔹 ESPN (source principale) :
----
{_espn_html_src}
----

À partir de ces données, génère un fichier CSV avec les colonnes suivantes.
Liste les infos suivantes pour toutes les, et chacune des, rencontres NFL "PRESEASON WEEK 2" de la Saison NFL '2025', nom de code de Week NFL 'PREWK2', qui ont eu lieu les 16, 17, 18, 19 août 2025 :

1. 'Season' est une constante str '2025' ;
2. 'Game Day Code' est le jour où la rencontre a eu lieu au format de date 'AAAA-MM-JJ' ;
3. 'Type de rencontre' est le code de Week NFL, une constante str 'PREWK2' ;
4. 'Away Team Name' Nom d'équipe en déplacement, tel que dans la source ;
5. 'Home Team Name' Nom d'équipe à domicile, tel que lu dans la source ;
6. 'Stadium' une constante "stadium" ;
7. 'B_IsNFLI13LSeries' une constante 'false' ;
8. 'Away Team Score' score de l'équipe en déplacement, un int ;
9. 'Home Team Score' score de l'équipe à domicile, un int.

- Formater sur une seule ligne de texte par rencontre.
- Encadrer chaque info entre guillemets '"' sauf les nombres. 
- Séparer chaque info par une virgule, qu'elle soit entre guillemets ou non. 
- Ne pas indiquer le titre des infos listées, indiquer seulement les valeurs dans cet ordre.
- Respecter l'intégrité d'une ligne pour une même rencontre, les infos d'une ligne doivent concerner la même rencontre. 
- Respecter l’ordre des colonnes.

"""
        return PromptComponent(prompt)
