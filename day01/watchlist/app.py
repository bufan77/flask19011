from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route('/')
def index():
    name = "Bruce"
    movies = [
        {'title': "大赢家", "year":"2020"},
        {'title': "囧妈", "year":"2020"},
        {'title': "战狼", "year":"2020"},
        {'title': "心花路放", "year":"2020"},
        {'title': "大赢家", "year":"1999"},
    ]
    return render_template('index.html', name=name, movies=movies)


if __name__ == "__main__":
    app.run()