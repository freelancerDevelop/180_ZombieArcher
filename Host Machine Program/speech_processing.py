import speech_recognition as sr
import threading
import Queue

global audioQueue
audioQueue = Queue.Queue()
global speechValue
#Start variable at pause and change it once speech comes in
speechValue = "pause"


def speech_initialize():
	#Initialize microphone and recognizer
	global recognizer
	recognizer = sr.Recognizer()
	global mic
	mic = sr.Microphone()
	#Perform any necessary calibration
	#Calibration only needs to be done once
	with mic as source:
		recognizer.adjust_for_ambient_noise(source)
	#Sets a 2 second time limit for phrases
	recognizer.phrase_time_limit = 2
'''
def recognize():
	#Continuously recognize keywords here
	while True:
		with mic as source:
			audio = recognizer.listen(source)
		try:
		# for testing purposes, we're just using the default API key
		# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		# instead of `r.recognize_google(audio)`
			print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
			if recognizer.recognize_google(audio) == "start" or recognizer.recognize_google(audio) == "stop":
				speechValue =  recognizer.recognize_google(audio)
				print("speechValue is now " + speechValue)
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
'''

def listen():
	#Continuously listen to audio and put it on the audioQueue
	while True:
		with mic as source:
			audio = recognizer.listen(source)
			audioQueue.put(audio)
			signal.set()
			
def recognize():
	#Define signal to hold while loop when there is nothing to process
	global signal
	signal = threading.Event()
	#Define and begin thread to run listen()
	listenThread = threading.Thread(target = listen)
	listenThread.start()
	#Process all speech in Queue
	while True:
		signal.wait()
		#Get audio from queue
		audio = audioQueue.get()
		try:
		# for testing purposes, we're just using the default API key
		# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		# instead of `r.recognize_google(audio)`
			print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
			if recognizer.recognize_google(audio) == "start" or recognizer.recognize_google(audio) == "stop":
				speechValue =  recognizer.recognize_google(audio)
				print("speechValue is now " + speechValue)
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
		signal.clear()
	