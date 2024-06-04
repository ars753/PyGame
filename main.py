import pygame
import time
import random
pygame.font.init()#add fonts from pygame

# Load images


WIDTH, HEIGHT=800,600
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Maimyl Game")

BG=pygame.transform.scale(pygame.image.load("images/jungle.jpg"),(WIDTH,HEIGHT))

PLAYER_WIDTH=80
PLAYER_HEIGHT=120

PLAYER_VEL=5
STAR_WIDTH=40
STAR_HEIGHT=50
STAR_VEL=3
star_img =pygame.transform.scale(pygame.image.load('images/monkey.PNG'),(STAR_WIDTH,STAR_HEIGHT) )
character_img = pygame.transform.scale(pygame.image.load('images/batyr.png'),(PLAYER_WIDTH,PLAYER_HEIGHT))


FONT=pygame.font.SysFont("comicsans", 30)#choosing font
def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    for star in stars:

        star_img_scaled = pygame.transform.scale(star_img, (star.width, star.height))
        WIN.blit(star_img_scaled, (star.x, star.y))


    character_img_scaled = pygame.transform.scale(character_img, (player.width, player.height))
    WIN.blit(character_img_scaled, (player.x, player.y))

    pygame.display.update()


player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
stars = []  # Assuming stars is a list used in your game
start_time = 0  # Define start_time globally

def restart_game():
    global player, stars, start_time  #объявляем переменные как глобальные, чтобы их можно было изменять

    #сброс позиции игрока
    player.x = 200
    player.y = HEIGHT - PLAYER_HEIGHT

    #сброс других переменных игры
    stars = []  #очищаем список маймылов
    start_time = time.time()  # Сбрасываем время игры до начального состояния
    return start_time

def main(): #starts game
    run=True

    player=pygame.Rect(200,HEIGHT-PLAYER_HEIGHT,PLAYER_WIDTH,PLAYER_HEIGHT)#creating character

    clock=pygame.time.Clock()

    start_time=time.time()
    elapsed_time=0

    star_add_increment=2000
    star_count=0
    stars=[]
    hit=False


    while run:
        star_count+=clock.tick(60)
        elapsed_time=time.time()-start_time

        if star_count> star_add_increment:
            for _ in range(3):
                star_x=random.randint(0, WIDTH-STAR_WIDTH)
                star=pygame.Rect(star_x,-STAR_HEIGHT,STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment=max(200,star_add_increment-50)
            star_count=0


        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break

        keys=pygame.key.get_pressed()#moving
        if keys[pygame.K_LEFT] and player.x-PLAYER_VEL>=0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x+PLAYER_VEL+player.width<=WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y+=STAR_VEL
            if star.y>HEIGHT:
                stars.remove(star)
            elif star.y+star.height>=player.y and star.colliderect(player):
                stars.remove(star)
                hit=True
                break
        if hit:
            lost_text = FONT.render("YOU ARE MAIMYL! " "Press R to restart", 1, "black")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()

            # Wait for R key to be pressed to restart
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        waiting = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            start_time = restart_game()  # Restart the game
                            waiting = False
                            hit = False  # Reset hit flag
                            break

            #очистка экрана после перезапуска игры
            WIN.fill((0, 0, 0))
            pygame.display.update()

        draw(player, elapsed_time,stars)
    pygame.quit()
if __name__=="__main__":
    main()