from flask import Flask, render_template, request
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
import json
import sys
sys.path.append('/Users/mac28/src/pdxapartmentfinder/pipeline')

from predictor import predict
dict90 = json.load(open('../pipeline/data/Day90ApartmentData.json'))



app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
boostrap = Bootstrap(app)

class NameForm(Form):
    id_number = StringField('What is the listing ID Number?',
    	validators=[Required(), 
    	Length(10, message = 'Field must be 10 digit craigslist ID Number')])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scorer', methods=['GET', 'POST'])
def scorer():
	id_number = None
	form = NameForm()
	my_dict = None
	pred, diff, no_assumptions, assumptions = None, None, None, None


	if form.validate_on_submit():
		id_number = form.id_number.data
		form.id_number.data = ''
		pred, diff, no_assumptions, assumptions = predict(
			id_number, dict90,'../pipeline/data/')
		my_dict = assumptions
		

	attrs = ['bed','bath','feet','dog','cat','content',
	'getphotos','hasmap','housingtype','lat','long','laundry',
	'parking','price','smoking','wheelchair']

	
	
	return render_template('scorer.html', id_number=id_number, attrs=attrs,
		my_dict=my_dict,form=form,pred=pred, diff=diff, 
		no_assumptions=no_assumptions,assumptions = assumptions)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)












