from cgi import escape
from urllib import unquote
import time

def index(req):
    s = """\
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
    <p>Hello World!</p>
    <p>Time is: {time}</p>
    </body>
    </html>
    """

    return s.format(time=time.strftime("%H:%M:%S"))


# test accessing parameters of http get or post requests
# URL localhost/test_publisher/FormTest
def FormTest(req):
    s = """\
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
        <form method="post" action="./FormTest">
            <p>
                Type a word: <input type="text" name="word" value="{val}">
                <input type="submit" value="Submit">
            </p>
            {out}
        </form>
    </body>
    </html>
    """
    word = req.form.getfirst('word', '')
    if word != "":
        word = escape(word) # Escape the user input to avoid script injection attacks
        return s.format(val=word, out="<p>the submitted word was " + word + "</p>")
    else:
        return s.format(val="", out="")


# The Publisher passes the Request object to the function
# URL localhost/test_publisher/ShowAttributes
def ShowAttributes(req):
    s = """\
    <!DOCTYPE html>
    <html>
    <head>
    <style type="text/css">
        td {{padding:0.2em 0.5em;border:1px solid black;}}
        table {{border-collapse:collapse;}}
    </style>
    </head>
    <body>
        <table cellspacing="0" cellpadding="0">{attr}</table>
    </body>
    </html>
    """

    # Loop over the Request object attributes
    attribs = ''
    for attrib in dir(req):
        attribs += '<tr><td>' + attrib + '</td><td>' + escape(unquote(str(req.__getattribute__(attrib)))) + '</td></tr>'

    return s.format(attr=attribs)
