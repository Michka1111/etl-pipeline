from ia_csv_builder.ia_csv_builder import IACSVBuilder
from singleton_registry_path import PathRegistry

def test_IACSVBuilder():
    icb = IACSVBuilder(model="deepseek-coder-v2")
    assert isinstance(icb, IACSVBuilder)
    assert icb.olm_model == "deepseek-coder-v2"
    assert icb.olm_messages == []
    assert icb.get_csv() == ""
    
    icb.csv_text = "some text"
    icb.reset()
    assert icb.get_csv() == ""
    pass

def test_start_csv_method():
    _model = "deepseek-coder-v2"
    icb = IACSVBuilder(_model)
    r = icb.start_csv( f"Bonjour, Serveur Ollama avec ton LLM local {_model}, es-tu prêt à générer des listes CSV ?")
    assert r != ""
    print(r)
    pass

def test_enrich_prompt_with_raw_sources():
    _model = "deepseek-coder-v2"
    builder = IACSVBuilder(model=_model)
    espn_url = "https://www.espn.com/nfl/scoreboard/_/week/3/year/2025/seasontype/1"
    cbs_url = "https://www.cbssports.com/nfl/scoreboard/all/2025/preseason/3/"
    # "https://www.cbssports.com/nfl/scoreboard/all/2025/preseason/3/"

    prompt = builder.enrich_prompt_with_raw_sources(espn_url, cbs_url)

    assert "ESPN" in prompt
    assert "CBS Sports" in prompt
    assert "Date, Home Team, Away Team, Score, Stadium" in prompt
    pass

def test_start_csv_method_with_enriched_prompt():
    _model = "deepseek-coder-v2"
    icb = IACSVBuilder(model=_model)
    espn_url = "https://www.espn.com/nfl/scoreboard/_/week/3/year/2025/seasontype/1"
    cbs_url = "https://www.cbssports.com/nfl/scoreboard/all/2025/preseason/3/"
    # "https://www.cbssports.com/nfl/scoreboard/all/2025/preseason/3/"#
    prompt = icb.enrich_prompt_with_raw_sources(espn_url, cbs_url)
    r = icb.start_csv(prompt)
    assert r != ""
    pass

def test_enrich_prompt_with_html_files():
    _model = "deepseek-coder-v2"
    builder = IACSVBuilder(model=_model)
    _data_in_path = PathRegistry.get_path("world_data_in_path")
    _espn_path = _data_in_path / "NFL_WEEK_ESPN.html"
    _cbs_path  = _data_in_path / "NFL_WEEK_CBSSPORT.html"

    prompt = builder.enrich_prompt_with_html_files(
        "PREWK2"
        , espn_path =_espn_path
        , cbs_path=_cbs_path
    )

    assert "ESPN" in prompt
    assert "CBS Sports" in prompt
    assert "I_NFL Season" in prompt
    assert "V_Code_NFL_Home" in prompt
    assert "Score" in prompt
    assert "Stadium" in prompt
    assert len(prompt) > 1000  # Vérifie que le prompt est bien rempli
    pass

def test_start_csv_method_with_enriched_prompt_from_html_files():
    _model = "deepseek-coder-v2"
    builder = IACSVBuilder(model=_model)
    _data_in_path = PathRegistry.get_path("world_data_in_path")
    _espn_path = _data_in_path / "NFL_WEEK_ESPN.html"
    _cbs_path  = _data_in_path / "NFL_WEEK_CBSSPORT.html"

    prompt = builder.enrich_prompt_with_html_files(
        "PREWK2"
        , espn_path =_espn_path
        , cbs_path=_cbs_path
    )

    r = builder.start_csv(prompt)

    # ASSERTIONS
    assert r != ""
    pass

