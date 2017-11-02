from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
import numpy as np
app=Flask(__name__)

from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
scaler=StandardScaler()
dfw=pd.read_csv('./static/data/wdata.csv',index_col='iid')
wtrainy=dfw['cluster']
wtrainx=dfw
del wtrainx['cluster']
dfm=pd.read_csv('./static/data/mdata.csv',index_col='iid')
mtrainy=dfm['cluster']
mtrainx=dfm
del mtrainx['cluster']
scaler.fit(wtrainx)
scaler.fit(mtrainx)
wtrainx=scaler.transform(wtrainx)
mtrainx=scaler.transform(mtrainx)
wclf=MLPClassifier(activation='logistic',solver='lbfgs')
wclf.fit(wtrainx,wtrainy)
mclf=MLPClassifier(activation='logistic',solver='lbfgs')
mclf.fit(mtrainx,mtrainy)

#return cluster
def clustering(test,gender):
	test=scaler.transform(test)
	if gender:
		return str(int(wclf.predict(test)[0]))
	else:
		return str(int(mclf.predict(test)[0]))

#return feature description
def description(gender, clu):
	if gender:
		df=pd.read_csv('./static/data/wf.csv',index_col='iid')
	else:
		df=pd.read_csv('./static/data/mf.csv',index_col='iid')
	des=list(df.loc[clu])
	for i in range(len(des)):
		if des[i] is np.nan:
			des.remove(des[i])
	return des

@app.route('/')
def homepage():
	return render_template("main.html")

@app.route('/summary/')
def summary():
	return render_template("summary.html")
@app.route('/research1/')
def research1():
	return render_template("research1.html")
@app.route('/research2/')
def research2():
	return render_template("research2.html")
@app.route('/research3/')
def research3():
	return render_template("research3.html")
@app.route('/research4/')
def research4():
	return render_template("research4.html")

@app.route('/testagain/')
def testagain():
	return render_template('testagain.html')


@app.route('/dashboard/', methods=["GET","POST"])
def dashboard():
	import pandas as pd
	Gender={'Female':1,'Male':0}
	field={'Law':1, 'Math':2, 'Social Science, Psychologist':3, 'Medical Science, Pharmaceuticals, and Bio Tech':4, 
	'Engineering':5,'English/Creative Writing/ Journalism':6, 'History/Religion/Philosophy':7, 
	'Business/Econ/Finance':8, 'Education, Academia':9, 'Biological Sciences/Chemistry/Physics':10, 
	'Social Work':11, 'Undergrad/undecided':12, 'Political Science/International Affairs':13, 'Film':14, 
	'Fine Arts/Arts Administration':15, 'Languages':16, 'Architecture':17, 'Other':18}
	Dates_goout={'Several times a week':1,'Twice a week':2,'Once a week':3,'Twice a month':4, 'Once a month':5, 'Several times a year':6, 'Almost never':7}
	feature=['Gender', 'Age','field','dates','go out','sports','tvsports','exercising','Dining','Museums','Art','Hiking','Gaming','Dancing','Reading','TV','Theater','Movies','concerts','Music','Shopping','Yoga','Attractiveness','Sincerity','IQ','humor','ambition']
	wmatch={'0':'1','1':'2','2':'0','3':'4','4':'5','5':'4','6':'4'}
	mmatch={'0':'2','1':'0','2':'1','3':'2','4':'6','5':'6','6':'1'}
	featurevalue=[]
	if request.form['submit']:
		for i in feature:
			featurevalue.append(request.form.get(i))
	featurevalue[0]=Gender[featurevalue[0]]
	featurevalue[2]=field[featurevalue[2]]
	featurevalue[3]=Dates_goout[featurevalue[3]]
	featurevalue[4]=Dates_goout[featurevalue[4]]
	for i in range(5,22):
		if featurevalue[i]=='1':
			featurevalue[i]=8
		else:
			featurevalue[i]=3
	for i in range(len(featurevalue)):
		featurevalue[i]=int(featurevalue[i])
	cluster=clustering(featurevalue[1:],featurevalue[0])
	if featurevalue[0]==1:
		ta=wmatch[cluster]
	else:
		ta=mmatch[cluster]
	return render_template('dashboard.html',gen=featurevalue[0],wo=cluster,ta=ta)

if __name__=="__main__":
	app.run()