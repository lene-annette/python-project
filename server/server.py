import flask
import os

server = flask.Flask(__name__)

@server.route('/')
def home():
    dir_name = './server/static'
    image_list = os.listdir(dir_name)

    url = 'http://localhost:5000/static'
    img_tags = [f'<img src="{url}/{file_name}">' for file_name in image_list]

    div = '<div>' + ''.join(img_tags) + '</div>'

    html = '''
    <html>
        <head>
            <title>Flask</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            {div}
        </body>
    </html>
    '''.format(div=div)

    return flask.render_template_string(html)

def run():
    server.run()

