from flask import Flask,render_template,url_for,redirect,session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import FloatField,SubmitField,TextField
import numpy as np
import joblib
from keras.models import load_model



def return_predictions(model,scaler,sample_json):
    POS= sample_json["POS"]
    GP= sample_json["GP"]
    MIN= sample_json["MIN"]
    PTS= sample_json["PTS"]
    FGM= sample_json["FGM"]
    FGA= sample_json["FGA"]
    FG= sample_json["FG%"]
    PM= sample_json["3PM"]
    PA= sample_json["3PA"]
    P= sample_json["3P%"]
    FTM= sample_json["FTM"]
    FTA= sample_json["FTA"]
    FT= sample_json["FT%"]
    FTM= sample_json["FTM"]
    FTA= sample_json["FTA"]
    FT= sample_json["FT%"]
    REB= sample_json["REB"]
    AST= sample_json["AST"]
    STL= sample_json["STL"]
    BLK= sample_json["BLK"]
    TO= sample_json["TO"]
    DD2= sample_json["DD2"]
    TD3= sample_json["TD3"]
    
    
    player=[[POS, GP, MIN, PTS, FGM, FGA, FG, PM, PA, P, FTM, FTA, FT, REB, AST, STL, BLK, TO, DD2, TD3]]
    
    player=scaler.transform(player)

    prediction=model.predict(player)

    return float(prediction)







app= Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY']="thisissecret"




class Form(FlaskForm):
	
	position = TextField("player_position")

	games_played = FloatField("games_played")
	
	minutes_per_game = FloatField("minutes_per_game")
	
	points_per_game = FloatField("points_per_game")
	
	average_field_goal_made = FloatField("average_field_goal_made")
	
	average_field_goal_attempted = FloatField("average_field_goal_attempted")
	
	field_goal_percentage = FloatField("field_goal_percentage")
	
	average_3_point_field_goal = FloatField("average_3_point_field_goal")
	
	average_3_point_field_goal_attempted = FloatField("average_3_point_field_goal_attempted")
	
	three_point_field_goal_percentage = FloatField("three_point_field_goal_percentage")

	average_free_throws_made=FloatField('average_free_throws_made')
	
	average_free_throws_attempted = FloatField("average_free_throws_attempted")
	
	free_throw_percentage = FloatField("free_throw_percentage")
	
	rebounds_per_game = FloatField("rebounds_per_game")
	
	assist_per_game = FloatField("assist_per_game")
	
	steals_per_game = FloatField("steals_per_game")
	
	block_per_game = FloatField("block_per_game")
	
	turnover_per_game = FloatField("turnover_per_game")
	
	double_double = FloatField("double_double")
	
	triple_double = FloatField("triple_double")

	submit = SubmitField("Submit")



@app.route('/form',methods=['GET','POST'])
def form():
	form=Form()
	if form.validate_on_submit():

		session['position']=form.position.data
		
		session['games_played']=form.games_played.data
		
		session['minutes_per_game']=form.minutes_per_game.data
		
		session['points_per_game']=form.points_per_game.data
		
		session['average_field_goal_made']=form.average_field_goal_made.data
		
		session['average_field_goal_attempted']=form.average_field_goal_attempted.data
		
		session['field_goal_percentage']=form.field_goal_percentage.data
		
		session['average_3_point_field_goal']=form.average_3_point_field_goal.data
		
		session['average_3_point_field_goal_attempted']=form.average_3_point_field_goal_attempted.data
		
		session['three_point_field_goal_percentage']=form.three_point_field_goal_percentage.data
		
		session['average_free_throws_made']=form.average_free_throws_made.data
		
		session['average_free_throws_attempted']=form.average_free_throws_attempted.data
		
		session['free_throw_percentage']=form.free_throw_percentage.data
		
		session['rebounds_per_game']=form.rebounds_per_game.data
		
		session['assist_per_game']=form.assist_per_game.data
		
		session['steals_per_game']=form.steals_per_game.data
		
		session['block_per_game']=form.block_per_game.data
		
		session['turnover_per_game']=form.turnover_per_game.data

		session['double_double']=form.double_double.data

		session['triple_double']=form.triple_double.data

		return redirect(url_for('prediction'))

	return render_template("home.html",form=form)


model=load_model('C:/Users/yousuf/nba.h5')
scaler_model=joblib.load('C:/Users/yousuf/nba.pickle')


@app.route('/prediction')
def prediction():
	content={}

	content['POS']=session['position']
	content['GP']=session['games_played']
	content['MIN']=session['minutes_per_game']
	content['PTS']=session['points_per_game']
	content['FGM']=session['average_field_goal_made']
	content['FGA']=session['average_field_goal_attempted']
	content['FG%']=session['field_goal_percentage']
	content['3PM']=session['average_3_point_field_goal']
	content['3PA']=session['average_3_point_field_goal_attempted']
	content['3P%']=session['three_point_field_goal_percentage']
	content['FTM']=session['average_free_throws_made']
	content['FTA']=session['average_free_throws_attempted']
	content['FT%']=session['free_throw_percentage']
	content['REB']=session['rebounds_per_game']
	content['AST']=session['assist_per_game']
	content['STL']=session['steals_per_game']
	content['BLK']=session['block_per_game']
	content['TO']=session['turnover_per_game']
	content['DD2']=session['double_double']
	content['TD3']=session['triple_double']

	results=round(return_predictions(model,scaler_model,content))

	return render_template('predictions.html',results=results)

if __name__ == '__main__':
	app.run(debug=True)