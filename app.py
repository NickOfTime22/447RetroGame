#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:54:46 2023

@author: brendan
"""

from flask import Flask, request, session, redirect, url_for
from flask.templating import render_template
import sqlite3
import logging


app = Flask(__name__)
app.debug = True
app.secret_key = 'admin'
app.logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
app.logger.addHandler(console_handler)


@app.route('/updateDB/1/<int:finalHealth>/<string:username>', methods=['POST','GET'])
def updateOne(finalHealth,username):
    conn = sqlite3.connect('TopRankTanks.db')
    c = conn.cursor()
    current = c.execute('SELECT levelOne FROM Users WHERE username=?',(username,)).fetchone()
    if(current[0] < finalHealth):
        c.execute('UPDATE Users SET levelOne =? WHERE username=?',(finalHealth,username,))
    conn.commit()
    return render_template('Levels.html', username=username)
    
@app.route('/levelThree/<string:username>', methods=['POST'])
def levelThree(username):
    return render_template('LevelThree.html',username=username)

@app.route('/levelTwo/<string:username>', methods=['POST'])
def levelTwo(username):
    return render_template('LevelTwo.html',username=username)

@app.route('/levelOne/<string:username>', methods=['POST'])
def levelOne(username):
    return render_template('LevelOne.html',username=username)


@app.route('/levels/<string:username>', methods=['POST','GET'])
def levels(username):
    return render_template('Levels.html', username=username)

def load_global_scores():
    conn = sqlite3.connect('TopRankTanks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Scores ORDER BY score DESC LIMIT 5')
    scores = [{'username': row[1], 'score': row[2]} for row in c.fetchall()]
    return scores

def load_local_scores(username):
    conn = sqlite3.connect('TopRankTanks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Scores WHERE username=? ORDER BY score DESC LIMIT 5', (username,))
    loc_scores = [{'username': row[1], 'score': row[2]} for row in c.fetchall()]
    return loc_scores

@app.route('/main_menu/<string:username>')
def main_menu(username):
    scores = load_global_scores()
    loc_scores = load_local_scores(username)
    return render_template('MainMenu.html',username=username,scores=scores,loc_scores=loc_scores)

@app.route('/account', methods=['POST','GET'])
def account():
    
    conn = sqlite3.connect('TopRankTanks.db')
    cur = conn.cursor()
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        
        if user is None:
            if(password != confirm):
                session['error'] = 'Passwords do not match'
                return render_template('account.html', error=session.get('error'))
            else:
                cur.execute("INSERT INTO Users (username, password, levelOne, levelTwo, levelThree) VALUES (?,?,0,0,0)", (username,password))
                conn.commit()
                return redirect('/login')
                
        else:
            session['error'] = 'Username already exists'
            return render_template('account.html', error=session.get('error'))
        
    return render_template('Account.html')

    
@app.route('/login', methods=['POST', 'GET'])
def login():
    conn = sqlite3.connect('TopRankTanks.db')
    cur = conn.cursor()
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
    
        if user is None:
            session['error'] = 'Invalid username'
            return render_template('login.html', error=session.get('error'))
    
        if user[1] != password:
            session['error'] = 'Incorrect password'
            return render_template('login.html', error=session.get('error'))
    
        session['username'] = username
        return redirect(url_for('main_menu', username=username))
    else:
        session.pop('error', None)
        return render_template('login.html', error=None)


@app.route('/')
def index():
    return render_template('Login.html')

if __name__ == '__main__':
    app.run()