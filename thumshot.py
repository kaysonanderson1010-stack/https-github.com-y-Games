import thumby
import random

thumby.display.setFPS(30)

# ---- SAVE SETUP ----
thumby.saveData.setName("ShooterGame")

# Load high score (0 if none saved)
high_score = thumby.saveData.getItem("high_score")
if high_score == None:
    high_score = 0

# Screen
W = 72
H = 40

# Player
PLAYER_W = 3
PLAYER_H = 3
player_x = W // 2
player_y = H - 6

# Game state
bullets = []
enemies = []
score = 0
game_over = False

# Sprites (WIDTH = bytes)
player_sprite = bytearray([
    0b010,
    0b111,
    0b010
])

enemy_sprite = bytearray([
    0b111,
    0b101,
    0b111
])

bullet_sprite = bytearray([0b1])

player = thumby.Sprite(PLAYER_W, PLAYER_H, player_sprite, player_x, player_y)

def reset_game():
    global bullets, enemies, score, game_over, player_x
    bullets = []
    enemies = []
    score = 0
    game_over = False
    player_x = W // 2

while True:
    thumby.display.fill(0)

    if not game_over:
        # ---- INPUT ----
        if thumby.buttonL.pressed() and player_x > 0:
            player_x -= 2
        if thumby.buttonR.pressed() and player_x < W - PLAYER_W:
            player_x += 2
        if thumby.buttonA.justPressed():
            bullets.append([player_x + 1, player_y])

        # ---- SPAWN ENEMY ----
        if random.randint(0, 18) == 0:
            enemies.append([random.randint(0, W - 3), 0])

        # ---- BULLETS ----
        for b in bullets[:]:
            b[1] -= 3
            if b[1] < 0:
                bullets.remove(b)

        # ---- ENEMIES ----
        for e in enemies[:]:
            e[1] += 1

            # ENEMY TOUCH PLAYER = DIE
            if (e[0] < player_x + PLAYER_W and
                e[0] + 3 > player_x and
                e[1] < player_y + PLAYER_H and
                e[1] + 3 > player_y):
                game_over = True

            if e[1] > H:
                enemies.remove(e)

        # ---- BULLET vs ENEMY ----
        for e in enemies[:]:
            for b in bullets[:]:
                if abs(e[0] - b[0]) < 2 and abs(e[1] - b[1]) < 2:
                    enemies.remove(e)
                    bullets.remove(b)
                    score += 1
                    break

        # ---- DRAW ----
        player.x = player_x
        thumby.display.drawSprite(player)

        for b in bullets:
            thumby.display.drawSprite(
                thumby.Sprite(1, 1, bullet_sprite, b[0], b[1])
            )

        for e in enemies:
            thumby.display.drawSprite(
                thumby.Sprite(3, 3, enemy_sprite, e[0], e[1])
            )

        thumby.display.drawText(str(score), 0, 0, 1)
        thumby.display.drawText("HI:" + str(high_score), 40, 0, 1)

    else:
        # ---- SAVE HIGH SCORE ----
        if score > high_score:
            high_score = score
            thumby.saveData.setItem("high_score", high_score)
            thumby.saveData.save()

        thumby.display.drawText("GAME OVER", 10, 8, 1)
        thumby.display.drawText("Score:" + str(score), 8, 18, 1)
        thumby.display.drawText("Best:" + str(high_score), 8, 26, 1)
        thumby.display.drawText("B=Restart", 5, 34, 1)

        if thumby.buttonB.justPressed():
            reset_game()

    thumby.display.update()
