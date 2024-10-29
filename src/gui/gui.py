# Author: Isabelle Maddox
# Last Updated: 10/29/2024

from flask import Flask, render_template, request
import requests
import helpers

app = Flask(__name__)

GOOGLE_API_KEY = "YOUR_API_SECRET_HERE"
NOTION_SECRET = "YOUR_NOTION_SECRET_HERE"
DATABASE_ID = "YOUR_NOTION_DATABASE_ID_HERE"

# set to True to enable Debug Mode
DEBUG = False


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        # get input from form
        title = request.form.get("name")
        series = request.form.get("series")
        author = request.form.get("author")
        pic = request.form.get("pic")
        tags = request.form.get("tags")
        status = request.form.get("status")

        tag_list = []

        tags = tags.split(",")

        for tag in tags:
            tag_list.append({"name": tag})

        #create new book entry
        new_entry = helpers.create_book_entry(title,author,series,tag_list,status,pic)
        
        if DEBUG:
            print(f"title:{title}, series:{series}, author:{author}, pic:{pic}, tags:{tags}, status:{status}")
        
        # send information to Notion database
        headers = {
            "Authorization": "Bearer " + NOTION_SECRET,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        payload = {
            "parent": {"database_id": DATABASE_ID}, 
            "properties": new_entry
        }
        
        response = requests.post(f"https://api.notion.com/v1/pages" , headers=headers, json=payload)
        if (response.status_code == 200):
            print("SUCCESS")
        else:
            print(f"ERROR: {response.status_code} {response.json()}")
    return render_template("index.html")

@app.route('/book', methods=['POST', 'GET'])
def request_book():
    if request.method == "POST":
        # getting ISBN input
        isbn = request.form.get("isbn")

        if DEBUG:
            print(isbn)
        
        # send request
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={GOOGLE_API_KEY}")
        if (response.status_code == 200):
            # parse response
            name, author, pic = helpers.parse_google_response(response)

            if DEBUG:
                print(f"{name} | {author} | {pic}")

            return render_template("book.html", bookName=name, bookAuthor=author, bookPic=pic)
        else:
            print(f"ERROR: {response.status_code}")
    return render_template("index.html")
    
