from flask import Flask,render_template,url_for,redirect,session
import numpy as np
from wtforms import  FloatField,SubmitField
from flask_wtf import FlaskForm
from keras.models import load_model


def prediction(model,sample_json):
    V_O=sample_json['VIX Open']
    V_H=sample_json['VIX High']
    V_L=sample_json['VIX Low']
    V_C=sample_json['VIX Close']
    
    classes=np.array(['Dont_Buy','Buy'])
    
    buy = [[[[V_O,V_H,V_L,V_C]]]]
    
    class_ind=model.predict_classes(buy)[0]
    
    return classes[class_ind]



app = Flask(__name__)

app.config['SECRET_KEY'] = 'mykeys'


class FlaskForm(FlaskForm):
	Open=FloatField()
	High=FloatField()
	Low=FloatField()
	Close=FloatField()

	submit = SubmitField('Analyze')



@app.route('/',methods=['GET','POST'])
def index():
	form=FlaskForm()

	if form.validate_on_submit():
		session['Open']=form.Open.data
		session['High']=form.High.data
		session['Low']=form.Low.data
		session['Close']=form.Close.data

		return redirect(url_for("buy_prediction"))
	return render_template('home.html',form=form)


model = load_model('C:/Users/yousuf/VIX.h5')

@app.route('/prediction')
def buy_prediction():
	content = {}
	content["VIX Open"] = session['Open']
	content["VIX High"] = session['High']
	content["VIX Low"] = session['Low']
	content["VIX Close"] = session['Close']

	results =prediction(model,content)

	return render_template("prediction.html",results=results)


if __name__ == '__main__':
	app.run() 