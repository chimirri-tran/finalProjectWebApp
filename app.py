import requests
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response, session, escape, json
import json
from flask import jsonify

serverUri = "http://localhost:5700/sdelab"
app = Flask(__name__, template_folder="./")
id="-1"

@app.route("/")
def index():

	#if id == "-1":
	#	return render_template('login.html')
	p = {"food": "","server":"motivation"}
	motivation = requests.get(serverUri+'/external', params=p).json()["motivationalPhrase"][0]#.str
	#motivation = "temporary mot phrase" 
	return render_template('index.html',motivation=motivation)

@app.route("/newMot", methods=['POST'])
def newMotivation():

	p = {"food": "","server":"motivation"}
	motivation = requests.get(serverUri+'/external', params=p).json()["motivationalPhrase"][0]#.str
	#motivation = "temporary mot phrase"
	return render_template('index.html',motivation=motivation)

@app.route("/calories", methods=['POST'])
def calories():

	p = {"food": "","server":"motivation"}
	motivation = requests.get(serverUri+'/external', params=p).json()["motivationalPhrase"][0]#.str
	#motivation = "temporary mot phrase"
	food = request.form['food']
	p = {"food": food,"server":"calories"}
	response = requests.get(serverUri+'/external', params=p).json()
	calories = response["calories"]
	exercize = response["exercize"][0]
	if calories == 0: calories = "don't know, please try something else"
	else: calories = "" + food + " has " + str(calories) + " kcal"
	if exercize != "NO":
		return render_template('index.html',calories=calories,motivation=motivation,exercize="This food has a lot of calories, exercize! "+exercize)
	else:
		return render_template('index.html',calories=calories,motivation=motivation,exercize="this food is ok to eat")

@app.route("/daily", methods=['GET', 'POST'])
def daily():

	p = {"food": "","server":"motivation"}
	motivation = requests.get(serverUri+'/external', params=p).json()["motivationalPhrase"][0]


	p = {"action": "daily", 'idperson':id,'steps':request.form['steps'], 'heartrate':request.form['heartrate'], 'weight':request.form['weight'], 'sleephours':request.form['sleephours'], 'minbloodpressure':request.form['minbloodpressure'],'maxbloodpressure':request.form['maxbloodpressure']}

	response = requests.get(serverUri+'/internal', params=p).json()

	if response["ok"] == "ok":
		feedBackSteps = response["feedBackSteps"]
		feedBackHeartrate = response["feedBackHeartrate"]
		feedBackWeight = response["feedBackWeight"]
		feedBackSleephours = response["feedBackSleephours"]
		feedBackMinbloodpressure = response["feedBackMinbloodpressure"]
		feedBackMaxbloodpressure = response["feedBackMaxbloodpressure"]
		return render_template('index.html',motivation=motivation,feedBackSteps=feedBackSteps,feedBackHeartrate=feedBackHeartrate,feedBackWeight=feedBackWeight,feedBackSleephours=feedBackSleephours,feedBackMinbloodpressure=feedBackMinbloodpressure,feedBackMaxbloodpressure=feedBackMaxbloodpressure)
	else:
		return render_template('index.html',motivation=motivation,error="you did not insert data correctly")
	


@app.route("/registration")
def registration():

	return render_template('registration.html')

@app.route("/login")
def login():

	return render_template('login.html')

@app.route("/fromregistration", methods=['POST'])
def fromregistration():

	p = {"action": "registration",'username':request.form['username'],'password':request.form['password'],'height':request.form['height'],'steps':request.form['steps'], 'heartrate':request.form['heartrate'], 'weight':request.form['weight'], 'sleephours':request.form['sleephours'], 'minbloodpressure':request.form['minbloodpressure'],'maxbloodpressure':request.form['maxbloodpressure']}


	response = requests.get(serverUri+'/internal', params=p).json()

	if response["ok"] == "ok":
		p = {"food": "","server":"motivation"}
		motivation = requests.get(serverUri+'/external', params=p).json()["motivationalPhrase"][0]
		id = response["idperson"]
		#feedBackSteps = response["feedBackSteps"]
		#feedBackHeartrate = response["feedBackHeartrate"]
		#feedBackWeight = response["feedBackWeight"]
		#feedBackSleephours = response["feedBackSleephours"]
		#feedBackMinbloodpressure = response["feedBackMinbloodpressure"]
		#feedBackMaxbloodpressure = response["feedBackMaxbloodpressure"]
		return render_template('index.html',motivation=motivation)#,feedBackSteps=feedBackSteps,feedBackHeartrate=feedBackHeartrate,feedBackWeight=feedBackWeight,feedBackSleephours=feedBackSleephours,feedBackMinbloodpressure=feedBackMinbloodpressure,feedBackMaxbloodpressure=feedBackMaxbloodpressure)
	else:
		return render_template('registration.html',error="you did not insert data correctly")

@app.route("/fromlogin", methods=['POST'])
def fromlogin():

	p = {"action": "login",'username':request.form['username'],'password':request.form['password']}


	response = requests.get(serverUri+'/internal', params=p).json()
	if response["ok"] == "ok":
		p = {"food": "","server":"motivation"}
		motivation = requests.get(serverUri+'/external', params=p).json()["motivationalPhrase"][0]
		id = response["idperson"]
		return render_template('index.html',motivation=motivation)
	else:
		return render_template('login.html',error="you did not insert correct data")


if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')
