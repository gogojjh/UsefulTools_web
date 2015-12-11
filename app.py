# coding=utf8
from flask import Flask, render_template, redirect, url_for, flash
from flask.ext.script import Manager

from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from pymongo import MongoClient
from plane_tickets import plane
from train_tickets import train
from flask.ext.bootstrap import Bootstrap
app = Flask(__name__)
app.config['SECRET_KEY'] = '950513'


manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class TypeForm(Form):
    type = SelectField(u'你瞅啥', choices=[('', ''),
                                        ('cdec', 'cdec'),
                                        ('movie', u'电影'),
                                        ('plane', u'机票查询'),
                                        ('train', u'火车票查询'),
                                        ('haodiao', u'梁浩何时有对象？')])
    submit = SubmitField(u'让我瞅瞅')


class PlaneForm(Form):
    p1 = StringField(u'起飞地', validators=[DataRequired()])
    p2 = StringField(u'降落地', validators=[DataRequired()])
    p3 = DateField(u'出发日期', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField(u'让我瞅瞅')


class TrainForm(Form):
    p1 = StringField(u'出发地', validators=[DataRequired()])
    p2 = StringField(u'目的地', validators=[DataRequired()])
    p3 = DateField(u'出发日期', format='%Y-%m-%d', validators=[DataRequired()])
    p4 = SelectField(u'发车时间', choices=[('00:00--24:00', '00:00--24:00'),
                                         ('00:00--08:00', '00:00--08:00'),
                                         ('08:00--16:00', '08:00--16:00'),
                                         ('16:00--24:00', '16:00--24:00')])
    p5 = SelectField(u'车次类型', choices=[('0', u'全部'),
                                         ('1', u'高铁\动车'),
                                         ('2', u'其它')])
    submit = SubmitField(u'让我瞅瞅')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = TypeForm()
    if form.validate_on_submit():
        if form.type.data == 'cdec':
            return redirect(url_for('cdecinfo'))
        elif form.type.data == 'movie':
            return redirect(url_for('movieinfo'))
        elif form.type.data == 'plane':
            return redirect(url_for('plane_tickets'))
        elif form.type.data == 'train':
            return redirect(url_for('train_tickets'))
        elif form.type.data == 'haodiao':
            return render_template('404.html')
    return render_template('index.html', form=form)


@app.route('/cdecinfo', methods=['POST', 'GET'])
def cdecinfo():
    flash('A dota a day,keeps girls away.')
    db = MongoClient().cdec
    rank_list = db.cdec.find()
    return render_template('cdecinfo.html', rank_list=rank_list)


@app.route('/movieinfo', methods=['POST', 'GET'])
def movieinfo():
    flash('You must be a single dog~')
    db = MongoClient().movieinfo
    movie_info = db.movieinfo.find()
    return render_template('movieinfo.html', movie_info=movie_info)


@app.route('/plane_tickets', methods=['POST', 'GET'])
def plane_tickets():
    # flash(u'天涯若比邻')
    form = PlaneForm()
    if form.validate_on_submit():
        client = MongoClient()
        db = client.plane
        db.plane.drop()
        plane_info = {
            '1': form.p1.data,
            '2': form.p2.data,
            '3': str(form.p3.data)
        }
        db.plane.insert_one(plane_info)
        return redirect(url_for('plane_tickets_results'))
    return render_template('plane_tickets.html', form=form)


@app.route('/plane_tickets_results', methods=['POST', 'GET'])
def plane_tickets_results():
    flash(u'本页数据由途牛提供，要旅游，找途牛~')
    db = MongoClient().plane
    plane_db = db.plane.find()
    for each in plane_db:
        plane_data = each
    plane_info = plane(plane_data)
    return render_template('plane_tickets_results.html', plane_info=plane_info)


@app.route('/train_tickets', methods=['POST', 'GET'])
def train_tickets():
    # flash(u'天涯若比邻')
    form = TrainForm()
    if form.validate_on_submit():
        client = MongoClient()
        db = client.train
        db.train.drop()
        train_info = {
            '1': form.p1.data,
            '2': form.p2.data,
            '3': str(form.p3.data),
            '4': form.p4.data,
            '5': form.p5.data
        }
        db.train.insert_one(train_info)
        return redirect(url_for('train_tickets_results'))
    return render_template('train_tickets.html', form=form)


@app.route('/train_tickets_results', methods=['POST', 'GET'])
def train_tickets_results():
    flash(u'本页数据由12306提供，它已经很努力了，不要黑它了～')
    db = MongoClient().train
    train_db = db.train.find()
    for each in train_db:
        train_data = each
    train_info = train(train_data)
    return render_template('train_tickets_results.html', train_info=train_info)



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1024, debug=True)
