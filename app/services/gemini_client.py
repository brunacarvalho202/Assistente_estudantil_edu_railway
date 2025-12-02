import google.generativeai as genai

class GeminiClient:
    def __init__(self, api_key: str, model: str):
        genai.configure(api_key=api_key)
        self.model_name = model
        self.model = genai.GenerativeModel(model)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text or ""
