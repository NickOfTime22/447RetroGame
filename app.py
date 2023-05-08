#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:54:46 2023

@author: brendan
"""

from flask import Flask, request, session, redirect, flash
from flask.templating import render_template
import sqlite3
import json
import logging


app = Flask(__name__)
app.debug = True
app.secret_key = 'admin'
app.logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
app.logger.addHandler(console_handler)

def load_global_scores():
    conn = sqlite3.connect('TopRankTanks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scores ORDER BY score DESC LIMIT 5')
    rows = c.fetchall()
    scores = []
    for row in rows:
        scores.append({'name': row[0], 'score': row[1]})
    conn.close()
    return json.dumps({'data': scores})

def load_local_scores():
    conn = sqlite3.connect('TopRankTanks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scores ORDER BY score DESC LIMIT 5')
    rows = c.fetchall()
    scores = []
    for row in rows:
        scores.append({'score': row[0]})
    conn.close()
    return json.dumps({'data': scores})


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
            return redirect('/login')
    
        if user[1] != password:
            session['error'] = 'Invalid password'
            return redirect('/login')
    
        session['username'] = username
        return redirect('/game/' + username)
    else:
        error = session.pop('error', None)
        return render_template('login.html', error=error)

@app.route('/game/<string:username>')
def game(username):
    conn = sqlite3.connect('TopRankTanks.db')
    cur = conn.cursor()
    
    
    username = request.args.get('username')
    return render_template('Game.html',username=username)

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
        
        app.logger.info("hello")
        
        if user is None:
            if(password != confirm):
                session['error'] = 'Passwords do not match'
                return redirect('/Account')
            else:
                cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (username,password))
                conn.commit()
                return redirect('/login')
                
        else:
            session['error'] = 'Username already exists'
            return redirect('/Account')
        
    return render_template('Account.html')

    
@app.route('/')
def index():
    return render_template('Login.html')

if __name__ == '__main__':
    app.run()