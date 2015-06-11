import json
from flask import Flask, request, make_response, redirect, url_for
app = Flask(__name__)
app.debug = True
app.what_am_i_thinking = 'what?'
app.board_messages = []

menu = """    
              <a href="/">Home</a>
              <br/>
              <a href="/sign-in-form/">Sign In</a>
              <br/>
              <a href="/sign-out/">Sign Out</a>
              <br/>
              <a href="/post-message-form/">Post a message</a>
              <br/>
              <a href="/message-board/">Message board</a>
              <br/>
              <a href="/current-thought/">Current Thought</a>
              <br/>
              <a href="/thought-change-form/">Change Thought</a>
              <br/>
              <a href="/use-json/">Use JSON</a>
              <hr>
              <br/>
        """

@app.route('/')
def hello_world():
    output = menu
    output += """Hello World!"""
    name = request.cookies.get('name')
    if name:
        output += "Hey, " + name
    return output



@app.route('/use-json/')
def different_name_for_function():
    obj = {
        'statement_list': [
            {
                'claim': 'json is better than xml',
                'truth_value': True,
            },
            {
                'claim': 'this function is returning json the way it should be returned by a real api',
                'truth_value': False,
            },
        ],
    }
    output = """    <a href="/">Home</a>
                    <br/>
              """
    output += json.dumps(obj, indent=4).replace('\n', '\n<br/>\n').replace('    ', '&nbsp;' * 4)

    return output

@app.route('/current-thought/')
def current_thought():
    output = app.what_am_i_thinking
    output += """   <br/>
                    <a href="/">Home</a>
              """
    return output

@app.route('/thought-change-form/')
def thought_change_form():
    line_list = [
        '<a href="/">home page</a>',
        '<form method="post" action="/set-thought/">',
        '<input type="text" name="thought" placeholder="put new thought here"/>',
        '<input type="submit" value="Post">',
        '</form>',
    ]
    return '\n<br/>\n'.join(line_list)
    
@app.route('/set-thought/', methods=['POST'])
def set_thought():
    thought = request.form.get('thought', '')
    app.what_am_i_thinking = thought
    return 'thought changed to ' + thought + '\n<br/>\n<br/>\n<a href="/">home page</a>\n<br/>\n<br/>\n<a href="/thought-change-form/">thought change form</a>'


@app.route('/sign-in-form/')
def sign_in_form():
    form = [
        '<a href="/">Home</a>',
        '<form method="post" action="/sign-in/">',
        '<input type="text" name="name" placeholder="Name"/>',
        '<input type="submit" value="Post">',
        '</form>',
    ]
    return '\n<br/>\n'.join(form)

@app.route('/sign-in/', methods=['POST'])
def sign_in():
    name = request.form.get('name', '')

    resp = make_response(redirect(url_for('hello_world')))
    resp.set_cookie('name', name)
    return resp

@app.route('/sign-out/')
def sign_out():
    resp = make_response(redirect(url_for('hello_world')))
    resp.set_cookie('name', '')
    return resp

@app.route('/post-message-form/')
def post_msg_form():
    form =[
        '<a href="/">Home</a>',
        '<form method="post" action="/post-message/">',
        '<textarea name="msg" autofocus="autofocus" cols=50 rows=4 wrap="hard" placeholder="Type your post here"></textarea>',
        '<input type="submit" value="Post">',
        '</form>',
    ]
    return '\n<br/>\n'.join(form)

class Message(object):
    def __init__(self, author, message, date):
        self.author = author
        self.message = message
        self.date = date

@app.route('/post-message/', methods=['POST'])
def post_msg():
    author = request.cookies.get('name')
    if not author: 
        author = "Anonymous"
    msg = request.form.get('msg', '')
    date = "now"
    msg_obj = Message(author, msg, date)
    app.board_messages.append(msg_obj)
    return redirect(url_for('display_messages'))



def format_message(msg):
    output = ""
    output += "<hr>"
    msg_format = [
    msg.date + "<br/>",
    msg.author + "<hr>",
    msg.message
    ]
    output += ''.join(msg_format)
    return output

@app.route('/message-board/', methods=['GET'])
def display_messages():
    output = menu
    FilterUser = request.args.get('user', '')

    if app.board_messages:
        if FilterUser:
            for msg in app.board_messages:
                if msg.author == FilterUser:    
                    output += format_message(msg)
        else:
            for msg in app.board_messages:
                output += format_message(msg)
    else:
        output += "No messages!"

    form =[
        '<form method="post" action="/post-message/">',
        '<textarea name="msg" autofocus="autofocus" cols=50 rows=4 wrap="hard" placeholder="Type your post here"></textarea>',
        '<input type="submit" value="Post">',
        '</form>',
    ]
    output += '\n<br/>\n'.join(form)
    return output


if __name__ == '__main__':
    app.run()
