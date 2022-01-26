from flask import Flask
from flask_restful import Resource, Api


# Flask is a lightweight rest API
app = Flask(__name__)
api = Api(app)

videos = {}

# Class as resource
class Video(Resource):
    # Methods for get, post, put, patch, delete.
    def get(self, video_id):
        return videos[video_id]

    def put(self, video_id):
        videos[video_id]
        return

# Telling the api that there's a resource and it's key is this small url
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)