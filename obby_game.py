import thumby
import time

thumby.saveData.setName("SafeObby2")

# --- Load save ---
wins = thumby.saveData.getItem("wins") or 0
canFly = thumby.saveData.getItem("fly") or False
hasGun = thumby.saveData.getItem("gun") or False

# --- Player ---
px, py = 5, 30
vx, vy = 0, 0
onGround = False
facingRight = True

GRAVITY = 1
JUMP = -6

# --- Bullet ---
bulletX, bulletY = -1, -1
bulletActive = False

# --- Goal ---
goalX, goalY = 65, 12
goalTouched = False

# --- Shop ---
shopOpen = False

# --- A press counter for fly removal ---
aPressCount = 0
lastAPressTime = 0

platforms = [
    (0, 36, 72),
    (20, 28, 15),
    (45, 20, 15),
]

def save():
    thumby.saveData.setItem("wins", wins)
    thumby.saveData.setItem("fly", canFly)
    thumby.saveData.setItem("gun", hasGun)
    thumby.saveData.save()

while True:
    thumby.display.fill(0)

    # --- SHOP SCREEN ---
    if shopOpen:
        thumby.display.drawText("SHOP", 22, 2, 1)
        thumby.display.drawText("A BUY GUN", 0, 14, 1)
        thumby.display.drawText("3 WINS", 0, 22, 1)
        thumby.display.drawText("B EXIT", 0, 30, 1)
        thumby.display.update()

        if thumby.buttonA.justPressed() and not hasGun and wins >= 3:
            wins -= 3
            hasGun = True
            save()

        if thumby.buttonB.justPressed():
            shopOpen = False
            time.sleep(0.15)

        time.sleep(0.05)
        continue

    # --- GAME SCREEN ---
    thumby.display.drawText("WIN " + str(wins), 0, 2, 1)
    if canFly:
        thumby.display.drawText("FLY", 50, 2, 1)

    for p in platforms:
        thumby.display.drawFilledRectangle(p[0], p[1], p[2], 3, 1)

    thumby.display.drawRectangle(goalX, goalY, 5, 5, 1)
    thumby.display.drawFilledRectangle(px, py, 3, 3, 1)

    if hasGun:
        thumby.display.drawFilledRectangle(px + (3 if facingRight else -2), py + 1, 2, 1, 1)

    if bulletActive:
        thumby.display.drawFilledRectangle(bulletX, bulletY, 2, 1, 1)

    thumby.display.update()

    vx = 0

    # Movement
    if thumby.buttonL.pressed():
        vx = -2
        facingRight = False
    if thumby.buttonR.pressed():
        vx = 2
        facingRight = True

    # Jump / Fly
    if canFly:
        vy = -2 if thumby.buttonU.pressed() else (2 if thumby.buttonD.pressed() else 0)
    else:
        if thumby.buttonA.justPressed() and onGround:
            vy = JUMP
        vy += GRAVITY

    # --- A press 3× to remove fly ---
    if thumby.buttonA.justPressed():
        t = time.ticks_ms()
        if t - lastAPressTime > 1000:  # reset counter if >1s
            aPressCount = 1
        else:
            aPressCount += 1
        lastAPressTime = t
        if aPressCount >= 3:
            canFly = False
            aPressCount = 0
            save()

    # Shoot
    if hasGun and thumby.buttonU.justPressed() and not bulletActive:
        bulletActive = True
        bulletX = px + 3 if facingRight else px - 2
        bulletY = py + 1

    # Shop
    if thumby.buttonB.justPressed():
        shopOpen = True
        time.sleep(0.15)

    # Update positions
    px += vx
    py += vy
    px = max(0, min(72-3, px))
    py = max(0, min(40-3, py))

    # Bullet movement
    if bulletActive:
        bulletX += 4 if facingRight else -4
        if bulletX < 0 or bulletX > 72:
            bulletActive = False

    # Platform collision
    onGround = False
    for p in platforms:
        if px+3 > p[0] and px < p[0]+p[2]:
            if py+3 >= p[1] and py+3 <= p[1]+3 and vy >= 0:
                py = p[1]-3
                vy = 0
                onGround = True

    # Death
    if py > 40:
        px, py = 5, 30
        vy = 0
        bulletActive = False
        goalTouched = False

    # Goal
    touching = px+3 > goalX and px < goalX+5 and py+3 > goalY and py < goalY+5
    if touching and not goalTouched:
        wins += 1
        canFly = True
        save()
        goalTouched = True
    if not touching:
        goalTouched = False

    time.sleep(0.04)
