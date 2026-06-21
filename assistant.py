from deep_translator import GoogleTranslator
from groq import Groq
import json
import os
from dotenv import load_dotenv
from rag_v2 import get_relevant_schemes

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class FarmerAssistant:
    def __init__(self):
        self.name = "Second Brain OS"
        self.language = "Kannada"
        self.schemes = json.load(open("schemes.json", "r"))

    def __str__(self):
        return f"I am {self.name}, your digital assistant. I speak in {self.language}"

    def translate_to_english(self, kannada_text):
        english_text = GoogleTranslator(source="kn", target="en").translate(kannada_text)
        return english_text

    def translate_to_kannada(self, english_text):
        kannada_text = GoogleTranslator(source="en", target="kn").translate(english_text)
        return kannada_text

    def ask_llama(self, english_text):
        relevant_scheme = get_relevant_schemes(english_text)
        message = [
            {
                "role": "user",
                "content": f"""You are an assistant helping Indian farmers.
Here is the government scheme data:
{relevant_scheme}

Based only on this data, answer this farmer question in simple English:
{english_text}"""
            }
        ]
        try:
            response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=message)
            answer = response.choices[0].message.content
        except:
            answer = "Sorry for the inconvenience, we will fix the problem soon!"
        return answer

    def greet(self):
        print(f"Welcome to {self.name}. Ask your farming question in {self.language}.")

    def count_schemes(self):
        print(len(self.schemes))

    def show_schemes(self):
        for key in self.schemes:
            print(key)

    def get_scheme_details(self, scheme):
        print(self.schemes[scheme]["benefit"])
        print(self.schemes[scheme]["eligibility"])
        print(self.schemes[scheme]["how_to_apply"])
        print(self.schemes[scheme]["documents"])

    def search_scheme(self, keyword):
        for key in self.schemes:
            if keyword.lower() in key.lower():
                print(key)

    def run(self):
        while True:
            farmer_question = input("Type your question here: ").strip().lower()
            if farmer_question == "quit":
                break
            english_answer = self.translate_to_english(farmer_question)
            llama_response = self.ask_llama(english_answer)
            kannada_answer = self.translate_to_kannada(llama_response)
            print(kannada_answer)



class VoiceFarmerAssistant(FarmerAssistant):
    def __init__(self):
        super().__init__()
        self.voice_language = "Kannada"
        
    def receive_voice_input(self):
        print("Listening for voice input in Kannada...")

    def show_voice_language(self):
        print(f"This assistant operates in {self.voice_language}")

    def voice_greet(self):
        super().greet()
        print(f"Namaskara! I am {self.name}. I will assist you in {self.voice_language}.")


    def run(self):
       print("Voice run mode started.")
       super().run()

    def __str__(self):
         return super().__str__() + " Voice mode is enabled."
                
if __name__ == '__main__':
    voice_assistant = VoiceFarmerAssistant()
    voice_assistant.run()