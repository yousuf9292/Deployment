from flask import Flask,request,jsonify
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
    print(player.shape)
    player=scaler.transform(player)

    prediction=model.predict(player)

    return float(prediction)


app= Flask(__name__)


@app.route('/')
def home():
	return	"<h1>Flask Running</h1>"


model=load_model('C:/Users/yousuf/nba.h5')
scaler_model=joblib.load('C:/Users/yousuf/nba.pickle')


@app.route('/api/predictions',methods=['POST'])
def predictions():
	content=request.json
	results=return_predictions(model,scaler_model,content)

	return jsonify(results)


if __name__ == '__main__':
	app.run(debug=True)