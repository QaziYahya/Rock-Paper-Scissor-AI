from tensorflow.keras.models import load_model
from keras.applications.mobilenet import preprocess_input
import cv2
import numpy as np
import random as rnd
import os

def Predict_Winner(playerMove, computerMove):
	
	if playerMove == computerMove:
		return "None"

	if playerMove == 0 and computerMove == 1:
		return "You"
	elif playerMove == 1 and computerMove == 2:
		return "You"
	elif playerMove == 2 and computerMove == 0:
		return "You"

	if playerMove == 1 and computerMove == 0:
		return "Computer"
	elif playerMove == 2 and computerMove == 1:
		return "Computer"
	elif playerMove == 0 and computerMove == 2:
		return "Computer"

model_path = os.path.join(os.path.dirname(__file__), 'SavedModel6')	
	
model = load_model(model_path)
cap = cv2.VideoCapture(0)
frame = None

playerMove = -1
prevMove = -1
prevComputerMove = -1
computerMove = 3
icon = None
gameStarted = False
winner = "None"

moves = ["paper", "rock", "scissors", "none"]

while True:
	ret, frame = cap.read()
	
	if not ret:
		continue
		
	cropped = frame[100:500, 100:500]
	
	cropped = cv2.resize(cropped, (224,224))
	cropped = np.array(cropped, dtype="float32")
	cropped = np.expand_dims(cropped, axis=0)
	
	cropped = preprocess_input(cropped)
	
	p = model.predict(cropped)
	
	prevMove = playerMove
	
	playerMove = np.argmax(p[0])
	
	if(playerMove != 3 and prevMove != playerMove):
		computerMove = rnd.randint(0,2)
		while computerMove == prevComputerMove:
			computerMove = rnd.randint(0,2)
		prevComputerMove = computerMove
		gameStarted = True
		winner = Predict_Winner(playerMove, computerMove)
		
	if(playerMove != 3 and prevMove == playerMove and gameStarted):
		frame[100:500, 800:1200] = icon	
		
	if(playerMove == 3):
		computerMove = 3
		winner = "None"
	
	cv2.rectangle(frame, (100, 100), (500, 500), (255,255,255), 2)
	cv2.rectangle(frame, (800,100), (1200,500), (255,255,255), 2)
	
	cv2.putText(img = frame, text = "Your Move: " + moves[playerMove], org = (100, 90), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.7, color=(255,255,255))
	cv2.putText(img = frame, text = "Computer's Move: " + moves[computerMove], org = (800, 90), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.7, color=(255,255,255))
	cv2.putText(img = frame, text = "Winner: " + winner, org = (550, 550), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(255,255,255))
	
	if(playerMove != 3):
		icon = cv2.imread("images/" + moves[computerMove] + ".png")
		icon = cv2.resize(icon, (400,400))
		frame[100:500, 800:1200] = icon
	
	cv2.imshow("Rock-Paper-Scissors", frame)
		
	k = cv2.waitKey(50)

	if k == ord('q'):
		break	
