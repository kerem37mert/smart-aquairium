import pygame
import random
import math
import uuid

class Fish:
    """Animasyonlu balık sınıfı"""
    
    def __init__(self, x, y, color, size=30, species=None, age=None, gender=None):
        self.id = str(uuid.uuid4())[:8]  # Benzersiz ID
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.species = species or random.choice(["Japon Balığı", "Guppy", "Neon Tetra", "Molly", "Platy"])
        self.age = age or random.randint(3, 24)  # Ay cinsinden (3-24 ay)
        self.gender = gender or random.choice(["Erkek", "Dişi"])
        self.health = "Sağlıklı"  # Varsayılan sağlık durumu
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-0.5, 0.5)
        self.direction = 1 if self.speed_x > 0 else -1
        self.animation_offset = random.uniform(0, 2 * math.pi)
        self.time = 0
        
    def update(self, tank_bounds):
        """Balık pozisyonunu güncelle"""
        self.time += 0.1
        
        # Hareket
        self.x += self.speed_x
        self.y += self.speed_y + math.sin(self.time + self.animation_offset) * 0.3
        
        # Tank sınırlarında geri dön
        if self.x < tank_bounds['left'] + self.size:
            self.x = tank_bounds['left'] + self.size
            self.speed_x = abs(self.speed_x)
            self.direction = 1
        elif self.x > tank_bounds['right'] - self.size:
            self.x = tank_bounds['right'] - self.size
            self.speed_x = -abs(self.speed_x)
            self.direction = -1
            
        if self.y < tank_bounds['top'] + self.size:
            self.y = tank_bounds['top'] + self.size
            self.speed_y = abs(self.speed_y)
        elif self.y > tank_bounds['bottom'] - self.size:
            self.y = tank_bounds['bottom'] - self.size
            self.speed_y = -abs(self.speed_y)
    
    def draw(self, screen):
        """Balığı çiz"""
        # Balık gövdesi (oval)
        body_rect = pygame.Rect(
            int(self.x - self.size),
            int(self.y - self.size // 2),
            self.size * 2,
            self.size
        )
        pygame.draw.ellipse(screen, self.color, body_rect)
        
        # Kuyruk
        tail_points = [
            (int(self.x - self.size * self.direction), int(self.y)),
            (int(self.x - self.size * 1.5 * self.direction), int(self.y - self.size // 2)),
            (int(self.x - self.size * 1.5 * self.direction), int(self.y + self.size // 2))
        ]
        pygame.draw.polygon(screen, self.color, tail_points)
        
        # Göz
        eye_x = int(self.x + self.size * 0.5 * self.direction)
        eye_y = int(self.y - self.size // 4)
        pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), self.size // 6)
        pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), self.size // 10)
        
        # Yüzgeç (animasyonlu)
        fin_offset = math.sin(self.time * 2 + self.animation_offset) * 5
        fin_points = [
            (int(self.x), int(self.y - self.size // 2 + fin_offset)),
            (int(self.x - self.size // 3 * self.direction), int(self.y - self.size + fin_offset)),
            (int(self.x + self.size // 3 * self.direction), int(self.y - self.size + fin_offset))
        ]
        pygame.draw.polygon(screen, self.color, fin_points)


class FishTank:
    """Balık tankı yöneticisi"""
    
    def __init__(self, bounds):
        self.bounds = bounds
        self.fishes = []
        self.food_particles = []  # Yem parçacıkları
        self.create_initial_fishes()
    
    def create_initial_fishes(self):
        """Başlangıç balıklarını oluştur"""
        fish_colors = [
            (255, 140, 0),   # Turuncu
            (255, 69, 0),    # Kırmızı-turuncu
            (248, 101, 252), # Pembe
            (255, 215, 0),   # Altın sarısı
            (147, 112, 219), # Mor
            (16, 210, 76),   # Yeşil
        ]
        
        # Başlangıçtaki balıklar
        for i in range(5):
            x = random.randint(
                self.bounds['left'] + 50,
                self.bounds['right'] - 50
            )
            y = random.randint(
                self.bounds['top'] + 50,
                self.bounds['bottom'] - 50
            )
            color = random.choice(fish_colors)
            size = random.randint(20, 35)
            self.fishes.append(Fish(x, y, color, size))
    
    def update(self):
        """Tüm balıkları ve yem parçacıklarını güncelle"""
        for fish in self.fishes:
            fish.update(self.bounds)
        
        # Yem parçacıklarını güncelle
        self.food_particles = [f for f in self.food_particles if f['y'] < self.bounds['bottom']]
        for food in self.food_particles:
            food['y'] += food['speed']
    
    def draw(self, screen):
        """Tüm balıkları ve yem parçacıklarını çiz"""
        # Yem parçacıklarını çiz
        for food in self.food_particles:
            pygame.draw.circle(screen, (139, 69, 19), (int(food['x']), int(food['y'])), 4)
            pygame.draw.circle(screen, (160, 82, 45), (int(food['x']), int(food['y'])), 3)
        
        # Balıkları çiz
        for fish in self.fishes:
            fish.draw(screen)
    
    def feed_fish(self):
        """Balıklara yem ver"""
        # Rastgele pozisyonlarda yem parçacıkları oluştur
        for _ in range(15):
            x = random.randint(self.bounds['left'] + 50, self.bounds['right'] - 50)
            y = self.bounds['top']
            speed = random.uniform(1, 2)
            self.food_particles.append({'x': x, 'y': y, 'speed': speed})
    
    def add_fish(self, color=None):
        """Yeni balık ekle"""
        if color is None:
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        
        x = (self.bounds['left'] + self.bounds['right']) // 2
        y = (self.bounds['top'] + self.bounds['bottom']) // 2
        self.fishes.append(Fish(x, y, color))
    
    def get_fish_list(self):
        """Balık listesini JSON formatında döndür"""
        fish_list = []
        for fish in self.fishes:
            fish_data = {
                "id": fish.id,
                "species": fish.species,
                "color": f"#{fish.color[0]:02x}{fish.color[1]:02x}{fish.color[2]:02x}",
                "size": fish.size,
                "age": fish.age,
                "gender": fish.gender,
                "health": fish.health
            }
            fish_list.append(fish_data)
        return fish_list
