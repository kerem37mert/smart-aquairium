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
                temperature REAL,
                status TEXT
            )
        ''')
        
        # Kullanıcı tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Basit migrasyon: temperature sütunu yoksa ekle
        try:
            cursor.execute("ALTER TABLE info ADD COLUMN temperature REAL DEFAULT 25.0")
        except sqlite3.OperationalError:
            # Sütun zaten varsa hata verir, yoksay
            pass
        
        # Varsayılan kullanıcı ekle (eğer yoksa)
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', ('admin', 'admin123'))

        conn.commit()
        conn.close()

    # TABLOYA İLK SATIRI EKLMEK İÇİN DAHA SONRADAN KULLANILMAYACAK
    def insert_first_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO info (fish_count, ph, ammonia, nitrite, nitrate, temperature, status) 
            VALUES(?, ?, ?, ?, ?, ?, ?)
        """, (0, 7, 0, 0, 0, 25.0, "unkown"))

        conn.commit()
        conn.close()

    # Güncelleme
    def updateData(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()

        fish_count = data.get('fish_count', 0)
        water_quality = data.get('water_quality', {})
        
        ph = water_quality.get('ph', 0.0)
        ammonia = water_quality.get('ammonia', 0.0)
        nitrite = water_quality.get('nitrite', 0.0)
        nitrate = water_quality.get('nitrate', 0.0)
        temperature = water_quality.get('temperature', 25.0)
        status = water_quality.get('status', 'Unknown')

        cursor.execute('''
            UPDATE info SET  
            fish_count=?, ph=?, ammonia=?, nitrite=?, nitrate=?, temperature=?, status=?
            WHERE id=1 
        ''', (fish_count, ph, ammonia, nitrite, nitrate, temperature, status))

        conn.commit()
        conn.close()

    # Veri Çekme
    def getData(self):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM info WHERE id=1")
        row = cursor.fetchone()

        conn.close()

        if row is None:
            return {}
        
        return dict(row)
    
    def verify_user(self, username, password):
        """Kullanıcı doğrulaması"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM users
            WHERE username = ? AND password = ?
        ''', (username, password))
        
        result = cursor.fetchone()
        conn.close()
        
        return result is not None