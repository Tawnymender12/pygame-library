import pygame

def moveLR(posX, speed, boundaries=False, boundaryXstart=0, boundaryXend=0):
    if pygame.key.get_pressed()[pygame.K_RIGHT]: posX += speed
    if pygame.key.get_pressed()[pygame.K_LEFT]: posX -= speed

    if boundaries:
        if posX <= boundaryXstart:
            posX = boundaryXstart
        if posX >= boundaryXend:
            posX = boundaryXend

    return posX

def moveUD(posY, speed, boundaries=False, boundaryYstart=0, boundaryYend=0):
    if pygame.key.get_pressed()[pygame.K_DOWN]: posY += speed
    if pygame.key.get_pressed()[pygame.K_UP]: posY -= speed

    if boundaries:
        if posY <= boundaryYstart:
            posY = boundaryYstart
        if posY >= boundaryYend:
            posY = boundaryYend

    return posY

def moveUDLR(posX, posY, speed):
    if pygame.key.get_pressed()[pygame.K_RIGHT]: posX += speed
    if pygame.key.get_pressed()[pygame.K_LEFT]: posX -= speed
    if pygame.key.get_pressed()[pygame.K_DOWN]: posY += speed
    if pygame.key.get_pressed()[pygame.K_UP]: posY -= speed

    return posX, posY

def boundaries(posX, posY, boundaryXstart, boundaryYstart, boundaryXend, boundaryYend):
    if boundaries:
        if posX <= boundaryXstart:
            posX = boundaryXstart
        if posX >= boundaryXend:
            posX = boundaryXend
        if posY <= boundaryYstart:
            posY = boundaryYstart
        if posY >= boundaryYend:
            posY = boundaryYend
          
    return posX, posY

def loadMap(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(row)
    return game_map

def drawMap(map, screen, tile1, tile2, tileSize):
    rect_list = []
    y = 0
    for row in map:
        x = 0
        for block in row:
            if block == '1':
                screen.blit(tile1, (x * tileSize, y * tileSize))
            if block == '2':
                screen.blit(tile2, (x * tileSize, y * tileSize))
            if block != '0':
                rect_list.append(pygame.Rect(x * tileSize, y * tileSize, tileSize, tileSize))
            x += 1
        y += 1
    return rect_list

gravity = 0
def falling(posY, gravityPower, maxAcceleration):
    global gravity
    gravity += gravityPower
    posY += gravity
    if gravity >= maxAcceleration: gravity = maxAcceleration
    return posY

def moveUDLRcol(player_rect, speed, rect_list):
    right = False
    left = False
    if pygame.key.get_pressed()[pygame.K_RIGHT]: player_rect.x += speed; right = True
    if pygame.key.get_pressed()[pygame.K_LEFT]: player_rect.x -= speed; left = True
    for rect in rect_list:
        if player_rect.colliderect(rect):
            if left:
                player_rect.left = rect.right
            elif right:
                player_rect.right = rect.left

    up = False
    down = False
    if pygame.key.get_pressed()[pygame.K_DOWN]: player_rect.y += speed; down = True
    if pygame.key.get_pressed()[pygame.K_UP]: player_rect.y -= speed; up = True
    for rect in rect_list:
        if player_rect.colliderect(rect):
            if up:
                player_rect.top = rect.bottom
            elif down:
                player_rect.bottom = rect.top

    return player_rect

def moveLRcol(player_rect, speed, jump_height, gravity_power, max_accelaration, rect_list, jump_SFX_path = None, volume=1):
    jump_SFX_path.set_volume(volume) if jump_SFX_path != None else None
    
    right = False
    left = False
    if pygame.key.get_pressed()[pygame.K_RIGHT]: player_rect.x += speed; right = True
    if pygame.key.get_pressed()[pygame.K_LEFT]: player_rect.x -= speed; left = True
    for rect in rect_list:
        if player_rect.colliderect(rect):
            if left:
                player_rect.left = rect.right
            elif right:
                player_rect.right = rect.left

    can_jump = False
    up = False
    down = False
    global gravity
    gravity += gravity_power
    if gravity >= max_accelaration: gravity = max_accelaration
    player_rect.y += gravity
    if gravity > 0: down = True
    if gravity < 0: up = True
    for rect in rect_list:
        if player_rect.colliderect(rect):
            if up:
                player_rect.top = rect.bottom
                gravity = 0
            elif down:
                player_rect.bottom = rect.top
                gravity = 0
                can_jump = True
                if pygame.key.get_pressed()[pygame.K_SPACE] and can_jump: 
                    gravity -= jump_height
                    can_jump = False
                    jump_SFX_path.play() if jump_SFX_path != None else None
                if pygame.key.get_pressed()[pygame.K_UP] and can_jump: 
                    gravity -= jump_height
                    can_jump = False
                    jump_SFX_path.play() if jump_SFX_path != None else None

    return player_rect

def write(font_path: str, font_size, text: str, antialias: bool, color: str, surface, pos=(0, 0)):
    font = pygame.font.Font(font_path, font_size)
    rendered_text = font.render(text, antialias, color)
    rendered_text_rect = rendered_text.get_rect(center = (pos))
    surface.blit(rendered_text, rendered_text_rect)

def button(button_img, posX, posY, surface, button_bool, button_clicked_img=None, click_sound=None):
    button_img_rect = button_img.get_rect(center = (posX, posY))
    surface.blit(button_img, button_img_rect)

    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos.colliderect(button_img_rect):
        if pygame.mouse.get_pressed()[0]:
            if button_clicked_img is not None: surface.blit(button_clicked_img, button_img_rect)
            if click_sound is not None: click_sound.play()
            button_bool = True
    
    return button_bool
