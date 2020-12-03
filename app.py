from flask import Flask, request, render_template
from transformers import RobertaTokenizer, TFRobertaForMultipleChoice
import tensorflow as tf
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
 
 
def run_transformers(question, choices):
    tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
    model = TFRobertaForMultipleChoice.from_pretrained('roberta-base')
    prompt = question
    choice0 = choices[0]
    choice1 = choices[1]
    encoding = tokenizer([[prompt, prompt], [choice0, choice1]], return_tensors='tf', padding=True)
    inputs = {k: tf.expand_dims(v, 0) for k, v in encoding.items()}
    outputs = model(inputs)  # batch size is 1
    # the linear classifier still needs to be trained
    probs = tf.nn.softmax(outputs.logits)
    final_probs = list(probs.numpy())[0]
    print(final_probs)
    return final_probs


### Calculate score
# Generate answer from the question or information that answer coudn't be found
def solution_pipeline(question, choices):
    result, equation_status = run_transformers(question, choices), True

    # Clear values which are empty
    for idx,val in enumerate(choices):
        if val == '':
            result[idx] = "NaN"

    # Just one answer -> five 100% 
    if result.count("NaN") == 4:
        for idx, val in enumerate(result):
            if val != "NaN":
                result[idx] = 100

    if result.count("NaN") == 5:
        equation_status = False

    return result, equation_status


@app.route('/loading_answer', methods=['GET', 'POST'])
def loading_answer():
    # Init empty vars for quesiton and choices 
    choice_a, choice_b, choice_c, choice_d, choice_e, question = '','','','','',''

    # Chocies text
    choice_a, choice_b, choice_c, choice_d, choice_e = request.form['choice_a'], request.form['choice_b'], request.form['choice_c'], request.form['choice_d'], request.form['choice_e']
    all_choices = [choice_a, choice_b, choice_c, choice_d, choice_e]

    # Question text
    question = request.form['question_field']

    # Calculate the most possible solution 
    answer, equation_status = solution_pipeline(question, all_choices)

    # Show answer on the screen
    return render_template("score.html", question = question, choices = all_choices, answer = answer, equation_status = equation_status)




