import sqlite3

class DB:
    def __init__(self, db_name="aquarium"):
        self.db_path = f"{db_name}.db"
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path) # veritabanı bağlanıtısı

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                fish_count INTEGER,
                ph REAL,
                ammonia REAL,
                nitrite REAL,
                nitrate REAL,
                status TEXT
            )
        ''')

        conn.commit()
        conn.close()

    # TABLOYA İLK SATIRI EKLMEK İÇİN DAHA SONRADAN KULLANILMAYACAK
    def insert_first_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO info (fish_count, ph, ammonia, nitrite, nitrate, status) 
            VALUES(?, ?, ?, ?, ?, ?)
        """, (0, 7, 0, 0, 0, "unkown"))

        conn.commit()
        conn.close()

    def updateData(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()

        fish_count = data.get('fish_count', 0)
        water_quality = data.get('water_quality', {})
        
        ph = water_quality.get('ph', 0.0)
        ammonia = water_quality.get('ammonia', 0.0)
        nitrite = water_quality.get('nitrite', 0.0)
        nitrate = water_quality.get('nitrate', 0.0)
        status = water_quality.get('status', 'Unknown')

        cursor.execute('''
            UPDATE info SET  
            fish_count=?, ph=?, ammonia=?, nitrite=?, nitrate=?, status=?
            WHERE id=1 
        ''', (fish_count, ph, ammonia, nitrite, nitrate, status))

        conn.commit()
        conn.close()