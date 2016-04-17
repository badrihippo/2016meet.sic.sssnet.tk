import os
from flask import Flask, render_template, redirect, url_for
from tinydb import TinyDB, Query
from flask.ext.wtf import Form
import wtforms as wtf
from datetime import datetime

app = Flask(__name__)
try:
    app.config.from_pyfile('instance/config.py')
except:
    # Set defaults
    app.config['SECRET_KEY'] = 'secret'
    this_dir = os.path.dirname(os.path.realpath(__file__))
    app.config['TINYDB_DB_PATH'] = os.path.join(this_dir, 'sic2016meet.json')

class DateListWidget(wtf.widgets.TextInput):
    def __init__(self):
        super(DateListWidget, self).__init__()

    def __call__(self, field, **kwargs):
        kwargs['data-provide'] = 'datepicker'
        kwargs['data-date-multidate'] = 'true'
        kwargs['data-date-format'] = 'dd-mm-yyyy'
        return super(DateListWidget, self).__call__(field, **kwargs)


class DateListField(wtf.Field):
    widget = DateListWidget()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            data = []
            for v in valuelist:
                values = v.split(',')
                for d in values:
                    try:
                        # Check for valid date
                        datetime.strptime(d, '%d-%m-%Y')
                        # Valid. Append to list
                        data.append(d)
                    except ValueError:
                        raise wtf.ValidationError('Invalid date: %s. Input must be a list of dates formatted dd-mm-yyyy only.' % d)
            self.data = data
        else:
            self.data = []

class DateVoteForm(Form):
    name = wtf.StringField('Name', validators=[wtf.validators.Required()])
    shop = wtf.StringField('Shop name', validators=[wtf.validators.Required()])
    email = wtf.StringField('Email ID')

    good_dates = DateListField()
    bad_dates = DateListField()

db = TinyDB(app.config['TINYDB_DB_PATH'])
dv = db.table('date_votes')

# Vote checker
def get_vote_dict():
    '''
    Analyze dates from all votes, weight the different dates, and
    arrange them in a dictionary of the form { date: vote_count }
    '''
    good_dates = []
    bad_dates = []
    vote_dict = {}
    for vote in dv.all():
        if vote['name'] != 'Nobody': # Skip test votes
            good_dates += vote['good_dates']
            bad_dates += vote['bad_dates']
    for d in good_dates:
        if vote_dict.has_key(d):
            vote_dict[d] += 1
        else:
            vote_dict[d] = 1
    for d in bad_dates:
        if vote_dict.has_key(d):
            vote_dict[d] -= 2 # More weighting for bad-date votes
        else:
            vote_dict[d] = -2
    return vote_dict
def get_top_dates():
    '''
    Returns a list of the most popular dates, according to vote
    '''
    vote_dict = get_vote_dict()
    if len(vote_dict) == 0: return [] # Return if empty dict
    vote_sizes = []
    # Invert list to sort by votes
    vote_density = {}
    for key, value in vote_dict.items():
        if not vote_density.has_key(value):
            vote_density[value] = []
            vote_sizes.append(value)
        vote_density[value].append(key)
    vote_sizes.sort()
    top_dates = vote_density[vote_sizes[-1]]
    # Convert date strings to actual dates
    top_dates_processed = [ datetime.strptime(d, '%d-%m-%Y') for d in top_dates ]
    top_dates_processed.sort()
    return top_dates_processed

@app.route('/')
def index():
    form = DateVoteForm()
    form.action = url_for('vote')
    return render_template('index.htm', form=form)

@app.route('/vote/', methods=['GET', 'POST'])
def vote():
    form = DateVoteForm()
    if form.validate_on_submit():
        v = {}
        v['name'] = form.name.data
        v['shop'] = form.shop.data
        v['email'] = form.email.data
        v['good_dates'] = form.good_dates.data
        v['bad_dates'] = form.bad_dates.data
        v['timestamp'] = datetime.now().isoformat()

        dv.insert(v)
        return redirect(url_for('vote_thanks'))
    return render_template('vote.htm', form=form)

@app.route('/vote/thanks/')
def vote_thanks():
    top_dates = [ d.strftime('%d %b %Y') for d in get_top_dates() ]
    return render_template('vote_thanks.htm', top_dates = top_dates)

if __name__ == '__main__':
    app.run()
