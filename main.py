import speech_recognition as sr
from models import Text
from texts import TEXTS
import pyaudio
import wave
import os

TEXTS = [
    "My father was born in 1927. He was 92 years old when he passed away and had been married to my mother for sixty-three years. Even as my father got older, he was in amazing health. However, this past March, my father was unexpectedly diagnosed with terminal cancer that had begun in his lungs and had spread into his bones. "
]

def execute_record():
    r = sr.Recognizer()
    with sr.Microphone() as input:
        print("recording is in progress...")
        audio = r.listen(input)
        text = r.recognize_google(audio, language='en-EN')
        print(text)
    return text

def parse_text(text):
    parsed_text = text.split('.')
    return parsed_text

def upper_to_lower(text):
    return text.lower()

def get_today_date():
    '''
    get date today
    :return today:string year and date today
    :note returns only "date" excluding time and second
    '''
    import datetime
    today = datetime.date.today().strftime('%Y%m%d')
    return today

def init_record_setting():
    '''
    initialize the setting for rescording
    '''
    # buffer size
    CHUNK = 2**10
    # quantization bit rate 
    FORMAT = pyaudio.paInt16
    # the number of used microphones 
    CHANNELS = 1
    # the time to record(length)
    record_time = 5
    RATE = 44100
    # get ready to save the record data
    date_today = get_today_date()
    output_path =  os.path.join("recorded_voices", f'{date_today}_Example_Text')

    return {'chunk':CHUNK, 'format':FORMAT, 'channel':CHANNELS, 'record_time':record_time, 'rate':RATE }

if __name__ == '__main__':
    # execute_record()
    try:
        for text in parse_text(TEXTS[0]):
            input_text = execute_record()
            lower_input_text = upper_to_lower(input_text)
            text = upper_to_lower(text)
            print(input_text)
            print(text)
            if input_text == 'stop':
                print('Recordig stopped ...')
                break

            if lower_input_text == text:
                print("correct")
            else:
                print('false')
    except Exception as e:
        print(f'error occured: {e}')
