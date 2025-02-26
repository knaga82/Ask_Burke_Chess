import pygame
from const import *
import sys

class Popup:
# This class creates a popup window to display text.
#  It needs to be improved in order to have a nicer looking popup.
    def __init__(self, screen):
        self.screen = screen

    def show(self, title, text, num_words):
        if num_words < 50:
            popup_width = 400
            popup_height = 300
        else:
            popup_width = 600
            popup_height = 450
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill((255, 255, 255))
        
        # Create text surfaces with smaller font
        small_font = pygame.font.SysFont('roboto', 28, bold=True)
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if small_font.size(test_line)[0] > popup_width - 40:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))

        # Create close button
        button_rect = pygame.Rect(popup_width//2 - 50, popup_height - 40, 100, 30)
        
        # Main popup loop
        popup_active = True
        scroll_offset = 0
        while popup_active:
            popup_x = (WIDTH - popup_width) // 2
            popup_y = (HEIGHT - popup_height) // 2
            
            self.screen.blit(popup_surface, (popup_x, popup_y))
            pygame.draw.rect(popup_surface, (200, 200, 200), button_rect)
            close_text = small_font.render("Close", True, (0, 0, 0))
            popup_surface.blit(close_text, (button_rect.centerx - close_text.get_width()//2, 
                                          button_rect.centery - close_text.get_height()//2))
            
            # Display text with scrolling
            y_offset = 20 - scroll_offset

            for line in lines:
                text_surface = small_font.render(line, True, (0, 0, 0))
                popup_surface.blit(text_surface, (20, y_offset))
                y_offset += 30

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    adjusted_pos = (mouse_pos[0] - popup_x, mouse_pos[1] - popup_y)
                    if button_rect.collidepoint(adjusted_pos):
                        popup_active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        popup_active = False
                if event.type == pygame.MOUSEWHEEL:
                    scroll_offset += event.y * 10
                    scroll_offset = max(0, min(scroll_offset, max(0, y_offset - popup_height + 40)))
            
            pygame.display.flip()