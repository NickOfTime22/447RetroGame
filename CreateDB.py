#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 15:04:58 2023

@author: brendan
"""
import sqlite3

conn = sqlite3.connect('TopRankTanks.db')

conn.execute('''DROP TABLE Users''')

conn.execute('''DROP TABLE Scores''')

conn.execute('''CREATE TABLE Users
             (username TEXT PRIMARY KEY, 
              password TEXT,
              levelOne INTEGER,
              levelTwo INTEGER,
              levelThree INTEGER,
              levelFour INTEGER)''')
             
conn.execute('''CREATE TABLE Scores
             (gameID INTEGER PRIMARY KEY, 
              username TEXT, 
              score INTEGER,
              FOREIGN KEY (username) REFERENCES Users(username))''')
             
conn.execute('''INSERT INTO scores Values (1,"BeatMyScore",10)''')
conn.execute('''INSERT INTO scores Values (2,"BeatMyScore",20)''')
conn.execute('''INSERT INTO scores Values (3,"BeatMyScore",30)''')
conn.execute('''INSERT INTO scores Values (4,"BeatMyScore",40)''')
conn.execute('''INSERT INTO scores Values (5,"BeatMyScore",50)''')
conn.execute('''INSERT INTO Users Values ("guest","guest",0,0,0,0)''')

conn.commit()

conn.close()