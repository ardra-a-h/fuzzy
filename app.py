from flask import Flask, render_template, request
from fuzzy_logic_system import evaluate_fuzzy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Render the input form

@app.route('/evaluate', methods=['POST'])
def evaluate():
    # Get user inputs from the form
    traffic_density = float(request.form['traffic_density'])
    queue_length = float(request.form['queue_length'])

    # Evaluate the fuzzy logic system
    green_signal_time = evaluate_fuzzy(traffic_density, queue_length)

    return render_template(
        'result.html',
        traffic_density=traffic_density,
        queue_length=queue_length,
        green_signal_time=green_signal_time
    )

if __name__ == '__main__':
    app.run(debug=True)
