import requests
import json

def parse_google_response(response):
    json_data = json.loads(response.content)
    name = json_data['items'][0]['volumeInfo']['title']
    
    authors = json_data['items'][0]['volumeInfo']['authors']
    author = ""
    if len(authors) > 1:
        for auth in authors:
            author += auth + ", "
        # remove extra comma and whitespace at end
        author = author[:-2]
    else:
        author += authors[0]  
        
    pic = json_data['items'][0]['volumeInfo']['imageLinks']['thumbnail']

    return [name, author, pic]

def create_book_entry(title, author, series, tag_list, status, pic):
    new_entry = {
        "Name": {"title": [{"text": {"content": title}}]},
        "Author": {"rich_text": [{"text": {"content": author}}]},
        "Series": {"rich_text": [{"text": {"content": series}}]},
        "Tags": {"multi_select": tag_list},
        "Status": {"select": {"name": status}},
        "Image": {"files": [{"name": pic[0:99], "type": "external", "external":{"url": pic}}]},
    }

    return new_entry


