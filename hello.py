import json
from flask import Flask, request
app = Flask(__name__)
app.debug = True
app.what_am_i_thinking = 'what?'


@app.route('/')
def hello_world():
    return 'Hello World!'

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
    return json.dumps(obj, indent=4).replace('\n', '\n<br/>\n').replace('    ', '&nbsp;' * 4)

@app.route('/current-thought/')
def current_thought():
    return app.what_am_i_thinking

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


if __name__ == '__main__':
    app.run()
