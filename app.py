from flask import Flask, request, render_template, flash, jsonify
import pickle


app = Flask(__name__)
app.secret_key = "apkofriowjfkf"


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/index.html")
def home():
    return render_template('index.html')


@app.route("/stroke.html")
def stroke():
    return render_template('stroke.html')


@app.route('/norisk.html')
def norisk():
    return render_template('norisk.html')


@app.route('/doctor.html')
def doctor():
    return render_template('doctor.html')

@app.route('/hospital.html')
def hospital():
    return render_template('hospital.html')


@app.route("/output", methods=["POST", "GET"])
def output():
    if request.method == 'POST':
        g = request.form['gender']
        if g == "male":
            g = 1
        elif g == "female":
            g = 0
        else:
            g = 2


        a = request.form['age']
        if a.isdigit():
            a = int(a)
            a = ((a - 0.08) / (82 - 0.08))
        else:
            flash("Please Enter a Valid Age")
            return render_template('stroke.html')  # Return to the form page


        hyt = request.form['hypertension'].lower()
        hyt = 1 if hyt == "yes" else 0


        ht = request.form['heart-disease'].lower()
        ht = 1 if ht == "yes" else 0


        m = request.form['marriage'].lower()
        m = 1 if m == "yes" else 0


        w = request.form['worktype'].lower()
        w = 0 if w == "government" else 1 if w == "student" else 2 if w == "private" else 3 if w == "self-employed" else 4


        r = request.form['residency'].lower()
        r = 1 if r == "urban" else 0


        gl = int(request.form['glucose'])
        gl = ((gl - 55) / (271 - 55))


        b = int(request.form['bmi'])
        b = ((b - 10.3) / (97.6 - 10.3))


        s = request.form['smoking']
        s = 0 if s == "unknown" else 1 if s == "never smoked" else 2 if s == "formerly smoked" else 3


        try:
            prediction_prob = predict_probability(g, a, hyt, ht, m, w, r, gl, b, s)


            # Adjusted threshold values
            no_risk_threshold = 1.0
            risk_threshold = 0.1


            # Classify predictions based on thresholds
            if prediction_prob >= no_risk_threshold:
                prediction = 'You have a significant risk of having a Stroke'
            elif prediction_prob >= risk_threshold:
                prediction = 'You have chances of having a Stroke'
            else:
                prediction = 'You have no risk of having a Stroke '


            flash(f"Logistic Regression Predicted Probability: {prediction_prob}")
            return render_template('output.html', prediction=prediction, prob=prediction_prob)


        except ValueError as e:
            app.logger.error(f"Error during prediction: {e}")
            flash("Please Enter Valid Values")
            return render_template('stroke.html')  # Return to the form page


def predict_probability(g, a, hyt, ht, m, w, r, gl, b, s):
    model = pickle.load(open('model.pkl', 'rb'))
    result_prob = model.predict_proba([[g, a, hyt, ht, m, w, r, gl, b, s]])[0, 1]
    return result_prob


if __name__ == "__main__":
    app.debug = True
    app.run()