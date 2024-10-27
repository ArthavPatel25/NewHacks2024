utton.png")  # Replace with your button image file
    button_image = pygame.transform.scale(button_image, (button_width, button_height))  # Resize button to height and width
    button_x = (screen_width - button_width) // 2  # Center horizontally
    button_y = screen_height - button_height - pos   # pos pixels from the bottom
    button_rect = button_image.get_rect()
    button_rect.topleft = (button_x, button_y)
    # Define font for button text
    font = pygame.font.SysFont("Times New Roman", 25)  # Times New Roman with font size 25
    button_text = font.render(text, True, (255, 255, 255))  # White text
    text_rect = button_text.get_rect(center=button_rect.center)
    