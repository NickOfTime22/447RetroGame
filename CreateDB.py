#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 15:04:58 2023

@author: brendan
"""
import sqlite3

conn = sqlite3.connect('TopRankTanks.db')


conn.execute('''CREATE TABLE Users
             (username TEXT PRIMARY KEY, 
              password TEXT)''')
             
conn.execute('''CREATE TABLE Scores
             (gameID INTEGER PRIMARY KEY, 
              username TEXT, 
              score INTEGER,
              FOREIGN KEY (username) REFERENCES Users(username))''')
             
conn.execute('''INSERT INTO scores)

conn.commit()

conn.close()