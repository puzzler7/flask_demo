#!/usr/bin/env python3.9

from flask import Flask, render_template_string, request, make_response, abort
from inspect import getsource # just used for putting the code in the page

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h1>Welcome to my Flask demo!</h1>

    The code for this entire website is at the bottom of the page.
    On every other page where I do a thing, I put the corresponding code.

    <br><br>
    Get the raw code <a href='/code'>here</a>, or on <a href='https://github.com/puzzler7/flask_demo'>GitHub</a>.
    There's also instructions on running the website with Docker at the GitHub repo.
    <br><br>

    Bullet points for today:
    <ul>
        <li> Minimal <a href='/hello_world.py'>Hello World example</a> </li>
        <li> Static sites: <a href='/static1'>Part 1</a> and <a href='/static2'>Part 2</a> </li>
        <li> <a href='/users/0x1337c0de'>Path</a> 
        and <a href='/students?name=Slim Shady'>Query</a> parameters </li>
        <li> <a href='/db'>Templates</a> </li>
    </ul>
    '''+prettify(open(__file__).read())

@app.route('/static1')
def static1():
    return '''
    <h1>Check it out it's a static site wooooooooooooooo!</h1>
    I'm supposed to "Hello, World!" here, right?
    '''+prettify(getsource(static1))

@app.route('/static2')
def static2():
    return open("static2.html").read()+prettify(getsource(static2))

@app.route('/users/<userID>')
def path(userID):
    return '''
    <h1>You have asked for the user with the ID %s.</h1>
    I really hope that exists. Is that my job?
    '''%userID+prettify(getsource(path))

@app.route('/students')
def query():
    name = request.args['name'] if 'name' in request.args else '{Name Missing}'
    return '''
    <h1>Paging the student named %s</h1>
    Will the real %s please stand up?
    '''%(name, name) + prettify(getsource(query))


def gen_fake_db():
    # fake database for template demo
    from random import seed, randint
    from hashlib import sha256
    seed(0x1337c0de)
    # generating a bunch of random junk
    return [(str(randint(0,2**32)), sha256(str(randint(0, 2**32)).encode()).hexdigest()) for _ in range(100)]  

@app.route('/db')
def my_query():
    try:
        skip = int(request.args['skip']) if 'skip' in request.args else 0
        limit = int(request.args['limit']) if 'limit' in request.args else 10
    except ValueError as e:
        skip = 0
        limit = 10

    template = '''
        <h1>Database Query Results</h1>
        <h2>{{ limit }} results returned: </h2>
        <ul>
        {% for key, val in db[skip:skip+limit] %}
        <li> {{key}}: {{val}} </li>
        {% endfor %}

        {# this is a comment that you won't see #}

        </ul>
    '''

    data = {
        "db": gen_fake_db(),
        "skip": skip,
        "limit": limit
    }
    return render_template_string(template, **data) + prettify(getsource(my_query))

allowed_files = ["app.py", "hello_world.py", "requirements.txt", "static2.html"]

@app.route('/code')
def get_code():
    template = '''
        <h1>Raw code files</h1>
        <ul>
        {% for item in files %}
            <li> <a href='/{{item}}'>{{item}}</a> </li>
        {%endfor%}
        </ul>
    '''
    return render_template_string(template, files=allowed_files) + \
            prettify(getsource(get_code)) + prettify(getsource(static_files))

@app.route('/<fname>')
def static_files(fname):
    if fname not in allowed_files:
        abort(404)
    resp = make_response(open(fname).read())
    resp.mimetype = 'text/plain'
    return resp

# putting this at the bottom so it's clear it's not Flask stuff
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# pretty print python code
def prettify(text):
    formatter = HtmlFormatter(noclasses=True)
    return "<h2>Code:</h2>"+highlight(text, PythonLexer(), formatter)