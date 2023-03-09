import re
from nltk.tokenize import word_tokenize
from pydub import AudioSegment
import fleep
from gtts import gTTS
from googletrans import Translator
import speech_recognition as sr
from playsound import playsound
from flask import Flask, redirect
from flask import request
from flask import Response
from flask_cors import CORS
from flask import send_file
from pprint import pprint
import json
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
app = Flask(__name__)
CORS(app)
langList= ('afrikaans', 'af', 'albanian', 'sq',
       'amharic', 'am', 'arabic', 'ar',
       'armenian', 'hy', 'azerbaijani', 'az',
       'basque', 'eu', 'belarusian', 'be',
       'bengali', 'bn', 'bosnian', 'bs', 'bulgarian',
       'bg', 'catalan', 'ca', 'cebuano',
       'ceb', 'chichewa', 'ny', 'chinese (simplified)',
       'zh-cn', 'chinese (traditional)',
       'zh-tw', 'corsican', 'co', 'croatian', 'hr',
       'czech', 'cs', 'danish', 'da', 'dutch',
       'nl', 'english', 'en', 'esperanto', 'eo',
       'estonian', 'et', 'filipino', 'tl', 'finnish',
       'fi', 'french', 'fr', 'frisian', 'fy', 'galician',
       'gl', 'georgian', 'ka', 'german',
       'de', 'greek', 'el', 'gujarati', 'gu',
       'haitian creole', 'ht', 'hausa', 'ha',
       'hawaiian', 'haw', 'hebrew', 'he', 'hindi',
       'hi', 'hmong', 'hmn', 'hungarian',
       'hu', 'icelandic', 'is', 'igbo', 'ig', 'indonesian',
       'id', 'irish', 'ga', 'italian',
       'it', 'japanese', 'ja', 'javanese', 'jw',
       'kannada', 'kn', 'kazakh', 'kk', 'khmer',
       'km', 'korean', 'ko', 'kurdish (kurmanji)',
       'ku', 'kyrgyz', 'ky', 'lao', 'lo',
       'latin', 'la', 'latvian', 'lv', 'lithuanian',
       'lt', 'luxembourgish', 'lb',
       'macedonian', 'mk', 'malagasy', 'mg', 'malay',
       'ms', 'malayalam', 'ml', 'maltese',
       'mt', 'maori', 'mi', 'marathi', 'mr', 'mongolian',
       'mn', 'myanmar (burmese)', 'my',
       'nepali', 'ne', 'norwegian', 'no', 'odia', 'or',
       'pashto', 'ps', 'persian', 'fa',
       'polish', 'pl', 'portuguese', 'pt', 'punjabi',
       'pa', 'romanian', 'ro', 'russian',
       'ru', 'samoan', 'sm', 'scots gaelic', 'gd',
       'serbian', 'sr', 'sesotho', 'st',
       'shona', 'sn', 'sindhi', 'sd', 'sinhala', 'si',
       'slovak', 'sk', 'slovenian', 'sl',
       'somali', 'so', 'spanish', 'es', 'sundanese',
       'su', 'swahili', 'sw', 'swedish',
       'sv', 'tajik', 'tg', 'tamil', 'ta', 'telugu',
       'te', 'thai', 'th', 'turkish',
       'tr', 'ukrainian', 'uk', 'urdu', 'ur', 'uyghur',
       'ug', 'uzbek', 'uz',
       'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh',
       'yiddish', 'yi', 'yoruba',
       'yo', 'zulu', 'zu')
dic = {"suhan": {"name": "Suhaan Parvez", "contact_no": "5842136845", "UPI_ID": "suhaan@paytm", "bank_name": "SBI"},
       "anand": {"name": "Anand Bachker", "contact_no": "4856974256", "UPI_ID": "anand@paytm", "bank_name": "PNB"}, 
       "tushar": {"name": "Tushar Singh", "contact_no": "5842136845", "UPI_ID": "tushar@paytm", "bank_name": "Axis Bank"},
       "aditya": {"name": "Aditya Kumar", "contact_no": "5842136845", "UPI_ID": "aditya@paytm", "bank_name": "SBI"}}

global units
units = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]

global tens
tens = ["", "", "twenty", "thirty", "forty",
        "fifty", "sixty", "seventy", "eighty", "ninety"]

global scales
scales = ["hundred", "thousand", "million", "billion", "trillion"]
translator = Translator()

def text2int(textnum, numwords={}):
    if not numwords:
      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):
          numwords[word] = (1, idx)
      for idx, word in enumerate(tens):
          numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):
          numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


@app.route('/setLang', methods=['POST'])
def set_lang():
    global lang
    lang = langList[langList.index(request.json['language'].lower())+1]
    print("language sucessfully set to " + lang)
    return ("language sucessfully set to " + lang)


@app.route('/transText', methods=['POST'])
def transText():
    btnDict = request.json["btn"]
    for key in btnDict:
        txt = translator.translate(btnDict[key], dest=lang)
        btnDict[key] = txt.text
    print(lang, btnDict)
    return json.dumps(btnDict)

@app.route('/transAudio', methods=['POST','GET'])
def transAudio():
    if request.method == 'POST':
        translator = Translator()
        translated = translator.translate(request.json["speak"]["text"], src='en', dest=lang)
        text_1 = translated.text
        print(text_1)
        audio = gTTS(text=text_1, lang=lang, slow=False)
        path= "./output/trans_voice.wav"
        audio.save(path)
        return json.dumps("ok")
    else:
        try:
            return send_file(
                    path,
                    mimetype="audio/wav",
                    as_attachment=True,
                    attachment_filename="trans_voice.wav")
        except Exception as e:
            return str(e)
    # return json.dumps({"asshole":"got it"})

@app.route('/audio', methods=['POST', 'GET'])
def upload_audio():
    r = sr.Recognizer()
    if request.method == 'POST':
        data = request.get_data()

        f = open("output/audio", 'wb+')
        f.write(data)
        f.close()

        with open("output/audio", "rb") as file:
            info = fleep.get(file.read(128))
        print(info.extension)
        m4a_file = 'output/audio'
        wav_filename = r"output/audio.wav"
        track = AudioSegment.from_file(m4a_file,  format='m4a')
        file_handle = track.export(wav_filename, format='wav')

        with sr.AudioFile(file_handle) as source:
            text = r.listen(source)
        try:
            text_output = r.recognize_google(text, language="en-IN")
            print('Converting speech into text ...')
            print(text_output)
            response = translator.translate(text_output)
            text = response.text.lower()
            print(text)
            input_words = list(text.split(" "))
            words = list(text.split(" "))
            rem = ["to", "rupees", "make", "of" ,*scales, *tens, *units]
            amount = -1
            action = 0
            for x in input_words:
                print(x)
                if (x.isnumeric()):
                    amount = int(x)
                    words.remove(x)
                if (x[0] == "₹"):
                    amount = int(x[1:])
                    words.remove(x)
                if (x == "pay" or x == "payment" or x == "send" or x == "transfer"):
                    action = 1
                    words.remove(x)
                if (x == "balance"):
                    action = 2
                    words.remove(x)
                if (x == "transaction" or x == "history"):
                    action = 3
                    words.remove(x)
                if x in rem:
                    words.remove(x)
            name = words[0]
            if amount == -1:
                amount = text2int(" ".join([input_words[input_words.index("rupees")-2], input_words[input_words.index("rupees")-1]]))
            if name in dic:
                acc_details = dic[name]
            else:
                acc_details = {"name": "not found", "contact_no": "not found",
                               "UPI_ID": "--", "bank_name": "--"},
            res = {"action": action, "amount": amount, "name": acc_details}
            print(res)
            return json.dumps(res)
        except:  
            text = "sorry, could'nt get that"
            print(text)
        
        return json.dumps(text)


if __name__ == "__main__":
    app.run(host=IPAddr, port=5000, debug=True)
