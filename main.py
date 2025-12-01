import pygame
import sys
from aquarium import Aquarium
from fish import FishTank
from water_quality import WaterQuality

import ws_client 

####### Renkler #######
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
PANEL_BG = (240, 240, 245)
#######################

class AquariumSimulator:
    """ Ana Simülatör sınıfı """
    def __init__(self, title):
        pygame.init()

        # Ekran Ayarları
        self.width = 1200
        self.height = 700
        self.title = title

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title) # Programın başlığını ayarla

        # Font Ayarları
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 22)

        # Akvaryum
        self.aquarium = Aquarium(50, 100, 700, 500)

        # Balıklar
        self.fish_tank = FishTank(self.aquarium.get_bounds())

        # Su Kalitesi
        self.water_quality = WaterQuality()

        # Saat
        self.clock = pygame.time.Clock()
        self.running = True

    def draw_panel(self):
        """Sağ taraftaki kontrol panelini çiz"""
        panel_width = 350
        panel_x = self.width - panel_width

        # Panel arka planı
        pygame.draw.rect(self.screen, PANEL_BG, 
                        (panel_x, 0, panel_width, self.height))
        
        # Başlık
        title = self.font_large.render("Kontrol Paneli", True, DARK_GRAY)
        text_x = panel_x + (panel_width - title.get_width()) // 2   # Metnin ortası
        self.screen.blit(title, (text_x, 30))

        # Balık Sayısı Bilgisi
        y_offset = 100
        
        # Bilgi kutusu arka planı
        info_box = pygame.Rect(panel_x + 20, y_offset, panel_width - 40, 80)
        pygame.draw.rect(self.screen, WHITE, info_box, border_radius=10)
        pygame.draw.rect(self.screen, (100, 150, 200), info_box, 3, border_radius=10)
        
        # Balık sayısı etiketi
        fish_label = self.font_medium.render("Balık Sayısı:", True, DARK_GRAY)
        self.screen.blit(fish_label, (panel_x + 40, y_offset + 15))
        
        # Balık sayısı değeri
        fish_count = len(self.fish_tank.fishes)
        fish_value = self.font_large.render(str(fish_count), True, (0, 100, 200))
        self.screen.blit(fish_value, (panel_x + 40, y_offset + 45))
        
        # Yem Verme Butonu
        y_offset = 200
        button_width = panel_width - 40
        button_height = 60
        
        self.feed_button = pygame.Rect(panel_x + 20, y_offset, button_width, button_height)
        
        # Buton rengi (hover efekti için mouse pozisyonunu kontrol et)
        mouse_pos = pygame.mouse.get_pos()
        if self.feed_button.collidepoint(mouse_pos):
            button_color = (80, 180, 100)  # Hover rengi
        else:
            button_color = (60, 160, 80)   # Normal rengi
        
        # Butonu çiz
        pygame.draw.rect(self.screen, button_color, self.feed_button, border_radius=10)
        pygame.draw.rect(self.screen, (40, 120, 60), self.feed_button, 3, border_radius=10)
        
        # Buton metni
        feed_text = self.font_medium.render("Yem Ver", True, WHITE)
        text_rect = feed_text.get_rect(center=self.feed_button.center)
        self.screen.blit(feed_text, text_rect)

        # Su Kalitesi Göstergesi
        y_offset = 290
        
        # Su kalitesi kutusu
        water_box = pygame.Rect(panel_x + 20, y_offset, panel_width - 40, 200)
        pygame.draw.rect(self.screen, WHITE, water_box, border_radius=10)
        pygame.draw.rect(self.screen, (100, 150, 200), water_box, 3, border_radius=10)
        
        # Başlık
        water_title = self.font_medium.render("Su Kalitesi", True, DARK_GRAY)
        self.screen.blit(water_title, (panel_x + 40, y_offset + 15))
        
        # Durum göstergesi
        status_text = self.water_quality.get_status_text()
        status_color = self.water_quality.get_status_color()
        status_label = self.font_small.render(status_text, True, status_color)
        self.screen.blit(status_label, (panel_x + 40, y_offset + 45))
        
        # Parametreler
        param_y = y_offset + 75
        
        # pH
        ph_text = self.font_small.render(f"pH: {self.water_quality.ph:.1f}", True, DARK_GRAY)
        self.screen.blit(ph_text, (panel_x + 40, param_y))
        
        # Amonyak
        param_y += 30
        ammonia_text = self.font_small.render(f"Amonyak: {self.water_quality.ammonia:.2f} ppm", True, DARK_GRAY)
        self.screen.blit(ammonia_text, (panel_x + 40, param_y))
        
        # Nitrit
        param_y += 30
        nitrite_text = self.font_small.render(f"Nitrit: {self.water_quality.nitrite:.2f} ppm", True, DARK_GRAY)
        self.screen.blit(nitrite_text, (panel_x + 40, param_y))
        
        # Nitrat
        param_y += 30
        nitrate_text = self.font_small.render(f"Nitrat: {self.water_quality.nitrate:.1f} ppm", True, DARK_GRAY)
        self.screen.blit(nitrate_text, (panel_x + 40, param_y))

        # Su Değiştirme Butonu
        y_offset = 510
        button_width = panel_width - 40
        button_height = 60
        
        self.change_water_button = pygame.Rect(panel_x + 20, y_offset, button_width, button_height)
        
        # Buton rengi (hover efekti)
        if self.change_water_button.collidepoint(mouse_pos):
            button_color = (80, 150, 220)  # Hover rengi (açık mavi)
        else:
            button_color = (60, 130, 200)   # Normal rengi (mavi)
        
        # Butonu çiz
        pygame.draw.rect(self.screen, button_color, self.change_water_button, border_radius=10)
        pygame.draw.rect(self.screen, (40, 100, 160), self.change_water_button, 3, border_radius=10)
        
        # Buton metni
        change_water_text = self.font_medium.render("Su Değiştir", True, WHITE)
        text_rect = change_water_text.get_rect(center=self.change_water_button.center)
        self.screen.blit(change_water_text, text_rect)

        # Bİlgilendirme - F
        title = self.font_small.render("F - Balık Ekle", True, DARK_GRAY)
        text_x = panel_x + (panel_width - title.get_width()) // 2   # Metnin ortası
        self.screen.blit(title, (text_x, 600))

        # Bİlgilendirme - ESC
        title = self.font_small.render("ESC - Çıkış", True, DARK_GRAY)
        text_x = panel_x + (panel_width - title.get_width()) // 2   # Metnin ortası
        self.screen.blit(title, (text_x, 630))

    def handle_click(self, pos):
        """Mouse tıklamalarını işle"""
        # Yem verme butonuna tıklandı mı?
        if hasattr(self, 'feed_button') and self.feed_button.collidepoint(pos):
            self.fish_tank.feed_fish()
            self.water_quality.feed_impact()  # Su kalitesine etkisi
        
        # Su değiştirme butonuna tıklandı mı?
        if hasattr(self, 'change_water_button') and self.change_water_button.collidepoint(pos):
            self.water_quality.change_water()  # Suyu değiştir
    
    def run(self):
        # Websocket başlat
        ws_client.ws_thread.start()

        """Ana döngü"""
        while self.running:
            # Olayları işle
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: #esc
                        self.running = False
                    elif event.key == pygame.K_f: #f
                        # Yeni balık ekle
                        self.fish_tank.add_fish()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            # Güncelle (Hareket ermeleri için)
            self.aquarium.update()
            self.fish_tank.update()
            
            # Su kalitesini güncelle
            fish_count = len(self.fish_tank.fishes)
            self.water_quality.update(fish_count)
            
            # Çiz
            self.screen.fill(WHITE)
            
            # Başlık
            title = self.font_large.render("Akvaryum", True, DARK_GRAY)
            text_x = (850 - title.get_width()) // 2   # Metnin ortası
            self.screen.blit(title, (text_x, 30))

            # Akvaryum ve balıkları çiz
            self.aquarium.draw(self.screen)
            self.fish_tank.draw(self.screen)

            # Kontrol panelini çiz
            self.draw_panel()

            aquarium_data = {
                "fish_count": len(self.fish_tank.fishes),
                "water_quality": {
                    "ph": self.water_quality.ph,
                    "ammonia": self.water_quality.ammonia,
                    "nitrite": self.water_quality.nitrite,
                    "nitrate": self.water_quality.nitrate,
                    "status": self.water_quality.get_status_text()
                },
                "timestamp": pygame.time.get_ticks()
            }

            # WebSocket üzerinden gönder
            ws_client.send_data(aquarium_data)

            # Ekranı güncelle
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()
        sys.exit()

# Programı Çalıştır
if __name__ == "__main__":
    simulator = AquariumSimulator(title="Akıllı Akvaryum")
    simulator.run()