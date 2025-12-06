from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import numpy as np
import pickle
from functools import wraps
from datetime import datetime
import os

# Create Flask app
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize extensions
mysql = MySQL(app)
bcrypt = Bcrypt(app)

# Load ML models
model = pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
ms = pickle.load(open('minmaxscaler.pkl', 'rb'))

# Crop dictionary
crop_dict = {
    1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 
    6: "Papaya", 7: "Orange", 8: "Apple", 9: "Muskmelon", 10: "Watermelon",
    11: "Grapes", 12: "Mango", 13: "Banana", 14: "Pomegranate", 15: "Lentil",
    16: "Blackgram", 17: "Mungbean", 18: "Mothbeans", 19: "Pigeonpeas",
    20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        phone = request.form.get('phone', '')
        
        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, email, password, full_name, phone) VALUES (%s, %s, %s, %s, %s)",
                       (username, email, hashed_password, full_name, phone))
            mysql.connection.commit()
            cur.close()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()
        
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    
    # Get user's recent predictions
    cur.execute("""
        SELECT * FROM predictions 
        WHERE user_id = %s 
        ORDER BY prediction_date DESC 
        LIMIT 5
    """, [session['user_id']])
    recent_predictions = cur.fetchall()
    
    # Get prediction statistics
    cur.execute("""
        SELECT predicted_crop, COUNT(*) as count 
        FROM predictions 
        WHERE user_id = %s 
        GROUP BY predicted_crop 
        ORDER BY count DESC
    """, [session['user_id']])
    crop_stats = cur.fetchall()
    
    cur.close()
    
    return render_template('dashboard.html', 
                         recent_predictions=recent_predictions,
                         crop_stats=crop_stats)

@app.route('/predict-form')
@login_required
def predict_form():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        # Get form data
        N = float(request.form['Nitrogen'])
        P = float(request.form['Phosphorus'])
        K = float(request.form['Potassium'])
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['Ph'])
        rainfall = float(request.form['Rainfall'])
        
        # Prepare features
        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)
        
        # Scale and predict
        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)
        prediction = model.predict(final_features)
        
        # Get crop name
        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            
            # Save prediction to database
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO predictions 
                (user_id, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, predicted_crop)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (session['user_id'], N, P, K, temp, humidity, ph, rainfall, crop))
            mysql.connection.commit()
            
            # Get crop details
            cur.execute("SELECT * FROM crops WHERE name = %s", [crop])
            crop_info = cur.fetchone()
            cur.close()
            
            return render_template('result.html', 
                                 crop=crop, 
                                 crop_info=crop_info,
                                 input_data={
                                     'nitrogen': N, 'phosphorus': P, 'potassium': K,
                                     'temperature': temp, 'humidity': humidity,
                                     'ph': ph, 'rainfall': rainfall
                                 })
        else:
            flash('Could not determine the best crop. Please try again.', 'warning')
            return redirect(url_for('predict_form'))
            
    except Exception as e:
        flash(f'Error processing prediction: {str(e)}', 'danger')
        return redirect(url_for('predict_form'))

@app.route('/crops')
def crops():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM crops ORDER BY name")
    all_crops = cur.fetchall()
    cur.close()
    return render_template('crops.html', crops=all_crops)

@app.route('/crop/<crop_name>')
def crop_detail(crop_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM crops WHERE name = %s", [crop_name])
    crop = cur.fetchone()
    cur.close()
    
    if crop:
        return render_template('crop_detail.html', crop=crop)
    else:
        flash('Crop not found!', 'danger')
        return redirect(url_for('crops'))

@app.route('/history')
@login_required
def history():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM predictions 
        WHERE user_id = %s 
        ORDER BY prediction_date DESC
    """, [session['user_id']])
    predictions = cur.fetchall()
    cur.close()
    
    return render_template('history.html', predictions=predictions)

@app.route('/profile')
@login_required
def profile():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", [session['user_id']])
    user = cur.fetchone()
    cur.close()
    
    return render_template('profile.html', user=user)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
