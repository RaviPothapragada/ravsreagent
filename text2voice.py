import pyttsx3

def text_to_voice(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Example usage
text_to_voice('Hello, this is a text to voice conversion.')