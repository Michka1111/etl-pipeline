from ..ia_csv_builder import IACSVBuilder

def test_IACSVBuilder():
    icb = IACSVBuilder()
    assert isinstance(icb, IACSVBuilder)
    assert icb.olm_model == "llama3.1"
    assert icb.olm_messages == []
    assert icb.get_csv() == ""
    
    icb.csv_text = "some text"
    icb.reset()
    assert icb.get_csv() == ""
    pass

def test_start_csv_method():
    icb = IACSVBuilder()
    r = icb.start_csv( "Bonjour, Serveur Ollama avec ton LLM local Llama3.1, es-tu prêt à générer des listes CSV ?")
    assert r != ""
    pass