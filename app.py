from flask import Flask, request, render_template
import flask

app = flask.Flask(__name__)

### Templates route

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/index', methods=['GET', 'POST'])
def index_html():
    return render_template("index.html")


@app.route('/examples', methods=['GET'])
def examples():
    return render_template("examples.html")


@app.route('/loading', methods=['GET'])
def loading():
    return render_template("loading.html")


@app.route('/score', methods=['GET'])
def score():
    return render_template("score.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title=404), 404
 
### Calculate score

# Generate answer from the question or information that answer coudn't be found
def solution_pipeline(question):
    return 2

@app.route('/loading_answer', methods=['GET', 'POST'])
def loading_answer():
    question = request.form['question_field']

    # TODO - run loading page here

    answer = solution_pipeline(question)

    # debug - delete in production
    print("Queston:", question, "Type of question:",
        type(question),
        'Answer:', answer,
        'type(answer):',
        type(answer))

    # final answer
    return render_template("score.html", question = question, answer = answer)




