from flask import Flask, render_template, jsonify, request
import sqlite3
from os.path import isfile

app = Flask(__name__)

@app.route('/')
def index():
    if isfile('database.db') == False:
        exec(open('initdb.py').read())
    return render_template('newmovie.html')

@app.route('/newmovie', methods = ['POST'])
def newmovie():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    
    title = request.form['title']
    year = request.form['year']
    
    try:
        cursor.execute('INSERT INTO movies (title,year) VALUES (?,?)', (title,year))
        connection.commit()
        message = 'Success!'
    except:
        connection.rollback()
        message = 'Oops!'
    finally:
        connection.close()
        return render_template('result.html', message = message)

@app.route('/movies')
def movies():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM movies')
    cinematography = cursor.fetchall()
    connection.close()
    return jsonify(cinematography)

@app.route('/search')
def serach():
    partial = request.args.get('title')
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM movies WHERE title LIKE "%{}%" COLLATE NOCASE'.format(partial))
    foundit = cursor.fetchall()
    connection.close()
    return jsonify(foundit)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')
    
app.run(debug = True)