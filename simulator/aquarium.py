import pygame
import random
import math

class Bubble:
    """Su baloncuğu"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 6)
        self.speed = random.uniform(0.5, 1.5)
        self.wobble = random.uniform(0, 2 * math.pi)
        self.wobble_speed = random.uniform(0.05, 0.15)
    
    def update(self):
        """Kabarcığı yukarı hareket ettir"""
        self.y -= self.speed
        self.wobble += self.wobble_speed
        self.x += math.sin(self.wobble) * 0.5
        return self.y > 0  # Ekrandan çıktıysa False döner
    
    def draw(self, screen):
        """Kabarcığı çiz"""
        pygame.draw.circle(screen, (200, 230, 255, 100), 
                         (int(self.x), int(self.y)), self.radius, 1)


class Plant:
    """Akvaryum bitkisi"""
    
    def __init__(self, x, y, height, color):
        self.x = x
        self.y = y
        self.height = height
        self.color = color
        self.segments = 8
        self.time = random.uniform(0, 2 * math.pi)
        self.sway_speed = random.uniform(0.02, 0.05)
    
    def update(self):
        """Bitki sallanmasını güncelle"""
        self.time += self.sway_speed
    
    def draw(self, screen):
        """Bitkiyi çiz (dalgalanan)"""
        segment_height = self.height / self.segments
        
        for i in range(self.segments):
            # Her segment için sallanma hesapla
            sway = math.sin(self.time + i * 0.3) * (i * 2)
            
            y_pos = self.y - i * segment_height
            x_pos = self.x + sway
            
            # Yaprak çiz
            leaf_width = 15 - i * 1.5
            leaf_height = segment_height * 1.5
            
            # Sol yaprak
            left_points = [
                (x_pos, y_pos),
                (x_pos - leaf_width, y_pos - leaf_height // 2),
                (x_pos, y_pos - leaf_height)
            ]
            pygame.draw.polygon(screen, self.color, left_points)
            
            # Sağ yaprak
            right_points = [
                (x_pos, y_pos),
                (x_pos + leaf_width, y_pos - leaf_height // 2),
                (x_pos, y_pos - leaf_height)
            ]
            pygame.draw.polygon(screen, self.color, right_points)


class Aquarium:
    """Akvaryum ana sınıfı"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bubbles = [] # baloncuklar
        self.plants = []  # bitkiler
        self.bubble_timer = 0
        self.create_plants()

        # Su rengi (gradient için)
        self.water_color_top = (100, 180, 220)
        self.water_color_bottom = (50, 120, 180)

    def create_plants(self):
        """Bitkileri oluştur"""
        plant_positions = [
            (self.x + 50, self.y + self.height),
            (self.x + 150, self.y + self.height),
            (self.x + self.width - 150, self.y + self.height),
            (self.x + self.width - 50, self.y + self.height),
        ]
        
        plant_colors = [
            (34, 139, 34),   # Koyu yeşil
            (50, 205, 50),   # Açık yeşil
            (46, 125, 50),   # Orman yeşili
        ]
        
        for pos_x, pos_y in plant_positions:
            height = random.randint(80, 140)
            color = random.choice(plant_colors)
            self.plants.append(Plant(pos_x, pos_y, height, color))

    def update(self):
        """Akvaryum elementlerini güncelle"""
        # Bitkileri güncelle
        for plant in self.plants:
            plant.update()

        # Kabarcıkları güncelle
        self.bubbles = [b for b in self.bubbles if b.update()]
        
        # Yeni kabarcık oluştur
        self.bubble_timer += 1
        if self.bubble_timer > 20:
            self.bubble_timer = 0
            # Rastgele pozisyonda kabarcık oluştur
            bubble_x = random.randint(self.x + 20, self.x + self.width - 20)
            self.bubbles.append(Bubble(bubble_x, self.y + self.height - 10))

    def draw(self, screen):
        """Akvaryumu çiz"""
        
        # Su gradient efekti
        for i in range(self.height):
            ratio = i / self.height
            color = (
                int(self.water_color_top[0] * (1 - ratio) + self.water_color_bottom[0] * ratio),
                int(self.water_color_top[1] * (1 - ratio) + self.water_color_bottom[1] * ratio),
                int(self.water_color_top[2] * (1 - ratio) + self.water_color_bottom[2] * ratio)
            )

            pygame.draw.line(screen, color, 
                           (self.x, self.y + i), 
                           (self.x + self.width, self.y + i))
        
        # Zemin (kum/çakıl)
        ground_height = 30
        pygame.draw.rect(screen, (194, 178, 128), 
                        (self.x, self.y + self.height - ground_height, 
                         self.width, ground_height))
        
        # Akvaryum çerçevesi
        pygame.draw.rect(screen, (80, 80, 80), 
                        (self.x, self.y, self.width, self.height), 5)
        
        # Bitkileri çiz
        for plant in self.plants:
            plant.draw(screen)

        # Kabarcıkları çiz
        for bubble in self.bubbles:
            bubble.draw(screen)

    def get_bounds(self):
        """Akvaryum sınırlarını döndür"""
        return {
            'left': self.x + 10,
            'right': self.x + self.width - 10,
            'top': self.y + 10,
            'bottom': self.y + self.height - 40  # Zemin için boşluk
        }