#!/usr/bin/env python3
"""
buddy-cli — ASCII animal companions for your terminal
https://github.com/jungkang0911/buddy-cli
MIT License

In memory of 嬌嬌 — a Schnauzer with a terrible sense of direction,
who wandered everywhere for 15 years and always found her way back.
"""
import sys, time, random, os, shutil

# ── ANSI ──────────────────────────────────────────────────
os.system("")
R  = "\033[0m"
BOLD = "\033[1m"
DIM  = "\033[2m"
FG = {
    "white":  "\033[37m",
    "dwhite": "\033[2;37m",
    "yellow": "\033[33m",
    "dyellow":"\033[2;33m",
    "green":  "\033[32m",
    "dgreen": "\033[2;32m",
    "cyan":   "\033[36m",
    "dcyan":  "\033[2;36m",
    "blue":   "\033[34m",
    "magenta":"\033[35m",
    "red":    "\033[31m",
    "brown":  "\033[2;33m",
}

def fg(name): return FG.get(name, "")
def goto(x, y): sys.stdout.write(f"\033[{y};{x}H")
def put(x, y, text, color=""):
    goto(x, y); sys.stdout.write(f"{color}{text}{R}")
def erase(x, y, w, h=1):
    for i in range(h):
        goto(x, y+i); sys.stdout.write(" " * w)

# ── SPRITES ───────────────────────────────────────────────
SCHNAUZER = {
    "walk_r":  ([r"|\  /| ", r"(o''o) ", r"\_ww_/>"],
                [r"|\  /| ", r"(o''o) ", r"\_ww_/~"]),
    "walk_l":  ([r" |\  /|", r" (o''o)", r"<\_ww_/"],
                [r" |\  /|", r" (o''o)", r"~\_ww_/"]),
    "sit":      [r" |\  /| ", r" (o''o) ", r" \_ww_/ "],
    "sleep":    [r" |\  /| ", r" (-..-)z", r" \_ww_/ "],
    "lookat_r": [r"|\  /|  ", r"(o''o)~ ", r"\_ww_/  "],
    "lookat_l": [r"  |\  /|", r" ~(o''o)", r"  \_ww_/"],
    "dig":     ([r" |\  /| ", r" (o'.') ", r" \_ww_/ "],
                [r" |\  /| ", r" (o'.') ", r" \_,w,/ "]),
    "chase_r":  [r"|\  /|  ", r"(o!!o)  ", r"\_ww_/=>"],
    "chase_l":  [r"  |\  /|", r"  (o!!o)", r"<=\_ww_/"],
    "w": 8, "h": 3,
    "color": "white", "dim_color": "dwhite",
}

BIRD = {
    "fly_r": ([r"\o/ ", r" |  "], [r"-o- ", r" |  "]),
    "fly_l": ([r" \o/", r"  | "], [r" -o-", r"  | "]),
    "w": 4, "h": 2,
    "color": "cyan",
}

BUTTERFLY = {
    "frames": ([r">8<", r" | "], [r"(8)", r" | "]),
    "w": 3, "h": 2,
    "color": "magenta",
}

# ── BACKGROUND ────────────────────────────────────────────
def build_bg(cols, rows):
    bg = []
    # stars
    for _ in range(cols // 4):
        sx, sy = random.randint(1, cols-1), random.randint(1, 3)
        bg.append((sx, sy, random.choice([".", "*", "·"]),
                   random.choice([fg("dwhite"), fg("dcyan"), fg("dyellow")])))
    # moon
    mx = random.randint(cols-20, cols-5)
    for ch, dx, dy in [("(",0,0),(" ",1,0),(")",2,0),("(",0,1),("_",1,1),(")",2,1)]:
        bg.append((mx+dx, 1+dy, ch, fg("dyellow")))
    # clouds
    for _ in range(max(1, cols//25)):
        cx, cy = random.randint(5, cols-12), random.randint(4, rows//3)
        for i, c in enumerate("(~~~)"):
            bg.append((cx+i, cy, c, fg("dwhite")))
    # ground
    for gx in range(1, cols):
        bg.append((gx, rows-1, random.choice(["_","_","."]), fg("dgreen")))
    # grass
    for _ in range(cols//5):
        gx, gy = random.randint(1, cols-4), rows-2
        for i, c in enumerate(random.choice([",;,", "v,v", "vvv"])):
            bg.append((gx+i, gy, c, fg("green")))
    # trees
    for _ in range(max(1, cols//18)):
        tx, ty = random.randint(3, cols-6), rows-6
        for item in [(tx+2,ty,"^",fg("green")),
                     (tx+1,ty+1,"/^\\",fg("green")),
                     (tx,ty+2,"/ \\",fg("dgreen")),
                     (tx+2,ty+3,"|",fg("brown")),
                     (tx+2,ty+4,"|",fg("brown"))]:
            bg.append(item)
    return bg

def draw_bg(bg):
    for item in bg:
        x, y, ch, col = item
        put(x, y, ch, col)
    sys.stdout.flush()

# ── BUBBLE ────────────────────────────────────────────────
def draw_bubble(x, y, text, cols):
    w = len(text)+2
    bx = min(x, cols-w-3); by = max(1, y-2)
    put(bx, by,   f"┌{'─'*w}┐", fg("cyan"))
    put(bx, by+1, f"│ {text} │", fg("cyan"))
    put(bx, by+2, f"└{'─'*w}┘", fg("cyan"))
    sys.stdout.flush()

def erase_bubble(x, y, text, cols):
    w = len(text)+4; bx = min(x, cols-w-3); by = max(1, y-2)
    erase(bx, by, w+2, 3)

# ── ENTITY ────────────────────────────────────────────────
class Entity:
    def __init__(self, x, y, dx, dy, w, h):
        self.x, self.y, self.dx, self.dy = x, y, dx, dy
        self.w, self.h = w, h
        self.frame = 0
        self.state = "idle"
        self.timer = 0
        self.active = True

    def erase(self): erase(self.x, self.y, self.w+2, self.h)

    def dist(self, other):
        return abs(self.x - other.x), abs(self.y - other.y)

# ── DOG ───────────────────────────────────────────────────
class Dog(Entity):
    BUBBLES = ["Woof!", "...", "zzz", "♪", "(*´▽`*)", "Woof?", "*yawn*", "!"]
    LOST_BUBBLES = ["Huh?", "Where am I?", "owo?", "...wait"]  # directionally challenged

    def __init__(self, x, y):
        super().__init__(x, y, random.choice([-1,1]), 0,
                         SCHNAUZER["w"], SCHNAUZER["h"])
        self.state   = "walk"
        self.bubble  = ""
        self.b_timer = 0
        self.idle    = 0
        self.speed   = 1

    def get_sprite(self):
        s = SCHNAUZER
        if self.state == "walk":
            frames = s["walk_r"] if self.dx >= 0 else s["walk_l"]
            return frames[self.frame % 2]
        if self.state == "chase":
            return s["chase_r"] if self.dx >= 0 else s["chase_l"]
        if self.state == "dig":
            return s["dig"][self.frame % 2]
        if self.state == "lookat":
            return s["lookat_r"] if self.dx >= 0 else s["lookat_l"]
        if self.state == "sit":   return s["sit"]
        if self.state == "sleep": return s["sleep"]
        return s["sit"]

    def update(self, cols, rows, butterfly, bird):
        ground = rows - 3
        bdx, bdy = self.dist(butterfly)
        bird_near = bird.active and self.dist(bird)[1] < 5 and self.dist(bird)[0] < 20

        # --- state transitions ---
        if self.state == "walk":
            self.idle = 0
            # chase butterfly if nearby
            if butterfly.active and bdx < 18 and bdy < 6:
                self.state = "chase"
                self.dx = 1 if butterfly.x > self.x else -1
                self.speed = 2
            elif bird_near:
                self.state = "lookat"
                self.dx = 1 if bird.x > self.x else -1
                self.timer = 12
            elif random.random() < 0.007:
                self.state = "sit"; self.idle = 0
            # 路痴：randomly second-guesses direction mid-walk
            elif random.random() < 0.05 and self.b_timer == 0:
                self.dx = -self.dx
                self.bubble  = random.choice(self.LOST_BUBBLES)
                self.b_timer = 10
                draw_bubble(self.x, self.y, self.bubble, cols)
        elif self.state == "chase":
            if not butterfly.active or (bdx < 3 and bdy < 3):
                self.state = "walk"; self.speed = 1
                if bdx < 3:
                    butterfly.respawn(cols, rows)
                    self.bubble = "Got it!!"; self.b_timer = 14
                    draw_bubble(self.x, self.y, self.bubble, cols)
            else:
                self.dx = 1 if butterfly.x > self.x else -1
        elif self.state == "lookat":
            self.timer -= 1
            if self.timer <= 0: self.state = "walk"
        elif self.state == "sit":
            self.idle += 1
            if self.idle > 12:
                self.state = random.choice(["sleep", "dig", "walk"])
                self.idle = 0
        elif self.state == "dig":
            self.idle += 1
            if self.idle > 14: self.state = "walk"; self.idle = 0
        elif self.state == "sleep":
            self.idle += 1
            if self.idle > 28: self.state = "walk"; self.idle = 0

        # --- movement ---
        if self.state in ("walk", "chase"):
            nx = self.x + self.dx * self.speed
            if nx < 1 or nx + self.w >= cols:
                self.dx = -self.dx; nx = self.x + self.dx * self.speed
            self.x = nx
            self.y = ground

        # --- bubble ---
        if self.b_timer > 0:
            self.b_timer -= 1
            if self.b_timer == 0:
                erase_bubble(self.x, self.y, self.bubble, cols)
                self.bubble = ""
        elif random.random() < 0.004 and self.state not in ("chase","lookat"):
            self.bubble  = random.choice(self.BUBBLES)
            self.b_timer = 16
            draw_bubble(self.x, self.y, self.bubble, cols)

    def draw(self):
        sprite = self.get_sprite()
        col = fg("white") if self.state != "sleep" else fg("dwhite")
        for i, line in enumerate(sprite):
            put(self.x, self.y+i, line, col)
        self.frame += 1
        sys.stdout.flush()

# ── BIRD ──────────────────────────────────────────────────
class Bird(Entity):
    def __init__(self, cols, rows):
        super().__init__(0, 0, 1, 0, BIRD["w"], BIRD["h"])
        self.active = False
        self._cols = cols; self._rows = rows
        self.spawn_timer = random.randint(60, 120)

    def respawn(self, cols, rows):
        self.dx = random.choice([-1, 1])
        self.x  = 1 if self.dx > 0 else cols - self.w - 1
        self.y  = random.randint(4, rows // 3)
        self.active = True

    def update(self, cols, rows):
        if not self.active:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                self.respawn(cols, rows)
                self.spawn_timer = random.randint(80, 160)
            return
        self.erase()
        self.x += self.dx * 2
        if self.x < 0 or self.x > cols:
            self.active = False

    def draw(self):
        if not self.active: return
        frames = BIRD["fly_r"] if self.dx > 0 else BIRD["fly_l"]
        sprite = frames[self.frame % 2]
        for i, line in enumerate(sprite):
            put(self.x, self.y+i, line, fg("cyan"))
        self.frame += 1
        sys.stdout.flush()

# ── BUTTERFLY ─────────────────────────────────────────────
class Butterfly(Entity):
    def __init__(self, cols, rows):
        super().__init__(cols//3, rows//2, random.choice([-1,1]),
                         random.choice([-1,0,1]), BUTTERFLY["w"], BUTTERFLY["h"])
        self.active = True

    def respawn(self, cols, rows):
        self.x = random.randint(10, cols-10)
        self.y = random.randint(5, rows-8)
        self.dx = random.choice([-1,1])
        self.dy = random.choice([-1,0,1])
        self.active = True

    def update(self, cols, rows):
        if not self.active: return
        self.erase()
        self.x += self.dx; self.y += self.dy
        # bounce
        if self.x < 2 or self.x + self.w >= cols - 1: self.dx = -self.dx
        if self.y < 4 or self.y + self.h >= rows - 4:  self.dy = -self.dy
        # random wander
        if random.random() < 0.06: self.dx = -self.dx
        if random.random() < 0.04: self.dy = random.choice([-1,0,1])

    def draw(self):
        if not self.active: return
        sprite = BUTTERFLY["frames"][self.frame % 2]
        for i, line in enumerate(sprite):
            put(self.x, self.y+i, line, fg("magenta"))
        self.frame += 1
        sys.stdout.flush()

# ── MAIN ──────────────────────────────────────────────────
def draw_hint(cols, rows):
    msg = "buddy-cli  |  Ctrl+C to quit"
    put(cols - len(msg) - 1, rows, msg, DIM)
    sys.stdout.flush()

def run():
    sys.stdout.write("\033[?25l")
    try:
        cols, rows = shutil.get_terminal_size((80, 24))
        os.system("cls")
        bg = build_bg(cols, rows)
        draw_bg(bg)
        draw_hint(cols, rows)

        dog = Dog(cols//2, rows-3)
        bird = Bird(cols, rows)
        butterfly = Butterfly(cols, rows)
        last_size = (cols, rows)

        while True:
            cols, rows = shutil.get_terminal_size((80, 24))
            if (cols, rows) != last_size:
                os.system("cls")
                bg = build_bg(cols, rows)
                draw_bg(bg); draw_hint(cols, rows)
                last_size = (cols, rows)

            dog.erase()
            bird.update(cols, rows)
            butterfly.update(cols, rows)
            dog.update(cols, rows, butterfly, bird)

            bird.draw()
            butterfly.draw()
            dog.draw()

            sleep = 0.08 if dog.state == "chase" else 0.13
            time.sleep(sleep)

    except KeyboardInterrupt:
        dog.erase(); bird.erase(); butterfly.erase()
        sys.stdout.write("\033[?25h")
        goto(1, rows)
        print("Goodbye~ Woof!")

if __name__ == "__main__":
    run()
