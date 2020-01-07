# 	File Name: faceScaffold.py
#	Author: Xiangyu
#	Email Address: xychen@ku.edu
#	Description: This is the final project for EECS 700 in fall 2019. It aims to let cozmo learn faces online assisting by human’s voice(guidance). E.g. Human: “This is Shirley.” Cozmo takes a picture of her and record her name to dataset. Then use the dataset to recognize her again when it sees her next time.
#	Last Changed: Nov. 6

#!/usr/bin/env python3

import speech_recognition as sr
import asyncio
import cozmo
import time
import cv2
import face_recognition
import numpy as np

###### COMMANDS ######
command_activate = "Cosmo"
command_learnnewface = "I'm"
command_say = "say"

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
current_name=""
name = ""


# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []
global size 
size = 0

###### ACTIONS ######
def show_face():
        new_face = cv2.imread("picture.png")
        # Display the resulting image
        cv2.imshow('faces', new_face)
        cv2.waitKey(1)
        
def get_image(robot: cozmo.robot.Robot):
         # take a record of this face
         latest_image = robot.world.latest_image
         pic_filename = "picture.png"
         latest_image.raw_image.convert('L').save(pic_filename)
        # large_frame = cv2.imread("picture.png")
         large_frame = face_recognition.load_image_file("picture.png")
         return large_frame
         
def encode_image(frame):
        face_encoding = face_recognition.face_encodings(frame)[0]
        return face_encoding
        
def new_face(current_face_encoding):
        if len(known_face_encodings)==0:
                return True
        else:
                matches = face_recognition.compare_faces(known_face_encodings, current_face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, current_face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                        current_name = known_face_names[best_match_index]
                        return False
                else: 
                        return True
                        
def old_face(current_face_encoding):
        matches = face_recognition.compare_faces(known_face_encodings, current_face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, current_face_encoding)
        best_match_index = np.argmin(face_distances)
        current_name = known_face_names[best_match_index]
        return current_name
                      
                
def add_new_face(frame):
        current_code = encode_image(frame)
        if new_face(current_code):
                known_face_encodings.append(current_code)
                

def add_new_name(name):
        known_face_names.append(name)
                
def say(recognized, robot):
	line = recognized.split(' ')[2]
	robot.say_text(line).wait_for_completed()
	print("Cozmo said: %s" % line)

def hear(source, r, robot):
	audio = r.listen(source)
	action_done = False
	try:
		recognized = r.recognize_google(audio)
		print("You said: " + recognized)
		new_name = recognized.split(' ')[0]
		#print("new_name = ")
		#print(new_name)
		#if command_activate in recognized or command_activate.lower() in recognized:
		if True:
			print("Action command recognized")

			#if command_learnnewface in recognized:
			if True:
				add_new_name(new_name) 
				print("known_face_names is as follow:")
				print(known_face_names)
				action_done = True

			elif command_say in recognized:
				say(recognized, robot)
				action_done = True

			else:
				print("Command not recognized")

		else:
			print("You did not say the magic word " + command_activate)

	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
	return action_done

                    
	
def run(robot: cozmo.robot.Robot):
        # Move lift down and tilt the head up
        robot.move_lift(-3)
        robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

        face_to_encode = None

        print("Press CTRL-C to quit")
        times = 0
        while True:
                turn_action = None
                if face_to_encode:
                        print("I got one face!")
                        #robot.say_text("I got one face!").wait_for_completed()
                     
                        current_face = get_image(robot)
                        current_encode = encode_image(current_face)
                        if not new_face(current_encode):
                                print("It is not a new face")
                                current_name = old_face(current_encode)
                                print("It's " + current_name)
                              #  print("Hi, "+ current_name)
                               # print(times)
                                if times==1 or times==5:
                                        time.sleep(3)
                                        robot.say_text("where are you from?").wait_for_completed()
                                        print("where are you from?")
                                        temp = sr.Recognizer()
                                        with sr.Microphone() as source:
                                                audio = temp.listen(source)
                                elif times ==2 or times==4 or times==7:
                                        time.sleep(3)
                                        robot.say_text(current_name).wait_for_completed()
                                      #  time.sleep(1)
                                        robot.say_text("what's your major?").wait_for_completed()
                                        print(current_name+", what's your major?")
                                        temp = sr.Recognizer()
                                        with sr.Microphone() as source:
                                                audio = temp.listen(source)
                                elif times ==3 or times==6:
                                        time.sleep(3)
                                        robot.say_text("Shirley").wait_for_completed()
                                       # time.sleep(1)
                                        robot.say_text("what's your favorite color?").wait_for_completed()
                                        print(current_name+", what's your favorite color?")
                                        temp = sr.Recognizer()
                                        with sr.Microphone() as source:
                                                audio = temp.listen(source)
                                else:
                                        robot.say_text("Thanks for participating! Have a good day!").wait_for_completed()
                                        print("Thanks for participating! Have a good day!")
                                times = times+1
                        else:
                                print("It is a new face")
                                add_new_face(current_face)
                                try:
                                        print("Hi there, I'm Cozmo. What's your name?")
                                        robot.say_text("Hi there, I'm Cozmo. What's your name?").wait_for_completed()
                                        r = sr.Recognizer()
                                        times = 1
                                        with sr.Microphone() as source:
                                                while 1:
                                                        hear_do = hear(source, r, robot)
                                                        if not hear_do:
                                                                print("Could you repeat again?")
                                                                robot.say_text("Could you repeat again?").wait_for_completed()
                                                        else:
                                                                break
                                                        recognized = None
                                except KeyboardInterrupt:
                                        print("")
                                        print("Exit requested by user")
                        turn_action = robot.turn_towards_face(face_to_encode)
                if not (face_to_encode and face_to_encode.is_visible):
                # find a visible face, timeout if nothing found after a short while
                        try:
                                face_to_encode = robot.world.wait_for_observed_face(timeout=30)
                        except asyncio.TimeoutError:
                                print("Didn't find a face - exiting!")
                                return

                if turn_action:
                        # Complete the turn action if one was in progress
                        turn_action.wait_for_completed()

                time.sleep(.1)
		
cozmo.run_program(run, use_viewer=True, force_viewer_on_top=True)

