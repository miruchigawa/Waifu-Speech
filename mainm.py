#!/usr/bin/python3
#import translators.server as tss
import subprocess
import requests
import speech_recognition as sr


class AudioToText:
    def __init__(self, audio_file, debug):
        self.audio_file = audio_file
        self.recognizer = sr.Recognizer()
        self.debug = debug

    def convert(self):
        try:
            with sr.AudioFile(self.audio_file) as audio:
                audio_data = self.recognizer.record(audio)
            text = self.recognizer.recognize_google(audio_data, language='id-ID')
            print(f"[Success] You say: {text}")
            return text
        except Exception as e:
            if self.debug == "y":
              print(e)
            return None
            
class MicToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def convert(self):
        try:
            with sr.Microphone() as audio:
                print("Speak now...")
                audio_data = self.recognizer.listen(audio)
            text = self.recognizer.recognize_google(audio_data, language='id-ID')
            print(f"[Success] You say: {text}")
            return text
        except:
            return None


#class TextTranslator:
#    def __init__(self, text):
#        self.text = text
#
#    def translate(self, source, target):
#        try:
#            translated_text = tss.google(self.text, source, target)
#            print(f"[Success] Translated: {translated_text}")
#            return translated_text
#        except:
#            return None
#

class TextToSpeech:
    def __init__(self, text):
        self.text = text

    def generate_audio(self, speaker_id=1):
        try:
            url = f"https://api.tts.quest/v1/voicevox/?text={self.text}&speaker={speaker_id}"
            response = requests.get(url).json()
            if response["success"] == True:
                audio_url = response["mp3DownloadUrl"]
                return audio_url
            else:
                return None
        except:
            return None

    def save_audio(self, audio_url, file_name):
        try:
            audio_content = requests.get(audio_url).content
            with open(file_name, "wb") as file:
                file.write(audio_content)
            return True
        except:
            return False


if __name__ == "__main__":
    audio_file = "assets/audio/testing.wav"
    section = int(input("Select source \n1. Audio\n2. Mic\n3. Text File(Japanese)\n: "))
    debug = input("Enable debug mode? y/n: ")
    
    if section == 1:
      # convert audio to text
      audio_to_text = AudioToText(audio_file, debug)
      text = audio_to_text.convert()
      if not text:
          print("[Failed] Failed to convert audio file to text")
          exit()
    elif section == 2:
      # convert microphone to text
      audio_to_text = MicToText()
      text = audio_to_text.convert()
      if not text:
          print("[Failed] Failed to convert audio file to text")
          exit()
    elif section == 3:
      # read text file
      f=open("text","rt")
      text = f.read()
      f.close()
    else:
      print("Invalid key.")

    if section==1 or section ==2:
        # translate text to Japanese
        text_translator = TextTranslator(text)
        translated_text = text_translator.translate("id", "ja")
        if not translated_text:
            print("[Failed] Failed to translate text")
            exit()
    elif section==3:
        translated_text = text

    # generate audio file
    text_to_speech = TextToSpeech(translated_text)
    audio_url = text_to_speech.generate_audio()
    if not audio_url:
        print("[Failed] Failed to generate audio")
        exit()

    # save audio file
    file_name = "test.mp3"
    if text_to_speech.save_audio(audio_url, file_name):
        print(f"[Success] Audio file saved as {file_name}")
    else:
        print("[Failed] Audio file not saved")
    print(translated_text)
    subprocess.run(["mpv","test.mp3"])
