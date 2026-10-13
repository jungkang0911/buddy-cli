#!/usr/bin/env python3
"""
buddy-cli — ASCII animal companions for your terminal
https://github.com/jungkang0911/buddy-cli
MIT License

In memory of 嬌嬌 — a Schnauzer with a terrible sense of direction,
who wandered everywhere for 15 years and always found her way back.

Controls:  p pet · f feed · b ball · t trick · c call · s sit · space hi
           h help · q quit · click on her to pet · click elsewhere to call her there
"""
import sys, time, random, os, shutil, re, unicodedata

IS_WIN = os.name == "nt"
if IS_WIN:
    import msvcrt
else:
    import termios, tty, select

# ── ANSI ──────────────────────────────────────────────────
os.system("")
R  = "\033[0m"
BOLD = "\033[1m"
DIM  = "\033[2m"
FG = {
    "white":  "\033[37m",
    "bwhite": "\033[1;37m",
    "dwhite": "\033[2;37m",
    "yellow": "\033[33m",
    "byellow":"\033[93m",
    "dyellow":"\033[2;33m",
    "green":  "\033[32m",
    "dgreen": "\033[2;32m",
    "cyan":   "\033[36m",
    "dcyan":  "\033[2;36m",
    "blue":   "\033[34m",
    "magenta":"\033[35m",
    "pink":   "\033[95m",
    "red":    "\033[91m",
    "brown":  "\033[2;33m",
}

def fg(name): return FG.get(name, "")

COLS, ROWS = 80, 24
BG = {}       # (x, y) -> (char, color) — so erasing restores the scenery
_buf = []

def goto(x, y): _buf.append(f"\033[{y};{x}H")
def flush():
    sys.stdout.write("".join(_buf)); _buf.clear(); sys.stdout.flush()

def put(x, y, text, color=""):
    if y < 1 or y > ROWS: return
    if x < 1: text = text[1-x:]; x = 1
    text = text[:max(0, COLS - x)]
    if text:
        goto(x, y); _buf.append(f"{color}{text}{R}")

def put_sprite(x, y, lines, color=""):
    """Draw lines, treating spaces as transparent."""
    for i, line in enumerate(lines):
        for m in re.finditer(r"\S+", line):
            put(x + m.start(), y + i, m.group(), color)

def erase(x, y, w, h=1):
    for j in range(h):
        yy = y + j
        if yy < 1 or yy > ROWS: continue
        for i in range(w):
            xx = x + i
            if 1 <= xx < COLS:
                ch, col = BG.get((xx, yy), (" ", ""))
                goto(xx, yy); _buf.append(f"{col}{ch}{R}")

def dw(s):
    """Display width (CJK / fullwidth chars take two cells)."""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)

def clamp(v, lo, hi): return max(lo, min(hi, v))

def is_night():
    h = time.localtime().tm_hour
    return h >= 23 or h < 6

# ── SPRITES ───────────────────────────────────────────────
DOG_W, DOG_H = 8, 3
EARS, BODY = r"|\  /|", r"\_ww_/"

def side(facing, eyes="oo", nose="''", tail="~"):
    face = f"({eyes[0]}{nose}{eyes[1]})"
    if facing >= 0:
        return [(EARS + " ").ljust(DOG_W), (face + " ").ljust(DOG_W), (BODY + tail).ljust(DOG_W)]
    return [(" " + EARS).rjust(DOG_W), (" " + face).rjust(DOG_W), (tail + BODY).rjust(DOG_W)]

def front(eyes="oo", nose="''", wag=0):
    body = " " + BODY + " "
    if wag > 0: body = " " + BODY + "~"
    if wag < 0: body = "~" + BODY + " "
    return [" " + EARS + " ", f" ({eyes[0]}{nose}{eyes[1]}) ", body]

POSES = {
    "belly":  [r" /'ww'\ ", r" (^''^) ", r" |/  \| "],     # rolled over, paws up
    "belly2": [r" \'ww'/ ", r" (^''^) ", r" |/  \| "],
    "beg":    [r" |\  /| ", r" (^''^)/", r" /_ww_\ "],     # sitting up, waving
    "beg2":   [r" |\  /| ", r" (^''^)-", r" /_ww_\ "],
    "dig":   ([r" |\  /| ", r" (o'.') ", r" \_ww_/ "],
              [r" |\  /| ", r" (o'.') ", r" \_,w,/ "]),
    "sleep_r": ["        ", r" _|\  /|", r"(_(-..-)"],     # curled up
    "sleep_l": ["        ", r"|\  /|_ ", r"(-..-)_)"],
}

BIRD = {
    "fly_r": ([r"\o/ ", r" |  "], [r"-o- ", r" |  "]),
    "fly_l": ([r" \o/", r"  | "], [r" -o-", r"  | "]),
    "w": 4, "h": 2,
}
BUTTERFLY = {"frames": ([r">8<", r" | "], [r"(8)", r" | "]), "w": 3, "h": 2}
BONE = ["o==o", "o=o", "o=", "."]

# ── BACKGROUND ────────────────────────────────────────────
def build_bg(cols, rows):
    BG.clear()
    def add(x, y, ch, col): BG[(x, y)] = (ch, col)
    for _ in range(cols // 4):                                      # stars
        add(random.randint(1, cols-1), random.randint(2, 3),
            random.choice([".", "*", "·"]),
            random.choice([fg("dwhite"), fg("dcyan"), fg("dyellow")]))
    mx = random.randint(max(1, cols-20), max(1, cols-5))            # moon
    for ch, dx, dy in [("(",0,0),(" ",1,0),(")",2,0),("(",0,1),("_",1,1),(")",2,1)]:
        add(mx+dx, 2+dy, ch, fg("dyellow"))
    for _ in range(max(1, cols//25)):                               # clouds
        cx, cy = random.randint(5, max(5, cols-12)), random.randint(4, max(4, rows//3))
        for i, c in enumerate("(~~~)"):
            add(cx+i, cy, c, fg("dwhite"))
    for gx in range(1, cols):                                       # ground
        add(gx, rows-1, random.choice(["_","_","."]), fg("dgreen"))
    for _ in range(cols//5):                                        # grass
        gx = random.randint(1, max(1, cols-4))
        for i, c in enumerate(random.choice([",;,", "v,v", "vvv"])):
            add(gx+i, rows-2, c, fg("green"))
    for _ in range(max(1, cols//18)):                               # trees
        tx, ty = random.randint(3, max(3, cols-6)), rows-6
        for x, y, s, col in [(tx+2,ty,"^","green"), (tx+1,ty+1,"/^\\","green"),
                             (tx,ty+2,"/ \\","dgreen"), (tx+2,ty+3,"|","brown"),
                             (tx+2,ty+4,"|","brown")]:
            for i, c in enumerate(s):
                add(x+i, y, c, fg(col))

def draw_bg():
    for (x, y), (ch, col) in BG.items():
        put(x, y, ch, col)

# ── PARTICLES ─────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, ch, color, life, dx=0, dy=-1, every=2, wobble=False):
        self.x, self.y, self.ch, self.color = x, y, ch, color
        self.life, self.dx, self.dy, self.every, self.wobble = life, dx, dy, every, wobble
        self.age = 0

    def update(self):
        self.age += 1; self.life -= 1
        if self.age % self.every == 0:
            self.x += self.dx + (random.choice([-1, 0, 1]) if self.wobble else 0)
            self.y += self.dy
        return self.life > 0 and self.y > 1

    def erase(self): erase(self.x, self.y, 2)
    def draw(self):  put(self.x, self.y, self.ch, self.color)

# ── TOYS ──────────────────────────────────────────────────
class Ball:
    def __init__(self):
        self.active = False; self.x = self.y = self.vx = self.vy = 0.0

    def throw(self, x, y, direction):
        self.x, self.y = float(x), float(y)
        self.vx = direction * random.uniform(2.0, 3.4)
        self.vy = -random.uniform(1.6, 2.6)
        self.active = True

    def grounded(self): return self.y >= ROWS - 1.5

    def update(self):
        if not self.active: return
        ground = ROWS - 1
        self.vy += 0.4; self.x += self.vx; self.y += self.vy
        if self.y >= ground:
            self.y = ground
            if self.vy > 1.2: self.vy = -self.vy * 0.5
            else: self.vy = 0
            self.vx *= 0.8
            if abs(self.vx) < 0.25: self.vx = 0
        if self.y < 3: self.y = 3; self.vy = abs(self.vy)
        if self.x < 2: self.x = 2; self.vx = -self.vx * 0.7
        if self.x > COLS - 3: self.x = COLS - 3; self.vx = -self.vx * 0.7

    def erase(self):
        if self.active: erase(int(self.x), int(self.y), 1)
    def draw(self):
        if self.active: put(int(self.x), int(self.y), "o", fg("red"))

class Bone:
    def __init__(self):
        self.active = False; self.x = self.y = 0; self.bites = 0

    def drop(self, x):
        self.x, self.y, self.bites, self.active = x, 2, 0, True

    @property
    def landed(self): return self.y >= ROWS - 1

    def update(self):
        if self.active and not self.landed: self.y += 1

    def erase(self):
        if self.active: erase(self.x, self.y, 4)
    def draw(self):
        if self.active: put(self.x, self.y, BONE[min(self.bites, 3)], fg("bwhite"))

# ── DOG ───────────────────────────────────────────────────
IDLE = {"walk", "sit", "sleep", "dig", "lookat", "front", "chase", "happy", "belly"}
RUN  = {"chase", "fetch", "food", "come"}

CHATTER = ["Woof!", "...", "♪", "(*´▽`*)", "Woof?", "*sniff sniff*", "!", "hehe~", "♪ ♪"]
LOST    = ["Huh?", "Where am I?", "owo?", "...wait", "this way? no..."]
LOVE    = ["♥", "hehe~", "more pats!", "(´▽`)", "I love you!", "*wag wag*", "♥ ♥ ♥"]
HELLO   = ["Woof!", "Hi hi!", "Hello~!", "*boop*", "Play with me!", "!!"]
HUNGRY  = ["hungry...", "*stomach growls*", "treat? (f)", "feed me?"]
LONELY  = ["play with me?", "pet me? (p)", "*looks at you*", "bored..."]
SLEEPY  = ["sleepy...", "it's late~", "you should sleep too", "*yawn*"]
FINDS   = ["found a bone!", "a sock?!", "...nothing", "a shiny pebble!", "a worm!"]

STATUS = {
    "walk": "is wandering around", "come": "is coming~", "lost": "is lost again...",
    "chase": "is chasing a butterfly!", "sleep": "is napping  zZ", "dig": "is digging a hole",
    "fetch": "is fetching the ball!", "return": "is bringing the ball back",
    "food": "smells a treat!", "eat": "is munching", "happy": "is so happy",
    "belly": "wants belly rubs", "trick": "is showing off", "sit": "is sitting",
    "front": "is looking at you", "lookat": "is watching a bird",
}

class Dog:
    def __init__(self, x, ground):
        self.x, self.ground = x, ground
        self.dx = random.choice([-1, 1])
        self.state, self.timer, self.frame, self.speed = "walk", 0, 0, 1
        self.mood, self.food = 70, 70
        self.bubble, self.b_timer, self.lift = "", 0, 0
        self.blink = self.hop = self.lost = 0
        self.carry = False
        self.tx = self.home_x = x
        self.seq, self.pose, self.pet_ticks = [], "front", []
        self.stats = {"pets": 0, "treats": 0, "fetches": 0, "tricks": 0}
        self._drawn = self._bdrawn = None

    @property
    def y(self): return self.ground - (1 if self.hop > 0 else 0)

    def set_state(self, s, timer=0):
        self.state, self.timer = s, timer
        self.speed = 2 if s in RUN else 1

    def say(self, text, t=16):
        self.bubble, self.b_timer = text, t

    def contains(self, x, y):
        return self.x - 1 <= x <= self.x + DOG_W and self.y - 1 <= y <= self.y + DOG_H

    # ── commands ──
    def pet(self, w):
        self.stats["pets"] += 1
        self.mood = min(100, self.mood + 8)
        w.burst(self.x + 3, self.y - 1, "♥", fg("pink"), 3)
        self.pet_ticks = [t for t in self.pet_ticks if w.tick - t < 30] + [w.tick]
        if self.state not in IDLE:
            return                                    # busy — hearts only
        if self.state == "sleep":
            self.set_state("happy", 24); self.say("*yawn* ...hi!", 18)
        elif self.state == "belly":
            self.timer = max(self.timer, 24); self.say(random.choice(["hehe~", "more!", "♥"]), 10)
        elif len(self.pet_ticks) >= 3:
            self.set_state("belly", 36); self.pet_ticks = []
            self.say(random.choice(["belly rubs!!", "more more!", "hehehe~"]), 20)
        else:
            self.set_state("happy", 24); self.say(random.choice(LOVE), 14)

    def feed(self, w):
        if w.bone.active:
            self.say("one at a time~", 12); return
        w.bone.drop(clamp(self.x + random.randint(-18, 18), 3, w.cols - 6))

    def throw(self, w):
        if w.ball.active or self.carry:
            self.say("the ball's out there!", 12); return
        d = 1 if self.x < w.cols // 2 else -1
        self.home_x = self.x
        w.ball.throw(self.x + 3, self.ground - 3, d)

    def trick(self, w):
        if self.state not in IDLE: return
        if self.food < 20:
            self.set_state("front", 16); self.say("treat first? (f)", 16); return
        kind = random.choice(["roll", "spin", "beg", "hop"])
        if kind == "roll":
            self.seq = [("front", 3), ("belly", 4), ("belly2", 4), ("belly", 4), ("front", 3)]
            self.say("watch this!", 10)
        elif kind == "spin":
            self.seq = [("right", 2), ("front", 2), ("left", 2), ("front", 2)] * 2
            self.say("spin~!", 10)
        elif kind == "beg":
            self.seq = [("beg", 4), ("beg2", 4)] * 3
            self.say("hi hi!", 10)
        else:
            self.seq = [("hop", 3), ("front", 2)] * 3
            self.say("boing!", 10)
        self.set_state("trick")

    def call(self, w, tx=None, lost_ok=True):
        if self.state not in IDLE: return
        self.tx = clamp(w.cols // 2 - 4 if tx is None else tx, 1, w.cols - DOG_W - 1)
        if lost_ok and abs(self.tx - self.x) > 6 and random.random() < 0.5:
            self.lost = random.randint(8, 14)              # 路痴: wrong way first
            self.dx = -1 if self.tx > self.x else 1
            self.say(random.choice(["Coming! ...?", "Where??", "Huh? where?"]), 12)
        else:
            self.lost = 0
            self.say(random.choice(["Coming!", "!!", "Woof!"]), 10)
        self.set_state("come")

    def sit(self):
        if self.state in IDLE and self.state != "sleep":
            self.set_state("front", 30); self.say("*sits*", 12)
            self.mood = min(100, self.mood + 2)

    def hello(self):
        if self.state == "sleep":
            self.say("zz... 5 more min...", 16); return
        self.hop = 2
        self.say(random.choice(HELLO), 12)

    # ── behaviour ──
    def move_toward(self, tx, cols):
        tx = clamp(tx, 1, cols - DOG_W - 1)
        if abs(tx - self.x) <= self.speed:
            self.x = tx; return True
        self.dx = 1 if tx > self.x else -1
        self.x += self.dx * self.speed
        return False

    def wander(self, cols):
        nx = self.x + self.dx * self.speed
        if nx < 1 or nx + DOG_W >= cols:
            self.dx = -self.dx; nx = self.x + self.dx * self.speed
        self.x = nx

    def update(self, w):
        cols = w.cols
        self.ground = w.rows - 3
        self.x = clamp(self.x, 1, max(1, cols - DOG_W - 1))
        st = self.state

        # needs slowly drift
        if w.tick % 90 == 0:  self.food = max(0, self.food - 1)
        if w.tick % 140 == 0: self.mood = max(0, self.mood - (2 if self.food < 25 else 1))

        # toys and food beat everything when she's not busy
        if st in IDLE:
            if w.bone.active:
                self.say("*sniff* ...!" if st == "sleep" else "!! food?", 12)
                self.set_state("food"); st = "food"
            elif w.ball.active and not self.carry:
                self.say("!!", 8); self.set_state("fetch"); st = "fetch"

        if st == "walk":
            self.wander(cols)
            b, bird = w.butterfly, w.bird
            r = random.random()
            if b.active and not b.busy and abs(b.x - self.x) < 18 and abs(b.y - self.y) < 7:
                self.set_state("chase", 60)
            elif bird.active and abs(bird.x - self.x) < 20:
                self.set_state("lookat", 12)
                self.dx = 1 if bird.x > self.x else -1
                if random.random() < 0.4:
                    self.say("Woof! Woof!", 10); bird.scare()
            elif r < 0.006 or (is_night() and r < 0.012):
                self.set_state("sit", random.randint(12, 20))
            elif r < 0.009 and self.mood < 30 and not self.b_timer:
                self.set_state("front", 24); self.say(random.choice(LONELY), 20)
            elif r < 0.012 and self.food < 25 and not self.b_timer:
                self.set_state("front", 24); self.say(random.choice(HUNGRY), 20)
            elif r < 0.020 and self.mood > 70 and not self.hop:
                self.hop = 2
                w.particles.append(Particle(self.x + 3, self.y - 1, "♪", fg("yellow"), 8, dx=1, every=2))
            elif r < 0.035 and not self.b_timer:          # 路痴: second-guesses herself
                self.dx = -self.dx
                self.say(random.choice(LOST), 10)

        elif st == "chase":
            b = w.butterfly
            self.timer -= 1
            if not b.active or b.busy:
                self.set_state("walk")
            elif abs(b.x - self.x - 3) < 4 and abs(b.y - self.y) <= 4:
                b.respawn(cols, w.rows)
                w.sparkle(self.x + 3, self.y - 1)
                self.say("Got it!!", 14); self.mood = min(100, self.mood + 5)
                self.set_state("walk")
            elif self.timer <= 0:
                self.say(random.choice(["aww...", "too fast~", "next time!"]), 12)
                self.set_state("walk")
            else:
                self.move_toward(b.x - 3, cols)
                if abs(b.x - self.x - 3) < 8 and not self.hop and random.random() < 0.3:
                    self.hop = 2

        elif st == "lookat":
            self.timer -= 1
            if self.timer <= 0: self.set_state("walk")

        elif st == "sit":
            self.timer -= 1
            self.maybe_perch(w)
            if self.timer <= 0:
                nxt = random.choice(["sleep", "dig", "walk", "front"])
                if is_night() or self.food < 15: nxt = "sleep"
                self.set_state(nxt, {"sleep": random.randint(60, 120), "dig": 16,
                                     "front": 20}.get(nxt, 0))
                if nxt == "sleep" and is_night() and not self.b_timer:
                    self.say(random.choice(SLEEPY), 16)

        elif st == "front":
            self.timer -= 1
            self.maybe_perch(w)
            if self.timer <= 0: self.set_state("walk")

        elif st == "sleep":
            self.timer -= 1
            self.maybe_perch(w)
            if w.tick % 9 == 0:
                w.particles.append(Particle(self.x + (6 if self.dx >= 0 else 1), self.y,
                                            random.choice(["z", "Z"]), fg("dcyan"), 12,
                                            dx=1 if self.dx >= 0 else -1, every=3))
            if self.timer <= 0:
                self.say("*yawn*~", 12); self.set_state("walk")

        elif st == "dig":
            self.timer -= 1
            if w.tick % 2 == 0:
                w.particles.append(Particle(self.x + random.choice([1, 6]), self.y + 2,
                                            random.choice([".", ",", "'"]), fg("brown"), 4,
                                            dx=random.choice([-1, 1]), dy=0, every=1))
            if self.timer <= 0:
                if random.random() < 0.3:
                    find = random.choice(FINDS)
                    self.say(find, 16)
                    if find == "found a bone!": self.food = min(100, self.food + 10)
                    self.set_state("happy", 12)
                else:
                    self.set_state("walk")

        elif st in ("happy", "belly"):
            self.timer -= 1
            if w.tick % 6 == 0:
                w.particles.append(Particle(self.x + random.randint(1, 6), self.y - 1, "♥",
                                            fg(random.choice(["pink", "red"])), 10, wobble=True))
            if st == "happy" and self.mood > 60 and not self.hop and random.random() < 0.08:
                self.hop = 2
            if self.timer <= 0:
                if st == "belly": self.set_state("front", 10); self.say("hehe~ ♥", 10)
                else: self.set_state("walk")

        elif st == "trick":
            if self.timer <= 0:
                if not self.seq:
                    self.say(random.choice(["ta-da!", "good girl?", "★ ta-da ★"]), 16)
                    w.sparkle(self.x + 3, self.y - 1)
                    self.mood = min(100, self.mood + 6); self.stats["tricks"] += 1
                    self.set_state("happy", 14)
                else:
                    self.pose, self.timer = self.seq.pop(0)
                    if self.pose == "hop": self.hop = 2
            self.timer -= 1

        elif st == "come":
            if self.lost > 0:
                self.lost -= 1; self.wander(cols)
                if self.lost == 0:
                    self.say("Oh! there you are!", 12); self.speed = 2
            elif self.move_toward(self.tx, cols):
                self.set_state("front", 24)
                self.say(random.choice(["Here I am~", "Woof! ♥", "I found you!"]), 14)
                self.mood = min(100, self.mood + 3)

        elif st == "fetch":
            ball = w.ball
            if not ball.active:
                self.set_state("walk")
            elif self.move_toward(int(ball.x) - 3, cols) and ball.grounded():
                ball.active = False; self.carry = True
                self.say("got it!", 10); self.set_state("return")

        elif st == "return":
            if self.move_toward(self.home_x, cols):
                self.carry = False
                self.stats["fetches"] += 1
                self.mood = min(100, self.mood + 8)
                self.set_state("front", 24)
                self.say(random.choice(["Again? Again!", "again! (b)", "Woof! ♥"]), 18)

        elif st == "food":
            bone = w.bone
            if not bone.active:
                self.set_state("walk")
            else:
                tx = bone.x - 6 if self.x < bone.x else bone.x + 3
                if self.move_toward(tx, cols) and bone.landed:
                    self.dx = 1 if bone.x > self.x else -1
                    self.set_state("eat", 24); self.say("nom nom", 14)

        elif st == "eat":
            self.timer -= 1
            w.bone.bites = (24 - self.timer) // 7
            if w.tick % 4 == 0:
                w.particles.append(Particle(w.bone.x + 1, w.rows - 2, random.choice([".", "'", "`"]),
                                            fg("bwhite"), 4, dx=random.choice([-1, 1]), every=1))
            if self.timer <= 0:
                full = self.food > 85
                w.bone.active = False
                self.food = min(100, self.food + 35); self.mood = min(100, self.mood + 5)
                self.stats["treats"] += 1
                self.say("so full..." if full else random.choice(["yum!", "delicious~", "more?"]), 14)
                self.set_state("happy", 12)

        # tiny things
        if self.hop > 0: self.hop -= 1
        if self.blink > 0: self.blink -= 1
        elif random.random() < 0.03: self.blink = 1
        self.lift = 2 if w.butterfly.perched else 0

        if self.b_timer > 0:
            self.b_timer -= 1
            if self.b_timer == 0: self.bubble = ""
        elif random.random() < 0.004 and self.state in ("walk", "sit"):
            pool = CHATTER
            if self.food < 25: pool = HUNGRY
            elif self.mood < 30: pool = LONELY
            elif is_night(): pool = SLEEPY
            self.say(random.choice(pool), 16)

    def maybe_perch(self, w):
        b = w.butterfly
        if b.active and not b.busy and abs(b.x - self.x) < 25 and random.random() < 0.02:
            b.land_on(self)

    # ── drawing ──
    def eyes(self):
        if self.blink: return "--"
        if self.food < 25: return ".."
        if self.mood < 25: return ";;"
        return "oo"

    def get_sprite(self):
        st, f, e = self.state, self.frame, self.eyes()
        wag = 1 if f % 2 else -1
        if st == "trick":
            p = self.pose
            if p == "right": return side(1, "^^")
            if p == "left":  return side(-1, "^^")
            if p in POSES:   return POSES[p]
            return front("^^", wag=wag)
        if st == "walk" or (st == "come" and self.lost):
            return side(self.dx, e, tail=">" if f % 2 == 0 else "~")
        if st in ("chase", "fetch", "food", "come"):
            return side(self.dx, "oo", "!!", "=>")
        if st == "return":
            return side(self.dx, "^^", tail="~" if f % 2 else "^")
        if st == "eat":
            return side(self.dx, "^^", "''" if f % 4 < 2 else "ww")
        if st == "lookat":
            return side(self.dx, e, tail="~")
        if st == "dig":
            return POSES["dig"][f % 2]
        if st == "sleep":
            return POSES["sleep_r" if self.dx >= 0 else "sleep_l"]
        if st == "happy":
            return front("♥♥" if f % 6 < 3 else "^^", wag=wag)
        if st == "belly":
            return POSES["belly" if f % 2 else "belly2"]
        if st == "front":
            return front(e, wag=wag if self.mood > 50 else 0)
        return front(e)                                     # sit

    def bubble_rect(self, cols):
        w = dw(self.bubble) + 4
        bx = clamp(self.x - 1, 1, max(1, cols - w - 1))
        by = max(2, self.y - 3 - self.lift)
        return bx, by, w

    def erase(self):
        if self._drawn: erase(*self._drawn)
        if self._bdrawn: erase(*self._bdrawn)
        self._drawn = self._bdrawn = None

    def draw(self):
        sprite = self.get_sprite()
        col = fg("dwhite") if self.state == "sleep" else fg("bwhite")
        put_sprite(self.x, self.y, sprite, col)
        if self.carry:                                     # ball in her mouth
            put(self.x + (6 if self.dx >= 0 else 1), self.y + 1, "o", fg("red"))
        self._drawn = (self.x, self.y, DOG_W + 1, DOG_H)
        self.frame += 1

    def draw_bubble(self, cols):
        if self.bubble:
            bx, by, w = self.bubble_rect(cols)
            px = clamp(self.x + 3 - bx, 1, w - 2)
            put(bx, by,     "╭" + "─" * (w - 2) + "╮", fg("cyan"))
            put(bx, by + 1, "│ " + self.bubble + " │", fg("cyan"))
            put(bx, by + 2, "╰" + "─" * (px - 1) + "v" + "─" * (w - 2 - px) + "╯", fg("cyan"))
            self._bdrawn = (bx, by, w + 1, 3)

# ── BIRD ──────────────────────────────────────────────────
class Bird:
    def __init__(self):
        self.active, self.frame, self.speed = False, 0, 2
        self.x = self.y = 0; self.dx = 1
        self.spawn_timer = random.randint(60, 120)

    def respawn(self, cols, rows):
        self.dx = random.choice([-1, 1]); self.speed = 2
        self.x = 1 if self.dx > 0 else cols - BIRD["w"] - 1
        self.y = random.randint(4, max(4, rows // 3))
        self.active = True

    def scare(self): self.speed = 4; self.y = max(3, self.y - 1)

    def update(self, cols, rows):
        if not self.active:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                self.respawn(cols, rows); self.spawn_timer = random.randint(80, 160)
            return
        self.x += self.dx * self.speed
        if self.x < 0 or self.x > cols: self.active = False

    def erase(self):
        if self.active: erase(self.x, self.y, BIRD["w"] + 1, BIRD["h"])
    def draw(self):
        if not self.active: return
        frames = BIRD["fly_r"] if self.dx > 0 else BIRD["fly_l"]
        put_sprite(self.x, self.y, frames[self.frame % 2], fg("cyan"))
        self.frame += 1

# ── BUTTERFLY ─────────────────────────────────────────────
class Butterfly:
    def __init__(self, cols, rows):
        self.x, self.y = cols // 3, rows // 2
        self.dx, self.dy = random.choice([-1, 1]), random.choice([-1, 0, 1])
        self.active, self.frame = True, 0
        self.landing, self.perched, self.dog = False, 0, None

    @property
    def busy(self): return self.landing or self.perched > 0

    def respawn(self, cols, rows):
        self.x = random.randint(10, max(10, cols - 10))
        self.y = random.randint(5, max(5, rows - 8))
        self.dx, self.dy = random.choice([-1, 1]), random.choice([-1, 0, 1])
        self.landing, self.perched = False, 0

    def land_on(self, dog):
        self.dog, self.landing = dog, True

    def update(self, cols, rows):
        d = self.dog
        if self.busy and d.state not in ("sit", "sleep", "front"):
            self.landing, self.perched, self.dy = False, 0, -1   # she moved — flutter off
        if self.landing:
            tx, ty = d.x + 2, d.y - 2
            self.x += (tx > self.x) - (tx < self.x)
            self.y += (ty > self.y) - (ty < self.y)
            if (self.x, self.y) == (tx, ty):
                self.landing, self.perched = False, random.randint(40, 70)
                if d.state != "sleep": d.say("!! ...don't move", 14)
            return
        if self.perched:
            self.perched -= 1
            self.x, self.y = d.x + 2, d.y - 2
            if self.perched == 0: self.dy = -1
            return
        self.x += self.dx; self.y += self.dy
        if self.x < 2 or self.x + BUTTERFLY["w"] >= cols - 1: self.dx = -self.dx
        if self.y < 4 or self.y + BUTTERFLY["h"] >= rows - 4: self.dy = -self.dy
        self.x = clamp(self.x, 1, max(1, cols - 5)); self.y = clamp(self.y, 3, max(3, rows - 5))
        if random.random() < 0.06: self.dx = -self.dx
        if random.random() < 0.04: self.dy = random.choice([-1, 0, 1])

    def erase(self): erase(self.x, self.y, BUTTERFLY["w"] + 1, BUTTERFLY["h"])
    def draw(self):
        flap = self.frame % 2 if not self.perched else (self.frame // 4) % 2
        put_sprite(self.x, self.y, BUTTERFLY["frames"][flap], fg("magenta"))
        self.frame += 1

# ── WORLD ─────────────────────────────────────────────────
class World:
    def __init__(self, cols, rows):
        self.cols, self.rows, self.tick = cols, rows, 0
        self.particles, self.show_help = [], True
        self.ball, self.bone = Ball(), Bone()
        self.bird, self.butterfly = Bird(), Butterfly(cols, rows)

    def burst(self, x, y, ch, color, n):
        for i in range(n):
            self.particles.append(Particle(x + i * 2 - n, y, ch, color, 10 + i * 2, wobble=True))

    def sparkle(self, x, y):
        for dx, dy in [(-2, 0), (2, 0), (0, -1), (-1, -1), (1, -1)]:
            self.particles.append(Particle(x, y, random.choice(["*", "+", "·"]), fg("byellow"),
                                           5, dx=dx, dy=dy, every=2))

def bar(n, full, empty):
    k = clamp(round(n / 20), 0, 5)
    return full * k + empty * (5 - k)

def draw_status(dog):
    st = "lost" if dog.state == "come" and dog.lost else dog.state
    put(2, 1, " " * min(70, COLS - 3))
    put(2, 1, "Jiao Jiao", BOLD + fg("bwhite"))
    put(12, 1, bar(dog.mood, "♥", "♡"), fg("pink"))
    put(18, 1, " " + bar(dog.food, "●", "○"), fg("yellow"))
    put(25, 1, STATUS.get(st, ""), DIM)

def draw_hint(w):
    erase(1, w.rows, w.cols)
    if not w.show_help:
        msg = "h help · q quit"
    else:
        msg = next((m for m in (
            "p pet · f feed · b ball · t trick · c call · s sit · ␣ hi · click her! · h hide · q quit",
            "p pet · f feed · b ball · t trick · c call · s sit · ␣ hi · q quit",
            "p f b t c s ␣ · h · q") if len(m) <= w.cols - 2), "q quit")
    put(max(1, w.cols - len(msg) - 1), w.rows, msg, DIM)

# ── INPUT ─────────────────────────────────────────────────
TOKEN = re.compile(r"\x1b\[<(\d+);(\d+);(\d+)([Mm])|\x1b\[[0-9;?]*[ -/]*[@-~]|\x1bO.|\x1b|.", re.S)

class Input:
    """Non-blocking keyboard + mouse clicks (xterm SGR mouse mode)."""
    def __enter__(self):
        self.ok, self.old, self.wmode = False, None, None
        try:
            if IS_WIN:
                self.ok = True
                import ctypes
                k = ctypes.windll.kernel32; h = k.GetStdHandle(-10)
                mode = ctypes.c_uint32()
                if k.GetConsoleMode(h, ctypes.byref(mode)):
                    self.wmode = mode.value
                    # VT input (so mouse arrives as escape codes), quick-edit off
                    k.SetConsoleMode(h, (mode.value | 0x200 | 0x80) & ~0x40)
            elif sys.stdin.isatty():
                self.fd = sys.stdin.fileno()
                self.old = termios.tcgetattr(self.fd)
                tty.setcbreak(self.fd)
                self.ok = True
        except Exception:
            pass
        if self.ok: sys.stdout.write("\033[?1000h\033[?1006h")
        return self

    def __exit__(self, *exc):
        sys.stdout.write("\033[?1000l\033[?1006l")
        try:
            if self.old is not None:
                termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)
            if self.wmode is not None:
                import ctypes
                k = ctypes.windll.kernel32; k.SetConsoleMode(k.GetStdHandle(-10), self.wmode)
        except Exception:
            pass

    def _raw(self):
        if not self.ok: return ""
        if IS_WIN:
            out = []
            while msvcrt.kbhit():
                c = msvcrt.getwch()
                if c in "\x00\xe0": msvcrt.getwch(); continue
                out.append(c)
            return "".join(out)
        r, _, _ = select.select([self.fd], [], [], 0)
        return os.read(self.fd, 1024).decode("utf-8", "ignore") if r else ""

    def events(self):
        evs = []
        for m in TOKEN.finditer(self._raw()):
            if m.group(1) is not None:
                b, x, y, kind = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
                if kind == "M" and b < 32 and b & 3 == 0:
                    evs.append(("click", x, y))
            elif not m.group(0).startswith("\x1b"):
                evs.append(("key", m.group(0)))
        return evs

# ── MAIN ──────────────────────────────────────────────────
def handle(ev, dog, w):
    if ev[0] == "click":
        _, x, y = ev
        if dog.contains(x, y): dog.pet(w)
        else: dog.call(w, x - 4, lost_ok=False)
        return True
    k = ev[1].lower()
    if k in ("q", "\x03"): return False
    if   k == "p": dog.pet(w)
    elif k == "f": dog.feed(w)
    elif k == "b": dog.throw(w)
    elif k == "t": dog.trick(w)
    elif k == "c": dog.call(w)
    elif k == "s": dog.sit()
    elif k == " ": dog.hello()
    elif k == "h": w.show_help = not w.show_help; draw_hint(w)
    return True

def redraw_all(w):
    _buf.append("\033[2J")
    build_bg(w.cols, w.rows); draw_bg(); draw_hint(w)

def run():
    global COLS, ROWS
    COLS, ROWS = shutil.get_terminal_size((80, 24))
    sys.stdout.write("\033[?1049h\033[?25l")             # alt screen, hide cursor
    w = World(COLS, ROWS)
    dog = Dog(COLS // 2 - 4, ROWS - 3)
    if is_night(): dog.say("*yawn* it's late~", 20)
    else: dog.say(random.choice(["Woof! ♥", "Hi hi!", "I missed you!"]), 20)
    try:
        with Input() as inp:
            redraw_all(w)
            running = True
            while running:
                size = shutil.get_terminal_size((80, 24))
                if size != (COLS, ROWS):
                    COLS, ROWS = size; w.cols, w.rows = size
                    dog._drawn = dog._bdrawn = None
                    redraw_all(w)

                for ev in inp.events():
                    running = handle(ev, dog, w) and running

                # erase everything, step the world, draw everything (one flush per frame)
                for p in w.particles: p.erase()
                w.bone.erase(); w.ball.erase(); w.bird.erase(); w.butterfly.erase(); dog.erase()

                w.tick += 1
                w.bird.update(COLS, ROWS)
                w.butterfly.update(COLS, ROWS)
                w.ball.update(); w.bone.update()
                dog.update(w)
                w.particles = [p for p in w.particles if p.update()]

                w.bone.draw(); w.ball.draw(); w.bird.draw(); w.butterfly.draw()
                dog.draw()
                for p in w.particles: p.draw()
                dog.draw_bubble(COLS)
                draw_status(dog)
                flush()

                time.sleep(0.08 if dog.state in RUN else 0.12)
    except KeyboardInterrupt:
        pass
    finally:
        _buf.clear()
        sys.stdout.write("\033[?25h\033[?1049l")
        sys.stdout.flush()
    s = dog.stats
    print(f"Goodbye~ Woof! ♥  (pets: {s['pets']} · treats: {s['treats']} · "
          f"fetches: {s['fetches']} · tricks: {s['tricks']})")

if __name__ == "__main__":
    run()
