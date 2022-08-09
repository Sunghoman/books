from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sungho:1464@cluster0.xcve6.mongodb.net/?retryWrites=true&w=majority')
db = client.sungho

@app.route('/')
def home():
    if "username" in session:
        return "You are logged in as" + session["username"]
    return render_template('index.html')

@app.route('/book', methods=["POST"])
def book_post():
    url_receive = request.form['url_give']
    name_receive = request.form["name_give"]
    comment_receive = request.form["comment_give"]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, "html.parser")

    title = soup.select_one("meta[property='og:title']")["content"].split("-")[0].strip()
    author = soup.select_one("meta[name='author']")["content"].replace(',', '')
    image = soup.select_one("meta[property='og:image']")["content"]

    doc = {
        "title": title,
        "author": author,
        "image": image,
        "name": name_receive,
        "comment": comment_receive,
        "url": url_receive
    }
    db.books.insert_one(doc)
    return jsonify({"msg": "저장 완료"})

@app.route('/book', methods=["GET"])
def book_get():
    book_list = list(db.books.find({}, {"_id": False}))
    return jsonify({"books": book_list})


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api')
def api():
    return render_template('api.html')

@app.route("/register", methods=["POST"])
def register():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    email_receive = request.form["email_give"]

    doc = {
        "username": username_receive,
        "password": password_receive,
        "email": email_receive
    }

    db.books_users.insert_one(doc)
    return jsonify({"result":"success"})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
