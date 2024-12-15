def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except LangDetectException as e:
        print(f"Language detection error: {e}")
        return ""

def translate_text_file(input_text, dest_language, src_lang):
    try:
        # detected_lang = src_lang 
        # if(detect_language != src_language):
        #         detected_lang = detect_language(input_text)

        translated = GoogleTranslator(source=src_lang, target=dest_language).translate(input_text)
        print(translated)
        return translated, src_lang
    except Exception as e:
        print(f"An error occurred: {e}")
    return "", ""
