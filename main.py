from flask import Flask, render_template, request
import requests
import json

API_KEY=""

app = Flask(__name__)

# Searches for a capped number of images on Flickr using a provided tag
def image_search(query, max_images=3):
    data = requests \
        .get("https://www.flickr.com/services/feeds/photos_public.gne?format=json&tags={}" \
        .format(query)).text[15:-1]
    json_form = json.loads(data)
    # print(json_form)
    images = []
    if len(json_form["items"]) < max_images:
        max_images = len(json_form)
    for entry in json_form["items"][0:max_images]:
        print("entry: {}".format(entry['media']['m']))
        images.append(entry['media']['m'])
    
    return images

# Searches for videos on youtube using a provided query
def video_search(query):
    data = requests.get('https://youtube.googleapis.com/youtube/v3/search?part=snippet\
            &maxResults=25&q={}&key={}'\
        .format(query, API_KEY), headers={'Accept': 'application/json'}) \
        .json()['items']
    print(data)
    for entry in data:
        print("entry['id']['kind']: {}".format(entry['id']['kind']))
        if entry['id']['kind'] == 'youtube#video':
            print(entry['id']['videoId'])
            return entry['id']['videoId']
    return "unimp"


# Endpoint for triggering Flickr image searches
@app.route("/api/getImage")
def getImage():
    query = request.args.get('query')
    
    images = image_search(query)

    return images[0]

# Endpoint for triggering Youtube video searches
@app.route("/api/getVideo")
def getVideo():
    query = request.args.get('query')
    
    video = video_search(query)

    return video


# Frontend route, the only endpoints designed to be accessed via a browser
@app.route("/")
def hello_world():
    return render_template('main.html')

if __name__ == "__main__":
    app.run(debug=True)