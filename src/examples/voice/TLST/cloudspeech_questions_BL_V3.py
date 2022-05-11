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

    prompt_name = 'First name, middle name, or last name? Or Allergies or history of heart disease?'
    prompt_name_first = 'What is your first name?'
    prompt_name_middle = 'What is your middle name?'
    prompt_name_last = 'What is your last name?'
    prompt_allergies = 'Do you have a history of allergies?'
    prompt_heart_disease = 'Do you have a history of heart disease?'
    name_firstTXT = ''
    name_middleTXT = ''
    name_lastTXT = ''
    allergies_TXT = ''
    heart_diseaseTXT = ''

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    with Board() as board:
        aiy.voice.tts.say(prompt_name)
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

            text = text.lower()

            if 'turn on the light' in text:
                board.led.state = Led.ON

            elif 'goodbye' in text:
                break

            elif 'turn off the light' in text:
                board.led.state = Led.OFF

            elif 'blink the light' in text:
                board.led.state = Led.BLINK

            elif 'First name' in text:
                board.led.state = Led.BLINK
                logging.info('You said First name')
                text = ''
                aiy.voice.tts.say(prompt_name_first)
                name_firstTXT = client.recognize(language_code=args.language)
                aiy.voice.tts.say(name_firstTXT)
                print(name_firstTXT)
                logging.info('You said your first name')

            elif 'Middle name' in text:
                board.led.state = Led.BLINK
                logging.info('You said Middle name')
                text = ''
                aiy.voice.tts.say(prompt_name_middle)
                name_middleTXT = client.recognize(language_code=args.language)
                aiy.voice.tts.say(name_middleTXT)
                print(name_middleTXT)
                logging.info('You said your middle name')

            elif 'Last name' in text:
                board.led.state = Led.BLINK
                logging.info('You said Last name')
                text= ''
                aiy.voice.tts.say(prompt_name_last)
                name_lastTXT = client.recognize(language_code=args.language)
                aiy.voice.tts.say(name_lastTXT)
                print(name_lastTXT)
                logging.info('You said your last name')
                
            elif 'Allergies' in text:
                board.led.state = Led.BLINK
                logging.info('You said Allergies')
                text= ''
                aiy.voice.tts.say(prompt_allergies)
                name_lastTXT = client.recognize(language_code=args.language)
                aiy.voice.tts.say(allergies_TXT)
                print(allergies_TXT)
                logging.info('You said your allergies')                

            elif 'history of Heart disease' in text:
                board.led.state = Led.BLINK
                logging.info('You said history of heart disease')
                text= ''
                aiy.voice.tts.say(prompt_heart_disease)
                name_lastTXT = client.recognize(language_code=args.language)
                aiy.voice.tts.say(allergies_TXT)
                print(heart_diseaseTXT)
                logging.info('You said your history of heart disease')
                continue
    
if __name__ == '__main__':
    main()
