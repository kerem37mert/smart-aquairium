import random

class WaterQuality:
    """Su kalitesi yönetim sınıfı"""
    
    # Eşik değerler
    THRESHOLDS = {
        'ph': {
            'ideal_min': 6.5,
            'ideal_max': 7.5,
            'danger_min': 6.0,
            'danger_max': 8.5
        },
        'ammonia': {  # ppm
            'ideal': 0.0,
            'acceptable': 0.25,
            'warning': 0.5,
            'danger': 1.0
        },
        'nitrite': {  # ppm
            'ideal': 0.0,
            'acceptable': 0.25,
            'warning': 0.5,
            'danger': 1.0
        },
        'nitrate': {  # ppm
            'ideal': 20,
            'acceptable': 40,
            'warning': 80,
            'danger': 100
        }
    }
    
    def __init__(self):
        # Başlangıç değerleri (ideal durumda)
        self.ph = 7.0
        self.ammonia = 0.0
        self.nitrite = 0.0
        self.nitrate = 5.0
        
        # Zaman sayacı
        self.time_counter = 0
    
    def update(self, fish_count):
        """Su kalitesini güncelle (her frame'de çağrılır)"""
        self.time_counter += 1
        
        # Her 60 frame'de bir (yaklaşık 1 saniye)
        if self.time_counter >= 60:
            self.time_counter = 0
            
            # Balık sayısına göre kirlenme
            pollution_rate = fish_count * 0.002
            
            # Amonyak yavaşça artar
            self.ammonia += pollution_rate
            
            # Nitrit amonyaktan oluşur
            if self.ammonia > 0.1:
                self.nitrite += pollution_rate * 0.5
                self.ammonia -= pollution_rate * 0.3  # Amonyak azalır
            
            # Nitrat nitritten oluşur
            if self.nitrite > 0.1:
                self.nitrate += pollution_rate * 0.8
                self.nitrite -= pollution_rate * 0.4  # Nitrit azalır
            
            # pH zamanla hafifçe değişir
            self.ph += random.uniform(-0.05, 0.05)
            
            # Değerleri sınırla
            self.ammonia = max(0, min(self.ammonia, 2.0))
            self.nitrite = max(0, min(self.nitrite, 2.0))
            self.nitrate = max(0, min(self.nitrate, 150))
            self.ph = max(5.5, min(self.ph, 9.0))
    
    def feed_impact(self):
        """Yem verildiğinde su kalitesine etkisi"""
        self.ammonia += 0.15  # Yem amonyak üretir
        self.nitrate += 0.5
    
    def change_water(self):
        """Su değişimi - değerleri sıfırla"""
        self.ammonia = 0.0
        self.nitrite = 0.0
        self.nitrate = 5.0
        self.ph = 7.0
    
    def get_status(self):
        """Su durumunu değerlendir"""
        # Kritik durumları kontrol et
        if (self.ammonia >= self.THRESHOLDS['ammonia']['danger'] or
            self.nitrite >= self.THRESHOLDS['nitrite']['danger'] or
            self.nitrate >= self.THRESHOLDS['nitrate']['danger'] or
            self.ph < self.THRESHOLDS['ph']['danger_min'] or
            self.ph > self.THRESHOLDS['ph']['danger_max']):
            return 'DANGER'  # Kırmızı
        
        # Uyarı durumları
        if (self.ammonia >= self.THRESHOLDS['ammonia']['warning'] or
            self.nitrite >= self.THRESHOLDS['nitrite']['warning'] or
            self.nitrate >= self.THRESHOLDS['nitrate']['warning'] or
            self.ph < self.THRESHOLDS['ph']['ideal_min'] or
            self.ph > self.THRESHOLDS['ph']['ideal_max']):
            return 'WARNING'  # Sarı
        
        # Her şey normal
        return 'GOOD'  # Yeşil
    
    def get_status_text(self):
        """Durum metnini döndür"""
        status = self.get_status()
        if status == 'DANGER':
            return 'KİRLİ - ACİL SU DEĞİŞİMİ!'
        elif status == 'WARNING':
            return 'ORTA - SU DEĞİŞİMİ ÖNERİLİR'
        else:
            return 'TEMİZ - İYİ DURUMDA'
    
    def get_status_color(self):
        """Durum rengini döndür"""
        status = self.get_status()
        if status == 'DANGER':
            return (220, 50, 50)  # Kırmızı
        elif status == 'WARNING':
            return (220, 180, 50)  # Sarı
        else:
            return (50, 200, 100)  # Yeşil
