import flask
import logging
import os

server = flask.Flask(__name__)

# Disable logging (no HTTP requests during scraping).
server.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

@server.route('/')
def home():
    dir_name = './server/static'
    image_list = os.listdir(dir_name)

    url = 'http://localhost:5000/static'
    img_tags = [f'<img src="{url}/{filename}">' for filename in image_list]

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
