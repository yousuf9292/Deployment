from flask import Flask,render_template,url_for,redirect,session
import numpy as np
from wtforms import  FloatField,SubmitField
from flask_wtf import FlaskForm
from keras.models import load_model


def prediction(model,sample_json):
    s_len=sample_json['sepal_length']
    s_wid=sample_json['sepal_width']
    p_len=sample_json['petal_length']
    p_wid=sample_json['petal_width']
    
    classes=np.array(['setosa','versicolor','virginica'])
    
    flower = [[[s_len,s_wid,p_len,p_wid]]]
    
    class_ind=model.predict_classes(flower)[0]
    
    return classes[class_ind]



app = Flask(__name__)

app.config['SECRET_KEY'] = 'mykey'


class FlaskForm(FlaskForm):
	sep_len=FloatField()
	sep_wid=FloatField()
	pet_len=FloatField()
	pet_wid=FloatField()

	submit = SubmitField('Analyze')



@app.route('/',methods=['GET','POST'])
def index():
	form=FlaskForm()

	if form.validate_on_submit():
		session['sep_len']=form.sep_len.data
		session['sep_wid']=form.sep_wid.data
		session['pet_len']=form.pet_len.data
		session['pet_wid']=form.pet_wid.data

		return redirect(url_for("flower_prediction"))
	return render_template('home.html',form=form)


model = load_model('C:/Users/yousuf/iris.h5')

@app.route('/prediction')
def flower_prediction():
	content = {}
	content["sepal_length"] = session['sep_len']
	content["sepal_width"] = session['sep_wid']
	content["petal_length"] = session['pet_len']
	content["petal_width"] = session['pet_wid']

	results =prediction(model,content)

	return render_template("prediction.html",results=results)


if __name__ == '__main__':
	app.run() 