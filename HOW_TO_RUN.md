# How to Run This Project

## Quick Start (If Already Set Up)

```bash
python app_modern.py
```

Then open browser: http://127.0.0.1:5000

---

## First Time Setup

### Step 1: Install Python Packages

```bash
pip install -r requirements_updated.txt
```

Or install individually:
```bash
pip install Flask flask-mysqldb flask-bcrypt flask-mail flask-wtf plotly numpy pickle5
```

### Step 2: Set Up MySQL Database

1. **Start MySQL** (make sure it's running)

2. **Create Database:**
   ```sql
   mysql -u root -p
   CREATE DATABASE crop_recommendation_db;
   exit;
   ```

3. **Run Database Setup:**
   ```bash
   mysql -u root -p crop_recommendation_db < database_setup.sql
   ```

4. **Add Extended Crops (100+ crops):**
   ```bash
   python setup_extended_crops.py
   ```

### Step 3: Configure Database Connection

Edit `config.py` with your MySQL credentials:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'crop_recommendation_db'
```

### Step 4: Run the Application

```bash
python app_modern.py
```

You should see:
```
============================================================
🌾 Crop Recommendation System
============================================================
Server running at: http://127.0.0.1:5000
Press Ctrl+C to stop
============================================================
```

### Step 5: Open in Browser

Go to: **http://127.0.0.1:5000**

---

## What You Can Do

### 1. Register an Account
- Click "Register"
- Fill in your details
- Create account

### 2. Login
- Use your username and password
- Access all features

### 3. Get Crop Recommendation
- Click "Predict" or "Get Recommendation"
- Enter soil parameters:
  - Nitrogen (N)
  - Phosphorus (P)
  - Potassium (K)
  - Temperature
  - Humidity
  - pH Level
  - Rainfall
- Click "Get Recommendation"
- See the best crop for your conditions!

### 4. Browse Crops
- Click "Crops"
- See all available crops
- Search for specific crops
- Click "View All" to see 100+ crops
- Click any crop to see details

### 5. View Dashboard
- Click "Dashboard"
- See your prediction history
- View charts and statistics

### 6. Check History
- Click "History"
- See all your past predictions

### 7. Edit Profile
- Click your username (top right)
- Update your information

---

## Troubleshooting

### "Module not found" Error
```bash
pip install [module_name]
```

### "Can't connect to MySQL"
1. Make sure MySQL is running
2. Check credentials in `config.py`
3. Verify database exists:
   ```bash
   mysql -u root -p -e "SHOW DATABASES;"
   ```

### "No module named 'MySQLdb'"
```bash
pip install mysqlclient
```

On Windows, if that fails:
```bash
pip install pymysql
```
Then add to `app_modern.py` at the top:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Port Already in Use
Change port in `app_modern.py` (last line):
```python
app.run(debug=False, port=5001)  # Changed from 5000
```

### Images Not Showing
The app works with placeholder images. To add real images:
```bash
python create_placeholder_images.py
```

---

## File Structure

```
crop_classification_system/
├── app_modern.py              ← Main application (RUN THIS)
├── config.py                  ← Database configuration
├── crop_recommendation_engine.py  ← Recommendation algorithm
├── database_setup.sql         ← Initial database setup
├── extended_crops_database.sql    ← 100+ crops data
├── setup_extended_crops.py    ← Setup script for crops
├── model.pkl                  ← ML model (legacy)
├── standscaler.pkl           ← Scaler (legacy)
├── minmaxscaler.pkl          ← Scaler (legacy)
├── requirements_updated.txt   ← Python packages
├── static/
│   └── images/
│       └── crops/            ← Crop images
└── templates/
    └── *_modern.html         ← Web pages
```

---

## Common Commands

### Start Application
```bash
python app_modern.py
```

### Stop Application
Press `Ctrl + C` in terminal

### Reset Database
```bash
mysql -u root -p -e "DROP DATABASE crop_recommendation_db;"
mysql -u root -p -e "CREATE DATABASE crop_recommendation_db;"
mysql -u root -p crop_recommendation_db < database_setup.sql
python setup_extended_crops.py
```

### Check if Running
Open browser: http://127.0.0.1:5000

---

## Features

✅ User registration and login
✅ Smart crop recommendation (100+ crops)
✅ Interactive dashboard with charts
✅ Prediction history
✅ Crop browsing and search
✅ Detailed crop information
✅ User profile management
✅ Modern, responsive UI
✅ Clean terminal output

---

## Quick Reference

| Action | Command |
|--------|---------|
| Install packages | `pip install -r requirements_updated.txt` |
| Setup database | `python setup_extended_crops.py` |
| Run application | `python app_modern.py` |
| Stop application | `Ctrl + C` |
| Access app | http://127.0.0.1:5000 |

---

## Need Help?

Check these files:
- `SETUP_INSTRUCTIONS.md` - Detailed setup
- `APP_FILES_COMPARISON.md` - Which app file to use
- `WHICH_APP_TO_RUN.txt` - Quick guide
- `EXTENDED_CROPS_README.md` - About the crop system

---

## Summary

**To run the project:**
1. Install packages: `pip install -r requirements_updated.txt`
2. Setup database: `python setup_extended_crops.py`
3. Configure: Edit `config.py` with your MySQL password
4. Run: `python app_modern.py`
5. Open: http://127.0.0.1:5000

That's it! 🚀
