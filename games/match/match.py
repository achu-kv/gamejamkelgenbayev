import pygame
import os
import random
import time


class Match:
    def __init__(self):
        # 36 blocks for sq grid
        self.total = 36
        self.side = 6
        self.size = 610
        self.__loop()

    def __path_to(self, f):
        return os.path.join(os.getcwd(), 'games', 'match', 'sprites', f)

    def __loop(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.size + 200, self.size))
        self.clock = pygame.time.Clock()

        self.__load_imgs()
        self.__generate_field()
        self.state = 0
        self.pressed = []
        self.ignore = set()
        self.win = False

        self.__game()

    def __game(self):
        self.screen.blit(self.bgimg, (-600, -350))
        while True:
            if self.win:
                self.__draw_win()
                return # placeholder
            
            self.__draw_blocks()
            if self.state == 2:
                if self.pressed[0][-1] == self.pressed[1][-1]:
                    self.ignore.update(self.pressed)
                    # play audio or something
                    
                time.sleep(1)
                self.__draw_blocks()
                self.pressed.clear()
                self.state = 0
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_o:
                        self.win = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(self.surfaces)):
                        rect = self.surfaces[i]
                        if rect.collidepoint(event.pos):
                            crd = self.sprite_id[i // self.side][i % self.side]
                            if crd not in self.pressed:
                                self.state += 1
                                self.pressed.append(crd)
                                self.__draw_img(crd[-1], rect)
            pygame.display.flip()
            self.__win_check()
                
    # tmp
    def __draw_img(self, i, rect):
        self.screen.blit(self.imgs[i], rect)

    def __load_imgs(self):
        self.imgs = []
        self.bgimg = pygame.image.load(self.__path_to('bg.png'))
        
        for i in range(0, self.total // 2):
            img = pygame.image.load(self.__path_to(f'Page {i + 1}.jpeg')).convert_alpha()
            img = pygame.transform.scale(img, (90, 90))
            self.imgs.append(img)
            # self.imgs.append(pygame.image.load(self.__path_to(f'page-{i}.jpeg')).convert_alpha())
    
    def __draw_blocks(self):
        
        for i in range(len(self.surfaces)):
            crd = self.sprite_id[i // self.side][i % self.side]
            if crd not in self.ignore and crd not in self.pressed:
                pygame.draw.rect(self.screen, (33, 121, 1), self.surfaces[i])
        
    
    def __win_check(self):
        if len(self.ignore) == self.total:
            self.win = True
    
    def __draw_win(self):
        winimg = pygame.image.load(self.__path_to('win.jpg'))
        rt = winimg.get_rect()
        winimg = pygame.transform.scale(winimg, (1000, 563))
        pygame.display.set_mode((1000, 563))
        self.screen.blit(winimg,  rt)
        pygame.display.flip()

    def __generate_field(self):
        dif = self.total // 2
        used = {}
        self.colors = [(255, 0, 0) for _ in range(self.total)]
        self.sprite_id = []
        self.surfaces = []
        k = 0
        for i in range(self.side):
            tmp = []
            for j in range(self.side):
                t = True
                while 1 and t:
                    genid = random.randint(0, dif - 1)
                    if genid not in used or used[genid] == 1:
                        if genid not in used:
                            used[genid] = 0
                        used[genid] += 1
                        tmp.append((i, j, genid))
                        t = False
                        k += 1
                    elif k == self.total:
                        break
                    else:
                        continue
                self.surfaces.append(pygame.Rect(10 + 100 * i, 10 + 100 * j, 90, 90))
            self.sprite_id.append(tmp)