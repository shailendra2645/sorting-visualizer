import pygame.mixer
import pygame
import sys
import numpy as np

pygame.init()

screen = pygame.display.set_mode((0, 0), flags=pygame.RESIZABLE)
clock = pygame.time.Clock()


class BubbleSort:
    def __init__(self, n: int, rect_gap=0.8, padding=10):
        self.array = np.linspace(0.1, 0.95, n)
        self.array = self.array[::-1]
        # np.random.shuffle(self.array)
        self.b_array = self.array.copy()
        self.i_array = self.array.copy()
        self.N = len(self.array)
        self.rect_gap = rect_gap
        self.padding = padding

        self.icomparisions = 0
        self.iswap = 0
        self.bcomparisions = 0
        self.bswap = 0
        self.bubble_sort_completed = False
        self.insertion_sort_completed = False
        self.current_indices = None
        self.icurrent_indices = None
        self.bcurrent_indices = None

    def bubble_sort_gen(self):
        for i in range(len(self.b_array)):
            swapped = False
            for j in range(len(self.b_array) - i - 1):
                self.bcurrent_indices = (j, j + 1)
                self.bcomparisions += 1
                if self.b_array[j] > self.b_array[j + 1]:
                    self.bswap += 1
                    swapped = True
                    self.b_array[j], self.b_array[j + 1] = (
                        self.b_array[j + 1], self.b_array[j])
                    yield
            yield
            if not swapped:
                break
        self.bubble_sort_completed = True
        self.bcurrent_indices = None

    def insertion_sort_gen(self):
        for i in range(1, self.N):
            current = self.i_array[i]
            j = i - 1
            self.icurrent_indices = (j, j + 1)
            while current < self.i_array[j] and j >= 0:
                self.icomparisions += 1
                self.iswap += 1
                self.icurrent_indices = (j, j + 1)
                self.i_array[j + 1] = self.i_array[j]
                j -= 1
                yield
            yield
            self.i_array[j + 1] = current

        self.icurrent_indices = None
        self.insertion_sort_completed = True

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    def draw_both(self):
        total_rect_width = (screen.get_width() - 2*self.padding) / self.N
        for i in range(self.N):
            w = total_rect_width - 2*self.rect_gap
            left = (self.padding + self.rect_gap) + total_rect_width * i
            # Dividing the screen in half to visualize both sorting
            h = (screen.get_height() // 2) - self.padding
            hb = self.b_array[i] * h
            hi = self.i_array[i] * h
            itop = (screen.get_height() - h) - hi  # Drawing at the top
            btop = (screen.get_height()) - hb  # Drawing at the bottom
            top = screen.get_height() - h
            irect = pygame.Rect(left, itop, w, hi)
            brect = pygame.Rect(left, btop, w, hb)
            icolor = "white"
            bcolor = "white"
            if self.icurrent_indices and (i == self.icurrent_indices[0] or i == self.icurrent_indices[1]):
                icolor = "darkblue"
            if self.bcurrent_indices and (i == self.bcurrent_indices[0] or i == self.bcurrent_indices[1]):
                bcolor = "orange"
            if self.bubble_sort_completed:
                bcolor = "skyblue"
            if self.insertion_sort_completed:
                icolor = "skyblue"
            pygame.draw.rect(screen, icolor, irect)
            pygame.draw.rect(screen, bcolor, brect)
        self.display_stats()

    def display_stats(self):
        font = pygame.font.SysFont("monospace", 20, bold=True)
        insertion_text = font.render(
            f"Insertion Sort: swaps={self.iswap} comparisons={self.icomparisions}", True, "lightgreen")
        bubble_text = font.render(
            f"Bubble Sort: swaps={self.bswap} comparisons={self.bcomparisions}", True, "lightgreen")
        screen.blit(insertion_text, (10, 5))
        screen.blit(bubble_text, (10, screen.get_height()//2 + self.padding))

    def draw(self):
        total_rect_width = (screen.get_width() - 2*self.padding) / self.N
        for i, h in enumerate(self.array):
            w = total_rect_width - 2*self.rect_gap
            h = h * screen.get_height()
            left = (self.padding + self.rect_gap) + total_rect_width * i
            top = screen.get_height() - h
            rect = pygame.Rect(left, top, w, h)
            color = "white"
            if self.current_indices and (i == self.current_indices[0] or i == self.current_indices[1]):
                color = "darkblue"
            pygame.draw.rect(screen, color, rect)


simulation = BubbleSort(100, 0.8, padding=20)
insertion_gen = simulation.insertion_sort_gen()
bubble_gen = simulation.bubble_sort_gen()
while True:
    simulation.check_events()
    next(insertion_gen, None)
    next(bubble_gen, None)
    screen.fill("black")
    simulation.draw_both()
    pygame.display.flip()
    clock.tick(120)
