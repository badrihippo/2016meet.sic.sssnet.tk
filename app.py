import os
from flask import Flask, render_template, redirect, url_for
from tinydb import TinyDB, Query
from flask.ext.wtf import Form
import wtforms as wtf

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
                for x in values:
                    # TODO: Check for actual valid dates, not just integer triplets
                    d = x.strip().split('-')
                    if len(d) == 3:
                        try:
                            d = [int(i) for i in d]
                        except ValueError:
                            raise wtf.ValidationError('Invalid date: %s. Input must be a list of dates formatted dd-mm-yyyy only.' % x)
                        data.append(d)
                    else:
                        raise wtf.ValidationError('Invalid date: %s. Input must be a list of dates formatted dd-mm-yyyy only.' % x)
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

        dv.insert(v)
        return redirect(url_for('vote_thanks'))
    return render_template('vote.htm', form=form)

@app.route('/vote/thanks/')
def vote_thanks():
    # TODO: get most popular date
    return render_template('vote_thanks.htm')

if __name__ == '__main__':
    app.run()
