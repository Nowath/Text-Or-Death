import pygame

class SplashScreen:
    def __init__(self, screen, logo_path='assets/images/logo.png', duration=2000):
        """
        Args:
            screen: pygame display surface
            logo_path: path to logo image
            duration: time to show logo at full opacity (milliseconds)
        """
        self.screen = screen
        self.duration = duration
        self.fade_speed = 5  # จำนวน alpha เพิ่มต่อ frame

        try:
            self.logo = pygame.image.load(logo_path).convert_alpha()
            # Resize logo ถ้าต้องการ
            self.logo = pygame.transform.scale(self.logo, (400, 400))
        except:
            # สร้าง placeholder ถ้าไม่มีไฟล์
            self.logo = pygame.Surface((300, 300))
            self.logo.fill((100, 100, 255))
            font = pygame.font.Font(None, 48)
            text = font.render("YOUR LOGO", True, (255, 255, 255))
            text_rect = text.get_rect(center=(150, 150))
            self.logo.blit(text, text_rect)

        # Center logo
        screen_rect = screen.get_rect()
        self.logo_rect = self.logo.get_rect(center=screen_rect.center)

    def show(self):
        """
        Display splash screen with fade in/out animation
        Returns: True if completed normally, False if user quit
        """
        clock = pygame.time.Clock()
        fade_surface = self.logo.copy()

        # Fade in
        if not self._fade_in(fade_surface, clock):
            return False

        # Hold at full opacity
        pygame.time.wait(self.duration)

        # Check for quit during hold
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # Fade out
        if not self._fade_out(fade_surface, clock):
            return False

        return True

    def _fade_in(self, fade_surface, clock):
        """Fade in animation"""
        for alpha in range(0, 256, self.fade_speed):
            # Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                # Skip on any key/click
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return True

            # Render
            self.screen.fill((0, 0, 0))  # Black background
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, self.logo_rect)
            pygame.display.flip()
            clock.tick(60)

        return True

    def _fade_out(self, fade_surface, clock):
        """Fade out animation"""
        for alpha in range(255, 0, -self.fade_speed):
            # Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                # Skip on any key/click
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return True

            # Render
            self.screen.fill((0, 0, 0))
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, self.logo_rect)
            pygame.display.flip()
            clock.tick(60)

        return True
