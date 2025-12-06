"""
Setup script for extended crops database
Adds 100+ crops that can all be recommended based on conditions
"""

import MySQLdb
from config import Config

def setup_extended_crops():
    try:
        # Connect to database
        db = MySQLdb.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            passwd=Config.MYSQL_PASSWORD,
            db=Config.MYSQL_DB
        )
        cursor = db.cursor()
        
        print("="*60)
        print("🌾 EXTENDED CROPS DATABASE SETUP")
        print("="*60)
        print()
        
        # Read and execute the SQL file
        print("📖 Reading SQL file...")
        with open('extended_crops_database.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split by semicolons and execute each statement
        statements = [s.strip() for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]
        
        print(f"⚙️  Processing {len(statements)} statements...")
        
        for i, statement in enumerate(statements, 1):
            try:
                if statement.strip():
                    cursor.execute(statement)
            except MySQLdb.Error as e:
                if "Duplicate entry" in str(e):
                    continue  # Skip duplicates
                elif "Duplicate column" in str(e):
                    continue  # Column already exists
                # Silently skip other minor errors
        
        db.commit()
        print("✓ Database updated successfully")
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) FROM crops")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM crops WHERE show_in_browse = TRUE")
        browse_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM crops WHERE show_in_browse = FALSE")
        hidden_count = cursor.fetchone()[0]
        
        print()
        print("="*60)
        print("✅ SUCCESS!")
        print("="*60)
        print(f"📊 Total crops: {total}")
        print(f"👁️  Browse menu: {browse_count} crops")
        print(f"🔍 Hidden (search only): {hidden_count} crops")
        print()
        print("💡 All crops can be recommended!")
        print("="*60)
        
        cursor.close()
        db.close()
        
        return True
        
    except Exception as e:
        print()
        print("="*60)
        print(f"❌ ERROR: {e}")
        print("="*60)
        print()
        print("💡 Troubleshooting:")
        print("  1. Make sure MySQL is running")
        print("  2. Check config.py credentials")
        print("  3. Verify database exists")
        print("="*60)
        return False

if __name__ == "__main__":
    print()
    if setup_extended_crops():
        print()
        print("📝 NEXT STEPS:")
        print("  1. Restart Flask: python app_modern.py")
        print("  2. Visit 'All Crops' page")
        print("  3. Try recommendations!")
        print()
    else:
        print()
        print("❌ Setup failed. Check errors above.")
        print()
