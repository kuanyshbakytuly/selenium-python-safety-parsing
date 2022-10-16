import urllib
from selenium import webdriver
from google.cloud import speech_v1p1beta1 as speech
import tensorflow as tf
import numpy as np
import pandas as pd

from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import imagenet_utils


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


class Prediction_Images:
    '''bypassing CAPTCHA with predicting images'''
    def __init__(self, driver):
        self.driver = driver

    def clicking_captcha(self):
        captcha = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[1]/div/div/span/div[4]')
        captcha.click()

    def neccessary_thing(self):
        '''the needed object'''
        word = self.driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[1]/div[1]/div/strong')
        return word.text()

    def installing_image(self):
        '''saving image in local'''
        img = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div/table/tbody/tr[2]/td[2]/div/div[1]/img')
        src = img.get_attribute('src')
        name_src = 'image.png'
        urllib.urlretrieve(src, name_src)
        return name_src

    def results(self, image):
        '''cutting image to 3x3 matrix and predicting'''
        im = cv2.imread(image)
        im = cv2.resize(im, (1000, 500))
        height, width, z = im.shape
        h_3 = height // 3
        w_3 = width // 3
        i, j = 0, 0
        for y in range(0, height, h_3):
            i += 1
            for x in range(0, width, w_3):
                j += 1
                y1 = y + h_3
                x1 = x + w_3
                tiles = im[y:y + h_3, x:x + w_3]
                if self.predicting(tiles):
                    return self.clicking(i, j)


    def predicting(self, piece_image):
        '''predicting image via Tensorflow'''
        img = image.load_img(filename, target_size=(224, 224))

        resized_img = image.img_to_array(img)
        final_image = np.expand_dims(resized_img, axis=0)

        mobile = tf.keras.applications.mobilenet.MobileNet() #deep_learninn_mobilenet
        final_image_1 = tf.keras.applications.mobilenet.preprocess_input(final_image)

        predictions_1 = mobile.predict(final_image_1)

        res = imagenet_utils.decode_predictions(predictions_1) #1
        word = self.neccessary_thing()
        return res[0][0][1] == word

    def clicking(self, *coord):
        '''buttoning with coordingates'''
        x, y = coord
        return self.driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div[2]/div/table/tbody/tr[{i}]/td[{j}]')
