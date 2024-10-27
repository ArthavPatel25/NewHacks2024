import pygame
import sys
import time
import random

class RouletteGame:
    def __init__(self, points):
        pygame.init()
        self.screen_info = pygame.display.Info()
        self.points = points
        self.numbers = []
    
    def getPoints(self):
        return self.points

    def create_board(self, screen, screen_width, screen_height, button_text):
        board_image = pygame.image.load("images/RoulleteBoard.png") 
        board_image = pygame.transform.scale(board_image, (screen_width*(2/3), screen_height//2))

        spin_image = pygame.image.load("images/RoulleteSpin.png")
        spin_image = pygame.transform.scale(spin_image, (screen_width*(1/3), screen_height//2))
        
        screen.fill((0, 138, 61))
        screen.blit(board_image, (screen_width*(1/3), 0))
        screen.blit(spin_image, (0, 0))
        font_points = pygame.font.SysFont("Times New Roman", 70)
        point_text = font_points.render("Points: " + str(self.points), True, (255, 255, 255))
        point_rect = pygame.Rect(100, screen_height/2, 200, 75)
        point_rect = point_text.get_rect(center=point_rect.center)
        screen.blit(point_text, point_rect)
        instruction_points = pygame.font.SysFont("Times New Roman", 30)
        instructions_text = instruction_points.render("Please input number/s with a space in between and nothing else (ex. 2 11)", True, (255, 255, 255))
        instructions_rect = pygame.Rect(screen_width*3/8, screen_height - 150, 500, 150)
        instructions_rect = instructions_text.get_rect(center=instructions_rect.center)
        screen.blit(instructions_text, instructions_rect)
        buttons = []
        height = 50
        width = 175
        for x in range(15):
            if x < 5:
                buttons.append(self.create_button(button_text[x], screen_width/3 + (width + 25)*x, screen_height/2 + 30, screen, height, width))
            elif x < 10:
                buttons.append(self.create_button(button_text[x], screen_width/3 + (width + 25)*(x - 5), screen_height/2 + 30 + 2*height, screen, height, width))
            elif x < 15:
                buttons.append(self.create_button(button_text[x], screen_width/3 + (width + 25)*(x - 10), screen_height/2 + 30 + 4*height, screen, height, width))
        return buttons
    
    def rolling(self, screen, screen_height, screen_width, numbers):
        clear_entire_rect = pygame.Rect(0, screen_height//2, screen_width // 3 - 20, screen_height // 2)
        screen.fill((0, 138, 61), clear_entire_rect)
        font_roll = pygame.font.SysFont("Times New Roman", 70)
        rolling_text =  font_roll.render("Rolling...", True, (255, 255, 255))
        area_rect = pygame.Rect(100, screen_height/2, 200, 75)
        rolling_rect = rolling_text.get_rect(center=area_rect.center)
                
        for x in range(10):
            screen.blit(rolling_text, rolling_rect)
            font = pygame.font.SysFont("Times New Roman", 300)
            number_rolling = font.render(str(random.randrange(37)), True, (255, 255, 255))
            fixed_area_rect = pygame.Rect(100, screen_height - 275, 300, 200) 
            number_place = number_rolling.get_rect(center=fixed_area_rect.center)
            screen.blit(number_rolling, number_place)
            pygame.display.flip()
            time.sleep(0.1)
            clear_rect = pygame.Rect(0, screen_height * 5 // 10 + 100, screen_width // 3 - 20, screen_height // 2)
            screen.fill((0, 138, 61), clear_rect)
        screen.fill((0, 138, 61), clear_entire_rect)
        font_final = pygame.font.SysFont("Times New Roman", 300)
        rand_num = random.randrange(37)
        number_rolling = font_final.render(str(rand_num), True, (255, 255, 255))
        fixed_area_rect = pygame.Rect(100, screen_height - 275, 300, 200) 
        number_place = number_rolling.get_rect(center=fixed_area_rect.center)
        screen.blit(number_rolling, number_place)
        pygame.display.flip()
        time.sleep(1)

        win = False
        for num in numbers:
            if int(num) == rand_num:
                    win = True
        clear_bottom_rect = pygame.Rect(0, screen_height/2, screen_width, screen_height/2)
        screen.fill((1, 138, 61), clear_bottom_rect)
        pygame.display.flip()

        return win

    def req_num(self, numbers, bet_type):
        for x in range(6):
            if bet_type == x:
                if len(numbers) == (x + 1):
                    for x in range(len(numbers) - 1):
                        if int(numbers[x+1]) is not int(numbers[x]) + 1 or int(numbers[x]) > 36 or int(numbers[x + 1]) > 36:
                            return False
                    return True
                else:
                    return False

    def number_type(self, screen, bet_type: int):
        if bet_type == 6:
            return [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        if bet_type == 7: 
            return [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        if bet_type == 8:
            return [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
        if bet_type == 9:
            return [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
        if bet_type == 10:
            return list(range(19, 37))
        if bet_type == 11:
            return list(range(1, 19))
        if bet_type == 12: 
            val = int(self.text_input_box(screen, "Pick a dozen (1, 2, or 3)", self.screen_info.current_w/3, self.screen_info.current_h - 100, self.screen_info.current_w/4, self.screen_info.current_h/10))
            clear_rect = pygame.Rect(self.screen_info.current_w/3, self.screen_info.current_h - 150, self.screen_info.current_w, self.screen_info.current_h/4)
            screen.fill((1, 138, 61), clear_rect)
            while True:
                if val == 1:
                    return list(range(1, 13))
                elif val == 2:
                    return list(range(13, 25))
                elif val == 3:
                    return list(range(25, 17))
                else:
                    val = int(self.text_input_box(screen, "Invalid input, pick a dozen (1, 2, or 3)", self.screen_info.current_w/3, self.screen_info.current_h - 100, self.screen_info.current_w/4, self.screen_info.current_h/10))
                    clear_rect = pygame.Rect(self.screen_info.current_w/3, self.screen_info.current_h - 150, self.screen_info.current_w, self.screen_info.current_h/4)
                    screen.fill((1, 138, 61), clear_rect)
        if bet_type == 13: 
            val = int(self.text_input_box(screen, "Pick a column (1, 2, or 3)", self.screen_info.current_w/3, self.screen_info.current_h - 100, self.screen_info.current_w/4, self.screen_info.current_h/10))
            clear_rect = pygame.Rect(self.screen_info.current_w/3, self.screen_info.current_h - 150, self.screen_info.current_w, self.screen_info.current_h/4)
            screen.fill((1, 138, 61), clear_rect)
            while True:
                if val == 1:
                    return [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
                elif val == 2:
                    return [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
                elif val == 3:
                    return [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]  
                else:
                    val = int(self.text_input_box(screen, "Invalid input, pick a column (1, 2, or 3)", self.screen_info.current_w/3, self.screen_info.current_h - 100, self.screen_info.current_w/4, self.screen_info.current_h/10))
                    clear_rect = pygame.Rect(self.screen_info.current_w/3, self.screen_info.current_h - 150, self.screen_info.current_w, self.screen_info.current_h/4)
                    screen.fill((1, 138, 61), clear_rect)        

    def bet_checker(self, screen, bet_amount, screen_width, screen_height):
        clear_rect = pygame.Rect(screen_width/3, screen_height - 150, screen_width, screen_height/4)
        screen.fill((1, 138, 61), clear_rect)
        bet_amount = self.text_input_box(screen, "All in! Y to confirm: ", screen_width/3, screen_height - 100, screen_width/4, screen_height/10)
        if bet_amount.lower() == ("y"):
            return True  
        else:
            return False

    def point_score(self, bet_amount, bet_type):
        if bet_type == 0:
            self.points = self.points + bet_amount * 35
        if bet_type == 1:
            self.points = self.points + bet_amount * 17
        if bet_type == 2:
            self.points = self.points + bet_amount * 11
        if bet_type == 3:
            self.points = self.points + bet_amount * 8
        if bet_type == 4:
            self.points = self.points + bet_amount * 6
        if bet_type == 5:
            self.points = self.points + bet_amount * 5
        if bet_type == 12 or bet_type == 13:
            self.points = self.points + bet_amount * 2
        else:
            self.points = self.points + bet_amount

    def create_button(self, text : str, pos_x : int, pos_y : int, screen, height : int, width : int):
        button_rect = pygame.Rect(pos_x, pos_y, width, height)
        outline_rect = pygame.Rect(button_rect.left - 2, button_rect.top - 2, button_rect.width + 4, button_rect.height + 4)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect)
        pygame.draw.rect(screen, (0, 138, 61), button_rect)
        font = pygame.font.SysFont("Times New Roman", 20)
        button_text = font.render(text, True, (255, 255, 255))
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)
        return button_rect
    
    def text_input_box(self, screen, prompt : str, pos_x, pos_y, width, height):
        font = pygame.font.SysFont("Times New Roman", 30)
        input_rect = pygame.Rect(pos_x + 600, pos_y - 20, width, height)
        active = False
        input_text = ''
        color = (255, 255, 255)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                        color = (180, 180, 180)
                    else:
                        active = False
                        color = (255, 255, 255)
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            return input_text  
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = '' 
                            screen.fill((0, 138, 61), input_rect)
                        else:
                            input_text += event.unicode  

            prompt_text = font.render(prompt, True, (255, 255, 255))
            screen.blit(prompt_text, (pos_x, pos_y))

            txt_surface = font.render(input_text, True, (255, 255, 255))
            screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
            pygame.draw.rect(screen, color, input_rect, 2)

            pygame.display.flip()
    
    def runGame(self): 
        screen_width = self.screen_info.current_w
        screen_height = self.screen_info.current_h
        # Create the game window
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Roulette Screen")
        running = True
        start = True
        button_text = ["Straight Bet", "Split Bet", "Street Bet", "Corner Bet", "Five Number Bet", "Line Bet", "Red", "Black", "Odd", "Even", "High", "Low", "Dozens Bet", "Columns Bet", "Quit"]
        buttons = self.create_board(screen, screen_width, screen_height, button_text)
        quit_button = pygame.Rect(100, 100, 150, 50)
        cont_button = pygame.Rect(100, 100, 150, 50)
        while running:
            gamble = None
            bet_amount = None
            roll = False
            mis_req = False
            mouse_pos = pygame.mouse.get_pos() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for x in range(15):
                        if buttons[x].collidepoint(mouse_pos):
                            start = False
                            clear_bottom_rect = pygame.Rect(0, screen_height/2, screen_width, screen_height/2)
                            screen.fill((1, 138, 61), clear_bottom_rect)
                            if x == 14:
                                running = False
                            elif x < 5:
                                bet_number = self.text_input_box(screen, "Please choose which numbers to place your bet: ", screen_width/3, screen_height - 100, screen_width/4, screen_height/10)
                                self.numbers = bet_number.split()
                                gamble = x
                                req = self.req_num(self.numbers, x)
                                if req:
                                    roll = True
                                    clear_rect = pygame.Rect(screen_width/3, screen_height - 150, screen_width, screen_height/10)
                                    screen.fill((1, 138, 61), clear_rect)
                                    bet_amount = int(self.text_input_box(screen, "You have selected " + button_text[x] + "! Please place bet: ", screen_width/3, screen_height - 100, screen_width/4, screen_height/10))
                                    if bet_amount >= self.points:
                                        valid = self.bet_checker(screen, bet_amount, screen_width, screen_height)
                                        if valid == False:
                                            roll = False
                                            mis_req = True
                                        bet_amount = self.points
                                else:
                                    mis_req = True
                            else:
                                roll = True
                                gamble = x
                                self.numbers = self.number_type(screen, x)
                                bet_amount = int(self.text_input_box(screen, "You have selected " + button_text[x] + "! Please place bet: ", screen_width/3, screen_height - 100, screen_width/4, screen_height/10))
                                if bet_amount >= self.points:
                                    valid = self.bet_checker(screen, bet_amount, screen_width, screen_height)
                                    if valid == False:
                                        roll = False
                                        mis_req = True
                                    bet_amount = self.points
                    if quit_button.collidepoint(mouse_pos):            
                                running = False
                    if cont_button.collidepoint(mouse_pos):
                                buttons = self.create_board(screen, screen_width, screen_height, button_text)

            if roll:
                rolled = self.rolling(screen, screen_height, screen_width, self.numbers)
                if rolled:
                    self.point_score(bet_amount, gamble)
                    bottom_font = pygame.font.SysFont("Times New Roman", 70)
                    bottom_msg = bottom_font.render("You Win! Your Points: " + str(self.points), True, (255, 255, 255))
                    msg_rect = pygame.Rect(screen_width/3, screen_height - 200, 300, 200) 
                    bottom_place = bottom_msg.get_rect(center=msg_rect.center)
                    screen.blit(bottom_msg, bottom_place)
                    pygame.display.flip()
                else:
                    self.points = self.points - bet_amount
                    bottom_font = pygame.font.SysFont("Times New Roman", 70)
                    bottom_msg = bottom_font.render("You Lose! Your Points: " + str(self.points), True, (255, 255, 255))
                    msg_rect = pygame.Rect(screen_width/3, screen_height - 200, 300, 200)  
                    bottom_place = bottom_msg.get_rect(center=msg_rect.center)
                    screen.blit(bottom_msg, bottom_place)
                    pygame.display.flip()
                quit_button = self.create_button("Quit", 50, screen_height - 125, screen, 50, 150)   
                cont_button = self.create_button("Cont", screen_width - 200, screen_height - 125, screen, 50, 150)
            
            if mis_req:
                clear_bottom_rect = pygame.Rect(0, screen_height/2, screen_width, screen_height/2)
                screen.fill((1, 138, 61), clear_bottom_rect)
                pygame.display.flip()
                bottom_font = pygame.font.SysFont("Times New Roman", 30)
                bottom_msg = bottom_font.render("You put inccorect amount of/out of sequence numbers, try again!", True, (255, 255, 255))
                msg_rect = pygame.Rect(screen_width*3/8, screen_height - 200, 300, 200)  
                bottom_place = bottom_msg.get_rect(center=msg_rect.center)
                screen.blit(bottom_msg, bottom_place)
                pygame.display.flip()
                quit_button = self.create_button("Quit", 50, screen_height - 125, screen, 50, 150)   
                cont_button = self.create_button("Cont", screen_width - 200, screen_height - 125, screen, 50, 150)
            pygame.display.flip()


        
