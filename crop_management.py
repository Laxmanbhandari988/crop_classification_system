from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, TextAreaField, FloatField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo
import numpy as np
import pickle
import plotly
import plotly.graph_objs as go
import plotly.express as px
import json
from functools import wraps
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
import requests
from crop_recommendation_engine import CropRecommendationEngine
import logging

# Suppress unnecessary logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Create Flask app
app = Flask(__name__)
app.config.from_object('config.Config')

# Disable Flask default request logging for cleaner output
import sys
if not app.debug:
    app.logger.disabled = True
    log.disabled = True

# Initialize extensions
mysql = MySQL(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
csrf = CSRFProtect(app)

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load ML models
try:
    model = pickle.load(open('model.pkl', 'rb'))
    # Random Forest trained on raw data - no scalers needed
except FileNotFoundError:
    model = None

# Crop dictionary with additional info
crop_dict = {
    1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 
    6: "Papaya", 7: "Orange", 8: "Apple", 9: "Muskmelon", 10: "Watermelon",
    11: "Grapes", 12: "Mango", 13: "Banana", 14: "Pomegranate", 15: "Lentil",
    16: "Blackgram", 17: "Mungbean", 18: "Mothbeans", 19: "Pigeonpeas",
    20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
}

# Forms
class PredictionForm(FlaskForm):
    nitrogen = FloatField('Nitrogen (N)', validators=[DataRequired(), NumberRange(min=0, max=300)])
    phosphorus = FloatField('Phosphorus (P)', validators=[DataRequired(), NumberRange(min=0, max=200)])
    potassium = FloatField('Potassium (K)', validators=[DataRequired(), NumberRange(min=0, max=300)])
    temperature = FloatField('Temperature (°C)', validators=[DataRequired(), NumberRange(min=-10, max=60)])
    humidity = FloatField('Humidity (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    ph = FloatField('pH Level', validators=[DataRequired(), NumberRange(min=0, max=14)])
    rainfall = FloatField('Rainfall (mm)', validators=[DataRequired(), NumberRange(min=0, max=5000)])
    submit = SubmitField('Get Recommendation')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

# Utility functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_weather_data(city="Delhi"):
    """Get weather data from OpenWeatherMap API (optional feature)"""
    try:
        # This is a placeholder - you would need to sign up for OpenWeatherMap API
        # api_key = "your_api_key_here"
        # url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        # response = requests.get(url)
        # return response.json()
        return None
    except:
        return None

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
    # Get some statistics for the homepage
    try:
        cur = mysql.connection.cursor(DictCursor)
        cur.execute("SELECT COUNT(*) as total_users FROM users")
        total_users = cur.fetchone()['total_users']
        
        cur.execute("SELECT COUNT(*) as total_predictions FROM predictions")
        total_predictions = cur.fetchone()['total_predictions']
        
        cur.execute("SELECT predicted_crop, COUNT(*) as count FROM predictions GROUP BY predicted_crop ORDER BY count DESC LIMIT 3")
        popular_crops = cur.fetchall()
        cur.close()
        
        stats = {
            'total_users': total_users,
            'total_predictions': total_predictions,
            'popular_crops': popular_crops
        }
    except:
        stats = {'total_users': 0, 'total_predictions': 0, 'popular_crops': []}
    
    return render_template('index.html', stats=stats)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        full_name = form.full_name.data
        phone = form.phone.data
        
        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        try:
            cur = mysql.connection.cursor(DictCursor)
            cur.execute("INSERT INTO users (username, email, password, full_name, phone) VALUES (%s, %s, %s, %s, %s)",
                       (username, email, hashed_password, full_name, phone))
            mysql.connection.commit()
            cur.close()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Username or email already exists!', 'danger')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        cur = mysql.connection.cursor(DictCursor)
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
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    cur = mysql.connection.cursor(DictCursor)
    
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
    
    # Get monthly prediction trends
    cur.execute("""
        SELECT DATE_FORMAT(prediction_date, '%%Y-%%m') as month, COUNT(*) as count
        FROM predictions 
        WHERE user_id = %s AND prediction_date >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
        GROUP BY month
        ORDER BY month
    """, [session['user_id']])
    monthly_trends = cur.fetchall()
    
    cur.close()
    
    # Create charts
    charts = create_dashboard_charts(crop_stats, monthly_trends)
    
    return render_template('dashboard.html', 
                         recent_predictions=recent_predictions,
                         crop_stats=crop_stats,
                         charts=charts)

@app.route('/predict-form', methods=['GET', 'POST'])
@login_required
def predict_form():
    form = PredictionForm()
    if form.validate_on_submit():
        try:
            # Get form data
            N = form.nitrogen.data
            P = form.phosphorus.data
            K = form.potassium.data
            temp = form.temperature.data
            humidity = form.humidity.data
            ph = form.ph.data
            rainfall = form.rainfall.data
            
            # Use the new recommendation engine
            engine = CropRecommendationEngine(mysql)
            crop, score, crop_details = engine.recommend_crop(
                N, P, K, temp, humidity, ph, rainfall
            )
            
            if crop and score > 30:  # Minimum threshold for recommendation
                # Save prediction to database
                cur = mysql.connection.cursor(DictCursor)
                cur.execute("""
                    INSERT INTO predictions 
                    (user_id, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, predicted_crop)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (session['user_id'], N, P, K, temp, humidity, ph, rainfall, crop))
                mysql.connection.commit()
                
                # Get crop details from database
                cur.execute("SELECT * FROM crops WHERE name = %s", [crop])
                crop_info = cur.fetchone()
                cur.close()
                
                # Create visualization
                feature_list = [N, P, K, temp, humidity, ph, rainfall]
                chart = create_prediction_chart(feature_list, crop)
                
                return render_template('result.html', 
                                     crop=crop, 
                                     crop_info=crop_info,
                                     input_data={
                                         'nitrogen': N, 'phosphorus': P, 'potassium': K,
                                         'temperature': temp, 'humidity': humidity,
                                         'ph': ph, 'rainfall': rainfall
                                     },
                                     match_score=score,
                                     match_details=crop_details,
                                     chart=chart)
            else:
                flash('Could not find a suitable crop for these conditions. Please adjust your parameters.', 'warning')
                return redirect(url_for('predict_form'))
                
        except Exception as e:
            flash(f'Error processing prediction: {str(e)}', 'danger')
            return redirect(url_for('predict_form'))
    else:
        return render_template('predict.html', form=form)

@app.route('/crops')
def crops():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    show_all = request.args.get('show_all', 'false', type=str) == 'true'
    
    cur = mysql.connection.cursor(DictCursor)
    
    if search:
        # When searching, show all matching crops
        cur.execute("SELECT * FROM crops WHERE name LIKE %s ORDER BY name", [f'%{search}%'])
    elif show_all:
        # Show all crops when requested
        cur.execute("SELECT * FROM crops ORDER BY name")
    else:
        # By default, show all crops sorted by popularity
        cur.execute("SELECT * FROM crops ORDER BY popularity_score DESC, name")
    
    all_crops = cur.fetchall()
    
    # Get total count for display
    cur.execute("SELECT COUNT(*) as total FROM crops")
    total_count = cur.fetchone()['total']
    
    cur.close()
    
    return render_template('crops.html', crops=all_crops, search=search, 
                         show_all=show_all, total_count=total_count)

@app.route('/crop/<crop_name>')
def crop_detail(crop_name):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM crops WHERE name = %s", [crop_name])
    crop = cur.fetchone()
    
    # Get related predictions
    cur.execute("""
        SELECT AVG(nitrogen) as avg_n, AVG(phosphorus) as avg_p, AVG(potassium) as avg_k,
               AVG(temperature) as avg_temp, AVG(humidity) as avg_humidity, 
               AVG(ph) as avg_ph, AVG(rainfall) as avg_rainfall, COUNT(*) as total_predictions
        FROM predictions WHERE predicted_crop = %s
    """, [crop_name])
    avg_conditions = cur.fetchone()
    cur.close()
    
    if crop:
        return render_template('crop_detail.html', crop=crop, avg_conditions=avg_conditions)
    else:
        flash('Crop not found!', 'danger')
        return redirect(url_for('crops'))

@app.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    per_page = app.config['POSTS_PER_PAGE']
    
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT * FROM predictions 
        WHERE user_id = %s 
        ORDER BY prediction_date DESC
        LIMIT %s OFFSET %s
    """, [session['user_id'], per_page, (page - 1) * per_page])
    predictions = cur.fetchall()
    
    # Get total count for pagination
    cur.execute("SELECT COUNT(*) as total FROM predictions WHERE user_id = %s", [session['user_id']])
    total = cur.fetchone()['total']
    cur.close()
    
    return render_template('history.html', 
                         predictions=predictions, 
                         page=page, 
                         total=total, 
                         per_page=per_page)

@app.route('/profile')
@login_required
def profile():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", [session['user_id']])
    user = cur.fetchone()
    
    # Get user statistics
    cur.execute("SELECT COUNT(*) as total_predictions FROM predictions WHERE user_id = %s", [session['user_id']])
    stats = cur.fetchone()
    cur.close()
    
    return render_template('profile.html', user=user, stats=stats)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Here you would typically send an email
        # For now, we'll just flash a success message
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)

# API Routes
@app.route('/api/predict', methods=['POST'])
@login_required
def api_predict():
    """API endpoint for predictions"""
    try:
        data = request.get_json()
        
        if not data or model is None:
            return jsonify({'error': 'Invalid data or model not available'}), 400
        
        # Extract features
        features = [
            data.get('nitrogen', 0),
            data.get('phosphorus', 0),
            data.get('potassium', 0),
            data.get('temperature', 0),
            data.get('humidity', 0),
            data.get('ph', 0),
            data.get('rainfall', 0)
        ]
        
        # Make prediction
        single_pred = np.array(features).reshape(1, -1)
        # Random Forest trained on raw data, no scaling needed
        prediction = model.predict(single_pred)
        
        crop = crop_dict.get(prediction[0], 'Unknown')
        
        return jsonify({
            'success': True,
            'predicted_crop': crop,
            'confidence': float(prediction[0]),
            'input_features': {
                'nitrogen': features[0],
                'phosphorus': features[1],
                'potassium': features[2],
                'temperature': features[3],
                'humidity': features[4],
                'ph': features[5],
                'rainfall': features[6]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crops')
def api_crops():
    """API endpoint to get all crops"""
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM crops ORDER BY name")
    crops = cur.fetchall()
    cur.close()
    
    return jsonify({'crops': crops})

# Chart creation functions
def create_dashboard_charts(crop_stats, monthly_trends):
    charts = {}
    
    # Crop distribution pie chart
    if crop_stats:
        crops = [stat['predicted_crop'] for stat in crop_stats[:5]]
        counts = [stat['count'] for stat in crop_stats[:5]]
        
        fig = px.pie(values=counts, names=crops, title="Your Top Recommended Crops")
        charts['crop_pie'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Monthly trends line chart
    if monthly_trends:
        months = [trend['month'] for trend in monthly_trends]
        counts = [trend['count'] for trend in monthly_trends]
        
        fig = px.line(x=months, y=counts, title="Monthly Prediction Trends")
        charts['monthly_trends'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

def create_prediction_chart(features, crop):
    """Create a radar chart for the prediction features"""
    categories = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=features,
        theta=categories,
        fill='toself',
        name=f'Conditions for {crop}'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(features) * 1.2]
            )),
        showlegend=True,
        title=f"Soil & Climate Conditions for {crop}"
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Crop Recommendation System")
    print("="*60)
    print(f"Server running at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    # Run with debug mode to see errors
    app.run(debug=True, port=5000, use_reloader=False)
