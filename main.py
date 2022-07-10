import speech_recognition as sr
from models import Text
from texts import TEXTS
import pyaudio
import wave
import os

def execute_dictation():
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
    record_time = 3
    RATE = 44100
    # get ready to save the record data
    date_today = get_today_date()
    output_path = os.path.join("../recorded_voices", f'{date_today}.wav')

    return {'chunk':CHUNK, 'format':FORMAT, 'channel':CHANNELS, 'record_time':record_time, 'rate':RATE, 'output_path':output_path }

def record():
    # initialize the setting for recording
    init = init_record_setting()
    # create an PuyAudio instance 
    py_audio = pyaudio.PyAudio()
    # open pyaudio stream with the setting defined above
    stream = py_audio.open(format=init['format'], channels=init['channel'], rate=init['rate'],
                            input=True, frames_per_buffer=init['chunk'])
    # define an empty array 
    frames = []
    # record body
    for i in range(0, int(init['rate'] / init['chunk'] * init['record_time'])):
        data = stream.read(init['chunk'])
        frames.append(data)
    # stop streaming
    stream.stop_stream()
    stream.close()
    py_audio.terminate()
    # output as a wave file
    output_wave_file(frames=frames, pyaudio=py_audio)

def output_wave_file(frames, pyaudio):
    # initiaze the setting for recording
    init = init_record_setting()
    # open a file with writable mode
    wf = wave.open(init['output_path'], 'wb')
    # set some settings 
    wf.setnchannels(init['channel'])
    wf.setsampwidth(pyaudio.get_sample_size(init['format']))
    wf.setframerate(init['rate'])
    # write data to the wave file
    wf.writeframes(b''.join(frames))
    # end output
    wf.close()

if __name__ == '__main__':
    # execute_record()
    try:
        record_data = record()
        output_wave_file(record_data[0], record_data[1])
        # for text in parse_text(TEXTS[0]):
        #     input_text = execute_dictation()
        #     lower_input_text = upper_to_lower(input_text)
        #     text = upper_to_lower(text)
        #     print(input_text)
        #     print(text)
        #     if input_text == 'stop':
        #         print('Recordig stopped ...')
        #         break

        #     if lower_input_text == text:
        #         print("correct")
        #     else:
        #         print('false')
    except Exception as e:
        print(f'error occured: {e}')
