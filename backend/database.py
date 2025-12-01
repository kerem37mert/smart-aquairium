import sqlite3
import json
from datetime import datetime
from pathlib import Path

class AquariumDatabase:
    """Akvaryum verilerini SQLite'a kaydeden sınıf"""
    
    def __init__(self, db_path="aquarium_data.db"):
        """
        Veritabanı bağlantısını başlat
        
        Args:
            db_path: Veritabanı dosyasının yolu
        """
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Veritabanı bağlantısı oluştur"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Veritabanı tablolarını oluştur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Ana veri tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS aquarium_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                fish_count INTEGER,
                ph REAL,
                ammonia REAL,
                nitrite REAL,
                nitrate REAL,
                status TEXT,
                raw_data TEXT
            )
        ''')
        
        # İndeksler (hızlı sorgulama için)
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON aquarium_data(timestamp)
        ''')
        
        conn.commit()
        conn.close()
        print(f"✓ Veritabanı hazır: {self.db_path}")
    
    def save_aquarium_data(self, data):
        """
        Akvaryum verilerini kaydet
        
        Args:
            data: Client'tan gelen veri dictionary'si
                {
                    "fish_count": int,
                    "water_quality": {
                        "ph": float,
                        "ammonia": float,
                        "nitrite": float,
                        "nitrate": float,
                        "status": str
                    },
                    "timestamp": int
                }
        
        Returns:
            int: Kaydedilen verinin ID'si
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Veriyi parse et
            fish_count = data.get('fish_count', 0)
            water_quality = data.get('water_quality', {})
            
            ph = water_quality.get('ph', 0.0)
            ammonia = water_quality.get('ammonia', 0.0)
            nitrite = water_quality.get('nitrite', 0.0)
            nitrate = water_quality.get('nitrate', 0.0)
            status = water_quality.get('status', 'Unknown')
            
            # Ham veriyi JSON olarak sakla
            raw_data = json.dumps(data, ensure_ascii=False)
            
            # Veritabanına kaydet
            cursor.execute('''
                INSERT INTO aquarium_data 
                (fish_count, ph, ammonia, nitrite, nitrate, status, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (fish_count, ph, ammonia, nitrite, nitrate, status, raw_data))
            
            conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            
            return last_id
            
        except Exception as e:
            print(f"❌ Veritabanına kaydetme hatası: {e}")
            return None
    
    def get_latest_data(self, limit=10):
        """
        En son kaydedilen verileri getir
        
        Args:
            limit: Getirilecek kayıt sayısı
            
        Returns:
            list: Veri listesi
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, fish_count, ph, ammonia, nitrite, nitrate, status
            FROM aquarium_data
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Dictionary formatına çevir
        results = []
        for row in rows:
            results.append({
                'id': row[0],
                'timestamp': row[1],
                'fish_count': row[2],
                'ph': row[3],
                'ammonia': row[4],
                'nitrite': row[5],
                'nitrate': row[6],
                'status': row[7]
            })
        
        return results
    
    def get_data_by_date_range(self, start_date, end_date):
        """
        Tarih aralığına göre verileri getir
        
        Args:
            start_date: Başlangıç tarihi (YYYY-MM-DD formatında)
            end_date: Bitiş tarihi (YYYY-MM-DD formatında)
            
        Returns:
            list: Veri listesi
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, fish_count, ph, ammonia, nitrite, nitrate, status
            FROM aquarium_data
            WHERE DATE(timestamp) BETWEEN ? AND ?
            ORDER BY timestamp DESC
        ''', (start_date, end_date))
        
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            results.append({
                'id': row[0],
                'timestamp': row[1],
                'fish_count': row[2],
                'ph': row[3],
                'ammonia': row[4],
                'nitrite': row[5],
                'nitrate': row[6],
                'status': row[7]
            })
        
        return results
    
    def get_statistics(self):
        """
        Genel istatistikleri getir
        
        Returns:
            dict: İstatistik bilgileri
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_records,
                AVG(fish_count) as avg_fish_count,
                AVG(ph) as avg_ph,
                AVG(ammonia) as avg_ammonia,
                AVG(nitrite) as avg_nitrite,
                AVG(nitrate) as avg_nitrate,
                MIN(timestamp) as first_record,
                MAX(timestamp) as last_record
            FROM aquarium_data
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        return {
            'total_records': row[0],
            'avg_fish_count': round(row[1], 2) if row[1] else 0,
            'avg_ph': round(row[2], 2) if row[2] else 0,
            'avg_ammonia': round(row[3], 4) if row[3] else 0,
            'avg_nitrite': round(row[4], 4) if row[4] else 0,
            'avg_nitrate': round(row[5], 2) if row[5] else 0,
            'first_record': row[6],
            'last_record': row[7]
        }
    
    def clear_old_data(self, days=30):
        """
        Eski verileri temizle
        
        Args:
            days: Kaç günden eski veriler silinecek
            
        Returns:
            int: Silinen kayıt sayısı
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM aquarium_data
            WHERE timestamp < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"✓ {deleted_count} eski kayıt silindi")
        return deleted_count
