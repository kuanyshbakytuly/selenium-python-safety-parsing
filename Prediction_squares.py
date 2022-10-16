import urllib
from selenium import webdriver
from google.cloud import speech_v1p1beta1 as speech


class Prediction_speech:
    '''bypassing CAPTCHA with predicting speech'''
    def __init__(self, driver):
        self.driver = driver
        self.client = client = speech.SpeechClient.from_service_account_json('key.json')

    def installing_audio(self):

        audio = self.driver.find_element(By.XPATH, '/html/body/div/div/div[7]/a')
        src = audio.get_attribute('src')
        name_src = 'audio.mp3'
        urllib.urlretrieve(src, name_src)
        return name_src

    def predicting(self, audio):
        '''reading audiol file'''
        with open(audio, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)

        '''config for mp3 audio'''
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=44100,
            language_code="en-US",
        )
        '''response to google'''
        r = self.client.recognize(config=config, audio=audio)

        for result in r.results:
            return f"{format(result.alternatives[0].transcript)}"

    def texting(self, text):
        audio = self.installing_audio()
        text = self.predicting(audio)

        '''enter texting to check result'''
        input_text = self.driver.find_element(By.XPATH, '/html/body/div/div/div[6]/input')
        input_text.send_keys(text)

        input_text.submit()


