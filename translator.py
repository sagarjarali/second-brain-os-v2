from deep_translator import GoogleTranslator

def translate_to_english(kannada_text):
    english_text = GoogleTranslator(source="kn",target="en").translate(kannada_text)
    return english_text

def translate_to_kannada(english_text):
    kannada_text = GoogleTranslator(source="en",target="kn").translate(english_text)
    return kannada_text