from deep_translator import GoogleTranslator

def translate_text(text, target_language):
    translator = GoogleTranslator(target=target_language)
    return translator.translate(text)
