from flask import Flask, request, render_template, flash, jsonify
import pickle

app = Flask(__name__)
app.secret_key = "apkofriowjfkf"


@app.route("/")
def index():
    return render_template('index.html')

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
            return "Please Enter a Valid Age"
        
        
        #hyper-tension
        hyt = request.form['hypertension']
        hyt = hyt.lower()
        if hyt == "yes":
            hyt = 1
        else:
            hyt = 0
            
        
        #heart-disease
        ht = request.form['heart-disease']
        ht = ht.lower()
        if ht == "yes":
            ht = 1
        else:
            ht = 0
            
        
        #marriage
        m = request.form['marriage']
        m = m.lower()
        if m == "yes":
            m = 1
        else:
            m = 0
            
        
        #worktype
        w = request.form['worktype']
        w = w.lower()
        if w == "government":
            w = 0
        elif w == "student":
            w = 1
        elif w == "private":
            w = 2
        elif w == "self-employed":
            w = 3
        else:
            w = 4
            
            
        #residency-type
        r = request.form['residency']
        r = r.lower()
        if r == "urban":
            r = 1
        else:
            r = 0
            
        #glucose-levels
        gl = request.form['glucose']
        gl = int(gl)
        gl =  ((int(gl) - 55)/(271 - 55))
            
            
        #bmi
        b = request.form['bmi']
        b = int(b)
        b = ((b-10.3)/(97.6-10.3))
        
            
        #smoking
        s = request.form['smoking']
        if s == "unknown":
            s = 0
        elif s == "never smoked":
            s = 1
        elif s == "formerly smoked":
            s = 2
        elif s == "smokes":
            s = 3
        else:
            s = 0

        try:
            prediction = stroke_pred(g,a,hyt,ht,m,w,r,gl,b,s)
            return render_template('output.html',prediction=prediction)

        except ValueError:
            return "Please Enter Valid Values"
        

#prediction-model
def stroke_pred(g,a,hyt,ht,m,w,r,gl,b,s):
    
    #load model
    model = pickle.load(open('model.pkl','rb'))

    #predictions
    result = model.predict([[g,a,hyt,ht,m,w,r,gl,b,s]])

    #output
    if result[0] == 1:
        pred = 'You have chances of having a Stroke'
    else:
        pred = 'You have no risk of having a Stroke'

    return pred
if __name__ == "__main__":
    app.debug = True  # Enable debug mode
    app.run()