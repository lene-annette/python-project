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
    '''Generates an HTML page with all the images in the static folder on the root path.'''
    dir_name = os.path.join('server', 'static')
    # Get all image files in the static folder.
    image_list = os.listdir(dir_name)

    url = 'http://localhost:5000/static'
    # Build img tags using the files in the static folder.
    img_tags = [f'<img src="{url}/{filename}">' for filename in image_list]

    # Append all img tags inside a div.
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
    '''Starts and runs the Flask server.'''
    server.run()
