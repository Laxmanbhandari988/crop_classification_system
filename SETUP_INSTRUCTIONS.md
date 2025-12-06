# Crop Recommendation System - Setup Instructions

## Prerequisites
1. **Python 3.8+** installed
2. **XAMPP** installed (for MySQL database)
3. **pip** (Python package manager)

## Step 1: Start XAMPP MySQL

1. Open XAMPP Control Panel
2. Start **Apache** and **MySQL** services
3. Click on **Admin** button next to MySQL to open phpMyAdmin
4. Or access phpMyAdmin at: `http://localhost/phpmyadmin`

## Step 2: Create Database

### Option A: Using phpMyAdmin (Recommended)
1. Open phpMyAdmin (`http://localhost/phpmyadmin`)
2. Click on "Import" tab
3. Click "Choose File" and select `database_setup.sql`
4. Click "Go" button at the bottom
5. Database and tables will be created automatically

### Option B: Using MySQL Command Line
1. Open Command Prompt
2. Navigate to project directory
3. Run: `mysql -u root -p < database_setup.sql`
4. Press Enter (default password is empty)

## Step 3: Install Python Dependencies

Open Command Prompt in project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (Web framework)
- Flask-MySQLdb (MySQL connector)
- Flask-Bcrypt (Password hashing)
- NumPy, Pandas (Data processing)
- Scikit-learn (Machine Learning)

## Step 4: Configure Database Connection

The database configuration is in `config.py`:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Default XAMPP password is empty
MYSQL_DB = 'crop_recommendation_db'
```

**Note:** If you changed your MySQL root password in XAMPP, update `MYSQL_PASSWORD` in `config.py`

## Step 5: Add Crop Images

Create the crops image directory:
```bash
mkdir static\images\crops
```

Download and place crop images in `static/images/crops/` folder. See `CROP_IMAGES_LIST.md` for image names.

## Step 6: Run the Application

```bash
python app_enhanced.py
```

The application will start at: `http://127.0.0.1:5000`

## Step 7: Create Your First Account

1. Open browser and go to `http://127.0.0.1:5000`
2. Click "Sign Up" button
3. Fill in registration form
4. Login with your credentials
5. Start getting crop recommendations!

## Troubleshooting

### MySQL Connection Error
- Make sure XAMPP MySQL is running
- Check if database `crop_recommendation_db` exists
- Verify credentials in `config.py`

### Module Not Found Error
- Run: `pip install -r requirements.txt` again
- Make sure you're using the correct Python environment

### Port Already in Use
- Change port in `app_enhanced.py`: `app.run(debug=True, port=5001)`

### Images Not Loading
- Make sure images are in `static/images/crops/` folder
- Check image filenames match the database entries
- Default fallback image will show if specific crop image is missing

## Default Login (After Setup)

You can create your own account through the registration page. There are no default credentials.

## Database Structure

- **users**: Stores user accounts
- **crops**: Contains crop information and growing conditions
- **predictions**: Stores prediction history for each user

## Features

✅ User Registration & Authentication
✅ Crop Prediction using ML
✅ Prediction History
✅ Crop Information Database
✅ User Dashboard
✅ Responsive Design

## Support

For issues or questions, refer to the README.md or contact support.
