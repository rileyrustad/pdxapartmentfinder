from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
app = Flask(__name__)
boostrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scorer/<id_number>')
def scorer(id_number):
	attrs = ['bed','bath','feet','dog','cat','content',
	'date','getphotos','hasmap','housingtype','lat','long','laundry',
	'parking','price','smoking','time','wheelchair']

	temp_dict = {'bed':'1','bath':'1.5','feet':'1000','dog':'yes','cat':'yes','content':'500',
	'date':'today','getphotos':2,'hasmap':'yes','housingtype':'apartment','lat':'#', 'long':'#',
	'laundry': 'in unit','parking':'street parking','price':'$500','smoking':'no smoking','time':'12:00',
	'wheelchair':'no wheelchair access'}
	my_dict = temp_dict
	return render_template('scorer.html', id_number=id_number, attrs=attrs,my_dict=my_dict)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)