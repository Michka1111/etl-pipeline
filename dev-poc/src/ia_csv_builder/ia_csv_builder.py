from ollama import Client

class IACSVBuilder:
    def __init__(self, model: str ='llama3.1', host='http://localhost:11434'):
        self.olm_client = Client(host=host)
        self.olm_model = model
        self.olm_messages = []
        self.csv_text = ""  # Dernière version du CSV généré

    def start_csv(self, prompt_intro):
        self.olm_messages = [{
            "role": "user"
            , "content": prompt_intro}]
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
