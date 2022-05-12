#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""
import argparse
import locale
import logging
import aiy.voice.tts

from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient


def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('turn on the light',
                'turn off the light',
                'blink the light',
                'goodbye',
		'repeat after me')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    prompt_unit = 'Imperial or Metric'
    prompt_height_imp = 'Please say your height in inches as a whole number'
    prompt_height_met = 'Please say your height in meters in decimals'
    prompt_weight_imp = 'Please say your weight in pounds as a whole number'
    prompt_weight_met = 'Please say your weight in kilograms'
    heightMetTXT = ''
    heightImpTXT = ''
    weightMetTXT = ''
    weightImpTXT = ''
    bmiTXT = ''
    Under = 'You are underweight'
    Normal = 'You have a normal weight'
    Over = 'You are overweight'
    Obese = 'You are obese'

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    with Board() as board:
        aiy.voice.tts.say(prompt_unit)
        while True:
            if hints:
                logging.info('Say something, e.g. %s.' % ', '.join(hints))
            else:
                logging.info('Say something.')

            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)

            if text:
                aiy.voice.tts.say(text)

            if text is None:
                logging.info('You said nothing.')
                continue

            logging.info('You said: "%s"' % text)
            text = text.lower()
            if 'turn on the light' in text:
                board.led.state = Led.ON

            elif 'turn off the light' in text:
                board.led.state = Led.OFF

            elif 'blink the light' in text:
                board.led.state = Led.BLINK

            elif 'metric' in text:
                board.led.state = Led.ON
                logging.info('You said metric')
                aiy.voice.tts.say(prompt_height_met)
                heightMetTXT = client.recognize(language_code=args.language)
                aiy.voice.tts.say(heightMetTXT)
                logging.info('You said your height in meters')

            elif 'imperial' in text:
                board.led.state = Led.BLINK
                logging.info('You said imperial')
                aiy.voice.tts.say(prompt_height_imp)
                heightImpTXT = client.recognize(language_code=args.language)
                aiy.voice.tts.say(heightImpTXT)
                HeightINT = int(heightImpTXT)
                print(HeightINT)
                print(type(HeightINT))
                logging.info('You said your height in inches')

            if HeightINT != None:
                print('is not null')
                board.led.state = Led.ON
                aiy.voice.tts.say(prompt_weight_imp)
                weightImpTXT = client.recognize(language_code=args.language)
                WeightINT = int(weightImpTXT)
                print(WeightINT)
                print(type(WeightINT))
                logging.info('You said your weight in pounds')
                bmi = (WeightINT*703)/(HeightINT*HeightINT)
                bmiTXT = str(bmi)
                continue


            BMIeval = ('Your BMI is %s.' .join(bmiTXT))
            print(BMIeval)

            aiy.voice.tts.say(BMIeval)

            if bmi <= 18.5:
                aiy.voice.tts.say(Under)

            elif bmi > 18.5 and bmi <= 25.0:
                aiy.voice.tts.say(Normal)

            elif bmi > 25.0 and bmi <= 30.0:
                aiy.voice.tts.say(Over)

            elif bmi >30.0:
                aiy.voice.tts.say(Obese)

            elif 'goodbye' in text:
                break

if __name__ == '__main__':
    main()
