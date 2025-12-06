"""
Advanced Crop Recommendation Engine
Recommends the best crop from a large database based on soil and climate conditions
"""

from MySQLdb.cursors import DictCursor

class CropRecommendationEngine:
    """
    Rule-based recommendation engine that scores crops based on how well
    the input conditions match their ideal growing requirements
    """
    
    def __init__(self, mysql_connection):
        self.mysql = mysql_connection
    
    def parse_range(self, range_str):
        """Parse range strings like '20-30°C' or '60-70%' to get min and max"""
        try:
            # Remove units and split by dash
            clean = range_str.replace('°C', '').replace('%', '').replace('mm', '').strip()
            if '-' in clean:
                parts = clean.split('-')
                return float(parts[0]), float(parts[1])
            else:
                # Single value, use ±10% as range
                val = float(clean)
                return val * 0.9, val * 1.1
        except:
            return None, None
    
    def calculate_score(self, value, ideal_min, ideal_max):
        """
        Calculate how well a value fits within ideal range
        Returns score from 0-100
        """
        if ideal_min is None or ideal_max is None:
            return 50  # Neutral score if no data
        
        # Perfect score if within range
        if ideal_min <= value <= ideal_max:
            return 100
        
        # Calculate how far outside the range
        if value < ideal_min:
            diff = ideal_min - value
            penalty = min(diff / ideal_min * 100, 100)
        else:
            diff = value - ideal_max
            penalty = min(diff / ideal_max * 100, 100)
        
        return max(0, 100 - penalty)
    
    def recommend_crop(self, nitrogen, phosphorus, potassium, temperature, 
                       humidity, ph, rainfall):
        """
        Recommend the best crop based on input parameters
        Returns: (crop_name, score, crop_details)
        """
        cur = self.mysql.connection.cursor(DictCursor)
        
        # Get all crops with their ideal conditions
        cur.execute("""
            SELECT id, name, description, ideal_temperature, ideal_humidity, 
                   ideal_ph, ideal_rainfall, growing_season, image_url
            FROM crops
            ORDER BY name
        """)
        
        all_crops = cur.fetchall()
        cur.close()
        
        best_crop = None
        best_score = 0
        best_details = None
        
        for crop in all_crops:
            # Access dictionary values
            crop_id = crop['id']
            name = crop['name']
            desc = crop['description']
            ideal_temp = crop['ideal_temperature']
            ideal_hum = crop['ideal_humidity']
            ideal_ph_range = crop['ideal_ph']
            ideal_rain = crop['ideal_rainfall']
            season = crop['growing_season']
            img = crop['image_url']
            
            # Parse ideal ranges
            temp_min, temp_max = self.parse_range(ideal_temp)
            hum_min, hum_max = self.parse_range(ideal_hum)
            ph_min, ph_max = self.parse_range(ideal_ph_range)
            rain_min, rain_max = self.parse_range(ideal_rain)
            
            # Calculate scores for each parameter
            temp_score = self.calculate_score(temperature, temp_min, temp_max)
            hum_score = self.calculate_score(humidity, hum_min, hum_max)
            ph_score = self.calculate_score(ph, ph_min, ph_max)
            rain_score = self.calculate_score(rainfall, rain_min, rain_max)
            
            # Weighted average (temperature and rainfall are more important)
            total_score = (
                temp_score * 0.3 +
                hum_score * 0.2 +
                ph_score * 0.2 +
                rain_score * 0.3
            )
            
            # Keep track of best crop
            if total_score > best_score:
                best_score = total_score
                best_crop = name
                best_details = {
                    'id': crop_id,
                    'name': name,
                    'description': desc,
                    'ideal_temperature': ideal_temp,
                    'ideal_humidity': ideal_hum,
                    'ideal_ph': ideal_ph_range,
                    'ideal_rainfall': ideal_rain,
                    'growing_season': season,
                    'image_url': img,
                    'match_score': round(total_score, 2),
                    'temp_match': round(temp_score, 2),
                    'humidity_match': round(hum_score, 2),
                    'ph_match': round(ph_score, 2),
                    'rainfall_match': round(rain_score, 2)
                }
        
        return best_crop, best_score, best_details
    
    def get_top_recommendations(self, nitrogen, phosphorus, potassium, 
                                temperature, humidity, ph, rainfall, top_n=5):
        """
        Get top N crop recommendations
        Returns: list of (crop_name, score, details)
        """
        cur = self.mysql.connection.cursor(DictCursor)
        
        cur.execute("""
            SELECT id, name, description, ideal_temperature, ideal_humidity, 
                   ideal_ph, ideal_rainfall, growing_season, image_url
            FROM crops
            ORDER BY name
        """)
        
        all_crops = cur.fetchall()
        cur.close()
        
        recommendations = []
        
        for crop in all_crops:
            # Access dictionary values
            crop_id = crop['id']
            name = crop['name']
            desc = crop['description']
            ideal_temp = crop['ideal_temperature']
            ideal_hum = crop['ideal_humidity']
            ideal_ph_range = crop['ideal_ph']
            ideal_rain = crop['ideal_rainfall']
            season = crop['growing_season']
            img = crop['image_url']
            
            temp_min, temp_max = self.parse_range(ideal_temp)
            hum_min, hum_max = self.parse_range(ideal_hum)
            ph_min, ph_max = self.parse_range(ideal_ph_range)
            rain_min, rain_max = self.parse_range(ideal_rain)
            
            temp_score = self.calculate_score(temperature, temp_min, temp_max)
            hum_score = self.calculate_score(humidity, hum_min, hum_max)
            ph_score = self.calculate_score(ph, ph_min, ph_max)
            rain_score = self.calculate_score(rainfall, rain_min, rain_max)
            
            total_score = (
                temp_score * 0.3 +
                hum_score * 0.2 +
                ph_score * 0.2 +
                rain_score * 0.3
            )
            
            details = {
                'id': crop_id,
                'name': name,
                'description': desc,
                'ideal_temperature': ideal_temp,
                'ideal_humidity': ideal_hum,
                'ideal_ph': ideal_ph_range,
                'ideal_rainfall': ideal_rain,
                'growing_season': season,
                'image_url': img,
                'match_score': round(total_score, 2)
            }
            
            recommendations.append((name, total_score, details))
        
        # Sort by score and return top N
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:top_n]
