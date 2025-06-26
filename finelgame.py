import pygame
import random
import sys
import math

# الإعدادات العامة
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
DARK_BLUE = (30, 30, 100)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
YELLOW = (255, 200, 0)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jetpack CHUCK M&B - جيت باك")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# إضافة موسيقى لكل مستوى
level_music = {
    0: "sound/theme.mp3",
    1: "sound/lev1.mp3",
    2: "sound/lev2.mp3",
    3: "sound/lev3.mp3"
}

def play_level_music(level):
    global music_loaded
    try:
        music_file = level_music.get(level, "sound/theme.mp3")
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)
        music_loaded = True
    except Exception as e:
        print(f"⚠️ خطأ في تحميل ملف الموسيقى: {e}")
        music_loaded = False

# تحميل الموسيقى الرئيسية للمنيو
try:
    pygame.mixer.music.load("sound/theme.mp3")
    music_loaded = True
except:
    print("⚠️ لم يتم العثور على ملف الموسيقى theme.mp3")
    music_loaded = False

# تحميل الصور مرة واحدة
projectile_image = None

try:
    projectile_image = pygame.image.load("ITEMS/BB1.png").convert_alpha()
    projectile_image = pygame.transform.scale(projectile_image, (30, 30))
except:
    print("⚠️ لم يتم العثور على بعض الصور")

# تحميل صور العدو الأخير لكل مرحلة
boss_images = {
    1: "final boss pic/T12.png",
    2: "final boss pic/boss2.png",
    3: "final boss pic/boss3.png"
}
loaded_boss_images = {}
for level, img_path in boss_images.items():
    try:
        img = pygame.image.load(img_path).convert_alpha()
        loaded_boss_images[level] = pygame.transform.scale(img, (220, 220))
    except:
        loaded_boss_images[level] = None

# Backgrounds
background_images = {
    1: "background pic/B1.png",
    2: "background pic/B2.png",
    3: "background pic/B3.png"
}
loaded_backgrounds = {}
for level, img_path in background_images.items():
    try:
        img = pygame.image.load(img_path).convert()
        loaded_backgrounds[level] = pygame.transform.scale(img, (WIDTH, HEIGHT))
    except:
        loaded_backgrounds[level] = None

# صورة القلب
try:
    heart_img = pygame.image.load("ITEMS/T14.png").convert_alpha()
    heart_img = pygame.transform.scale(heart_img, (60, 60))
except:
    heart_img = None

# صورة العملة الحمراء
try:
    red_coin_img = pygame.image.load("ITEMS/T6.png").convert_alpha()
    red_coin_img = pygame.transform.scale(red_coin_img, (70, 70))
except:
    red_coin_img = None

try:
    gold_coin_img = pygame.image.load("ITEMS/coin.png").convert_alpha()
    gold_coin_img = pygame.transform.scale(gold_coin_img, (38, 38))
except:
    gold_coin_img = None
    print("⚠️ لم يتم العثور على ملف صورة العملة الذهبية ITEMS/T1.png")
# Enemy sprites
enemy_sprites = {
    1: "rocket pic/R1.png",
    2: "rocket pic/r2.png",
    3: "rocket pic/r3.png"
}
loaded_enemy_sprites = {}
for level, img_path in enemy_sprites.items():
    try:
        img = pygame.image.load(img_path).convert_alpha()
        loaded_enemy_sprites[level] = pygame.transform.scale(img, (90, 60))
    except:
        loaded_enemy_sprites[level] = None

# Sound effects
missile_hit_sound = None
try:
    missile_hit_sound = pygame.mixer.Sound("sound/missile_hit.wav")
    missile_hit_sound.set_volume(1.0)
except:
    print("Warning: missile_hit.wav not found. Missile hit sound will not play.")

hurtsound = None
try:
    hurtsound = pygame.mixer.Sound("sound/hurt.wav")
    hurtsound.set_volume(1.0)
except:
    print("Warning: hurt.wav not found. Hurt sound will not play.")

# صوت إطلاق القذيفة
gun_sound = None
try:
    gun_sound = pygame.mixer.Sound("sound/GUN1.mp3")
    gun_sound.set_volume(0.5)
except:
    print("Warning: GUN1.MP3 not found. Gun sound will not play.")

item_collect_sound = None
try:
    item_collect_sound = pygame.mixer.Sound("sound/videoplayback.wav")
    item_collect_sound.set_volume(0.1)
except:
    print("Warning: item_collect.wav not found. Item collect sound will not play.")


# العدو الخاص
class BossEnemy:
    def __init__(self, level=1):
        self.image = loaded_boss_images.get(level)
        self.x = WIDTH + 100
        self.y = HEIGHT // 2 - 60
        self.width = 220
        self.height = 220
        self.speed = 0.5
        self.target_x = WIDTH - self.width - 10
        self.health = 150 + (level - 1) * 50
        self.last_shot_time = pygame.time.get_ticks()
        self.shot_interval = 2000 - (level - 1) * 200
        self.direction = 1  
        if self.shot_interval < 500: self.shot_interval = 500

    def update(self):
        if self.x > self.target_x:
            self.x -= self.speed
        else:
            self.x = self.target_x
         
        # حركة لأعلى ولأسفل
        self.y += self.direction * 2
        if self.y <= 0 or self.y >= HEIGHT - self.height:
            self.direction *= -1
         
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shot_interval:
            self.last_shot_time = now
            for _ in range(3):
                small_enemy = Obstacle(self.x + self.width // 2, 5, level=current_level)
                obstacles.append(small_enemy)

        if now - self.last_shot_time >= self.shot_interval:
            obstacles.append(Obstacle(self.x, speed=7, level=current_level))

    def draw(self):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, self.width, 8))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.width * (self.health / 150), 8))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

def check_victory():
    global current_level, game_state
    if boss_defeated:
        if current_level == 1:
            try:
                current_background = pygame.image.load("win pic/win1.png").convert()
                screen.blit(current_background, (0, 0))
            except:
                screen.fill(DARK_BLUE)
            victory_msg = font.render("You have completed Level 1 PRESS 'SPACE' TO CONTNUE!", True, (0, 128, 0))
            screen.blit(victory_msg, (WIDTH // 2 - victory_msg.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            wait_for_space()
            current_level = 2
            show_level_transition(1)
            reset_game_state(current_level)
        elif current_level == 2:
            try:
                current_background = pygame.image.load("win pic/win2.jpg").convert()
                screen.blit(current_background, (0, 0))
            except:
                screen.fill(DARK_BLUE)
            victory_msg = font.render("You have completed Level 2 PRESS 'SPACE' TO CONTNUE!", True, (0, 128, 0))
            screen.blit(victory_msg, (WIDTH // 2 - victory_msg.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            wait_for_space()
            current_level = 3
            show_level_transition(2)
            reset_game_state(current_level)
        elif current_level == 3:
            try:
                current_background = pygame.image.load("win pic/win3.jpg").convert()
                screen.blit(current_background, (0, 0))
            except:
                screen.fill(DARK_BLUE)
            victory_msg = font.render("You have completed Level 3 PRESS 'SPACE' TO CONTNUE!", True, (0, 128, 0))
            screen.blit(victory_msg, (WIDTH // 2 - victory_msg.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            wait_for_space()
            show_level_transition(3)
            game_state = "menu"
            main_menu() 

def wait_for_space():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def show_level_transition(completed_level):
    global game_state, current_level
    
    # إيقاف الموسيقى الحالية لضمان سماع صوت الفوز بوضوح
    pygame.mixer.music.stop()
    
    # تحميل صوت الفوز وتشغيله
    win_sound = None
    try:
        win_sound = pygame.mixer.Sound(f"sound/win{completed_level}.mp3")
        win_sound.set_volume(1.0)  # ضبط الصوت لأعلى مستوى
        win_sound.play()
        sound_length = win_sound.get_length() * 1000  # طول الصوت بالميلي ثانية
        print(f"تم تشغيل صوت الفوز للمستوى {completed_level}")
    except Exception as e:
        print(f"⚠️ لم يتم العثور على ملف الصوت win{completed_level}.mp3: {e}")
        win_sound = None
        sound_length = 3000  # 3 ثواني كبديل
    
    # تحميل صور شاشة الفوز
    images = []
    try:
        img1 = pygame.image.load(f"win pic/stage{completed_level+1}_win_1.png").convert()
        img1 = pygame.transform.scale(img1, (WIDTH, HEIGHT))
        images.append(img1)
    except:
        images.append(None)
        print(f"⚠️ لم يتم العثور على ملف الصورة stage{completed_level+1}_win_1.png")
    
    try:
        img2 = pygame.image.load(f"win pic/stage{completed_level+1}_win_2.png").convert()
        img2 = pygame.transform.scale(img2, (WIDTH, HEIGHT))
        images.append(img2)
    except:
        images.append(None)
        print(f"⚠️ لم يتم العثور على ملف الصورة stage{completed_level+1}_win_2.png")
    
    try:
        img3 = pygame.image.load(f"win pic/stage{completed_level+1}_win_3.png").convert()
        img3 = pygame.transform.scale(img3, (WIDTH, HEIGHT))
        images.append(img3)
    except:
        images.append(None)
        print(f"⚠️ لم يتم العثور على ملف الصورة stage{completed_level+1}_win_3.png")
    
    # نص القصة بين المستويات
    story_texts = {
        1: " With great difficulty, the premature being managed to bring down the first massive mutant creature that blocked his path. It was a monster with sharp claws and glowing eyes, but the being’s agility and the power of his jetpack were enough to overcome it. He felt a brief moment of triumph, but the sound of more creatures emerging from the dark depths of the lab brought him back to reality. This was only the beginning—he had to keep fighting if he wanted to survive.",
        2: "Khadeej delved deeper into the laboratory, skillfully avoiding laser traps and cracked doors. He encountered another creature—this time, an agile being soaring through the air, firing energy projectiles. After a thrilling chase and exchange of fire, Khadeej managed to destroy the creature's power source, causing it to fall. He realized that these beings were growing stronger and more complex, and that he would need to be more cautious and strategic in his movements.",
        3: "After an epic battle against the final creature—an embodiment of all Khadeej’s failed experiments—the scientist finally managed to activate the laboratory’s self-destruct system. The mutated beings exploded one after another, and silence gradually returned to the place. Khadeej emerged from the ruined lab, exhausted but victorious. He had saved the world from a threat of his own creation and learned a harsh lesson about the limits of science and the weight of responsibility. Now, he could finally rest—or perhaps begin inventing something new... but this time, with much greater caution."
    }
    
    story_text = story_texts.get(completed_level, "Level completed! Prepare for the next challenge.")
    
    # تقسيم النص إلى أسطر
    story_lines = []
    current_line = ""
    words = story_text.split()
    
    for word in words:
        test_line = current_line + word + " "
        text_width = font.size(test_line)[0]
        if text_width < WIDTH - 100:
            current_line = test_line
        else:
            story_lines.append(current_line)
            current_line = word + " "
    
    if current_line:
        story_lines.append(current_line)
    
    # متغيرات التحكم
    current_image_index = 0
    last_switch = pygame.time.get_ticks()
    text_y = HEIGHT + 100  # بدء النص من أسفل الشاشة
    scroll_speed = 0.3  # سرعة الصعود
    start_time = pygame.time.get_ticks()
    transition_done = False
    skip_requested = False
    
    while not transition_done:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - last_switch
        
        # تبديل الصور كل 3 ثواني
        if elapsed >= 3000:
            last_switch = current_time
            current_image_index = (current_image_index + 1) % len(images)
        
        # عرض الصورة الحالية
        if images[current_image_index]:
            screen.blit(images[current_image_index], (0, 0))
        else:
            screen.fill(DARK_BLUE)
        
        # عرض النص المتدحرج
        text_y -= scroll_speed
        for i, line in enumerate(story_lines):
            text_surface = font.render(line, True, (255, 165, 0))  # لون برتقالي
            screen.blit(text_surface, (50, text_y + i * 40))
        
        # تطبيق السطوع
        if brightness < 1.0:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)
            alpha = int(255 * (1.0 - brightness))
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))
        
        # التحقق من انتهاء الصوت أو الضغط على Space
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    skip_requested = True
                    transition_done = True
        
        # التحقق من انتهاء الصوت
        if not skip_requested and current_time - start_time > sound_length + 3000:  # زيادة 3 ثواني بعد الصوت
            transition_done = True
        
        pygame.display.flip()
        clock.tick(60)
    
    # الانتقال إلى المستوى التالي
    play_level_music(completed_level + 1)

# اللاعب
class Player:
    def __init__(self, level=1):
        self.level = level
        self.set_player_image(level)
        self.width, self.height = 70, 70
        self.x = 100
        self.y = HEIGHT // 2
        self.speed_y = 0
        self.speed_x = 5
        self.gravity = 0.5
        self.jump_power = -10
        self.lives = 3
        self.has_red_coin = False

    def set_player_image(self, level):
        try:
            if level == 1:
                img_name = "player pic/C2.png"
            if level == 2:
                img_name = "player pic/c41.png"
            if level == 3:
                img_name = "player pic/c61.png"
            
            original_image = pygame.image.load(img_name).convert_alpha()
            self.image = pygame.transform.scale(original_image, (85, 85))
        except:
            self.image = None

    def update(self, keys):
        if keys[pygame.K_SPACE]:
            self.speed_y = self.jump_power
        self.speed_y += self.gravity
        self.y += self.speed_y

        if keys[pygame.K_RIGHT]:
            self.x += self.speed_x
        if keys[pygame.K_LEFT]:
            self.x -= self.speed_x

        self.y = max(0, min(self.y, HEIGHT - self.height))
        self.x = max(0, min(self.x, WIDTH - self.width))

    def draw(self):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


# الصاروخ
class Obstacle:
    def __init__(self, x, speed, level=1):
        self.image = loaded_enemy_sprites.get(level)
        self.width = 60
        self.height = 60
        self.x = x
        self.y = random.randint(50, HEIGHT - 80)
        self.speed = speed

    def update(self):
        self.x -= self.speed

    def draw(self):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class MovingObstacle(Obstacle):
    def __init__(self, x, speed, level=3):
        super().__init__(x, speed, level)
        self.initial_y = self.y
        self.amplitude = 100
        self.frequency = 0.02
        self.time = 0

    def update(self):
        super().update()
        self.time += 1
        self.y = self.initial_y + self.amplitude * math.sin(self.frequency * self.time)


# العملة
class Coin:
    def __init__(self, x, y, shape="circle"):
        self.x = x
        self.y = y
        self.speed = 3
        self.shape = shape
        self.radius = 15
        self.width = 30
        self.height = 30

    def update(self):
        self.x -= self.speed

    def draw(self):
        if gold_coin_img:
            screen.blit(gold_coin_img, (self.x - self.radius, self.y - self.radius))
        else:
            # الرسم الاحتياطي إذا لم يتم تحميل الصورة
            pygame.draw.circle(screen, GOLD, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

# القلوب
class Heart:
    def __init__(self):
        self.x = random.randint(WIDTH, WIDTH + 500)
        self.y = random.randint(50, HEIGHT - 50)
        self.speed = 2
        self.width = 30
        self.height = 30

    def update(self):
        self.x -= self.speed

    def draw(self):
        if heart_img:
            screen.blit(heart_img, (self.x, self.y))
        else:
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


# القذيفة
class Projectile:
    def __init__(self, x, y):
        self.image = projectile_image
        self.x = x
        self.y = y
        self.speed = 10
        self.radius = 8

    def update(self):
        self.x += self.speed

    def draw(self):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


# الإنفجار
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 5

    def update(self):
        self.timer -= 1

    def draw(self):
        if self.timer > 0:
            pygame.draw.circle(screen, GREEN, (self.x, self.y), 7 - self.timer)


# إنشاء العملات الهندسية المرتبة بشكل دائرة
def generate_geometric_coins(shape="circle"):
    coins = []
    center_x = WIDTH + 200
    center_y = HEIGHT // 2
    radius = 100
    if shape == "circle":
        num_coins = 8
        for i in range(num_coins):
            angle = 2 * math.pi * i / num_coins
            x = center_x + radius * math.cos(angle) 
            y = center_y + radius * math.sin(angle) 
            coins.append(Coin(x, y, shape))
    elif shape == "square":
        for i in range(3):
            for j in range(3):
                x = center_x + i * 30 - 60
                y = center_y + j * 30 - 60
                coins.append(Coin(x, y, shape))
    elif shape == "triangle":
        rows = 4
        for i in range(rows):
            for j in range(i + 1):
                x = center_x + (j - i / 2) * 30
                y = center_y + i * 30 - 60
                coins.append(Coin(x, y, shape))
    return coins


# Game state variables
current_level = 1
game_state = "menu"
volume = 1.0
brightness = 1.0
BLUE = (0, 120, 255)
coin_counter = 0 


def reset_game_state(level):
    global player, obstacles, coins, projectiles, explosions, hearts, score, coin_score, projectile_count, start_time, difficulty_increased, game_over, game_over_time, red_coin,coin_counter ,red_coin_collected, boss, boss_defeated, victory_time, last_coin_spawn_time, last_obstacle_spawn_time
    
    player = Player(level)
    obstacles = []
    if level == 1:
        obstacles = [Obstacle(WIDTH + i * 300, 5, level) for i in range(3)]
    elif level == 2:
        obstacles = [Obstacle(WIDTH + i * 250, 7, level) for i in range(5)]
    elif level == 3:
        obstacles = [Obstacle(WIDTH + i * 200, 9, level) for i in range(4)] + \
                    [MovingObstacle(WIDTH + i * 200 + 100, 8, level) for i in range(2)]

    coins = generate_geometric_coins(random.choice(["circle", "square", "triangle"]))
    projectiles = []
    explosions = []
    hearts = []

    coin_counter = 0 
    score = 0
    coin_score = 0
    projectile_count = 0
    start_time = pygame.time.get_ticks()
    difficulty_increased = False
    game_over = False
    game_over_time = 0
    red_coin = None
    red_coin_collected = False
    boss = None
    boss_defeated = False
    victory_time = 0
    last_coin_spawn_time = pygame.time.get_ticks()
    last_obstacle_spawn_time = pygame.time.get_ticks()
    
    if game_state == "menu":
        play_level_music(0)
    else: 
        play_level_music(level)

# شاشة القصة قبل بدء اللعبة
def story_screen():
    global game_state
    
    # إيقاف موسيقى القائمة الرئيسية
    pygame.mixer.music.stop()
    
    # تحميل الصوت الخاص بالقصة
    story_sound = None
    try:
        story_sound = pygame.mixer.Sound("sound/in the start game.mp3")
        story_sound.play()
        story_sound_length = 43000  # طول الصوت 30 ثانية
    except:
        print("⚠️ لم يتم العثور على ملف الصوت in the start game.mp3")
        story_sound = None
        story_sound_length = 43000
    
    # تحميل الصور
    try:
        story_img1 = pygame.image.load("win pic/intro_1.png").convert()
        story_img1 = pygame.transform.scale(story_img1, (WIDTH, HEIGHT))
    except:
        story_img1 = None
        print("⚠️ لم يتم العثور على ملف الصورة intro_1.png")
    try:
        story_img2 = pygame.image.load("win pic/intro_2.png").convert()
        story_img2 = pygame.transform.scale(story_img2, (WIDTH, HEIGHT))
    except:
        story_img2 = None
        print("⚠️ لم يتم العثور على ملف الصورة intro_2.png")
    try:
        story_img3 = pygame.image.load("win pic/intro_3.png").convert()
        story_img3 = pygame.transform.scale(story_img3, (WIDTH, HEIGHT))
    except:
        story_img3 = None
        print("⚠️ لم يتم العثور على ملف الصورة intro_3.png")
    
    # نص القصة
    story_text = "Deep within Vladimir Khaduz's secret laboratory, experiments on genetically modified organisms were in full swing. The scientist Khadij sought to develop supernatural creatures, but a fatal error in the protocol led to catastrophe. The containment units shattered, the mutated creatures broke free, and the lab began descending into rampant chaos. Now, Khadij finds himself surrounded by his own out-of-control creations. He must don his jetpack and use every weapon and technology at his disposal to regain control of his lab and save himself from the very creatures he made with his own hands."
    
    # تقسيم النص إلى أسطر
    story_lines = []
    current_line = ""
    words = story_text.split()
    
    for word in words:
        test_line = current_line + word + " "
        text_width = font.size(test_line)[0]
        if text_width < WIDTH - 100:
            current_line = test_line
        else:
            story_lines.append(current_line)
            current_line = word + " "
    
    if current_line:
        story_lines.append(current_line)
    
    # متغيرات التحكم
    current_image = story_img1
    last_switch = pygame.time.get_ticks()
    text_y = HEIGHT + 100  # بدء النص من أسفل الشاشة مع زيادة المسافة
    scroll_speed = 0.3  # إبطاء سرعة الصعود
    start_time = pygame.time.get_ticks()
    story_done = False
    image_index = 0
    images = [story_img1, story_img2, story_img3]
    
    while not story_done:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - last_switch
        
        # تبديل الصور كل 4 ثواني (زيادة المدة)
        if elapsed >= 4000:
            last_switch = current_time
            image_index = (image_index + 1) % len(images)
            current_image = images[image_index]
        
        # عرض الصورة الحالية
        if current_image:
            screen.blit(current_image, (0, 0))
        else:
            screen.fill(DARK_BLUE)
        
        # عرض النص المتدحرج - تغيير اللون إلى البرتقالي
        text_y -= scroll_speed
        for i, line in enumerate(story_lines):
            # تغيير لون النص إلى البرتقالي (255, 165, 0)
            text_surface = font.render(line, True, (255, 165, 0))
            screen.blit(text_surface, (50, text_y + i * 40))
        
        # تطبيق السطوع
        if brightness < 1.0:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)
            alpha = int(255 * (1.0 - brightness))
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))
        
        # التحقق من انتهاء الصوت أو الضغط على Space
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    story_done = True
        
        # التحقق من انتهاء الصوت
        if current_time - start_time > story_sound_length + 5000:  # زيادة مدة بقاء النص
            story_done = True
        
        pygame.display.flip()
        clock.tick(60)
    
    # إيقاف صوت القصة عند الانتقال إلى اللعبة
    if story_sound:
        story_sound.stop()
    
    # الانتقال إلى اللعبة
    game_state = "playing"
    reset_game_state(1)

# Initial game state
reset_game_state(current_level)


# --- Menu System Functions --- #
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, text_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action
    
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.color
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        pygame.draw.rect(surface, current_color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()


# Fixed menu functions
def options_menu_action():
    global game_state
    game_state = "options"

def developers_info_action():
    global game_state
    game_state = "developers"

def play_menu_music():
    """Plays the menu music if it's not already playing"""
    if not pygame.mixer.music.get_busy():
        try:
            pygame.mixer.music.load("sound/theme.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(volume)
        except:
            print("⚠️ لم يتم العثور على ملف الموسيقى theme.mp3")

def back_to_menu():
    global game_state
    game_state = "menu"
    
def start_game():
    global game_state
    game_state = "story"  # تغيير من "playing" إلى "story"
    pygame.mixer.music.stop()  

def quit_game():
    pygame.quit()
    sys.exit()


def main_menu():
    global game_state
    try:
        menu_background = pygame.image.load("background pic/bbbb.jpg").convert()
        menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
    except:
        menu_background = None

    play_menu_music()

    start_button = Button("Start Game", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, DARK_BLUE, GREEN, YELLOW, start_game)
    options_button = Button("Options", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, DARK_BLUE, GREEN, YELLOW, options_menu_action)
    developers_button = Button("Developers", WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, DARK_BLUE, GREEN, YELLOW, developers_info_action)
    exit_button = Button("Exit", WIDTH // 2 - 100, HEIGHT // 2 + 160, 200, 50, DARK_BLUE, GREEN, YELLOW, quit_game)

    buttons = [start_button, options_button, developers_button, exit_button]

    while game_state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.handle_event(event)

        if menu_background:
            screen.blit(menu_background, (0, 0))
        else:
            screen.fill(DARK_BLUE)

        title_font = pygame.font.SysFont("Arial", 50, bold=True)
        title = title_font.render("Jetpack CHUCK", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        subtitle = font.render("M&B Edition", True, WHITE)
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 160))

        if pygame.mixer.music.get_busy():
            music_indicator = font.render("♪", True, WHITE)
            screen.blit(music_indicator, (WIDTH - 40, 20))

        for button in buttons:
            button.draw(screen)
            
        # تطبيق السطوع
        if brightness < 1.0:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)
            alpha = int(255 * (1.0 - brightness))
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))

        pygame.display.flip()


def options_menu():  
    global game_state, volume, brightness  
    try:
        options_background = pygame.image.load("background pic/bbbb.jpg").convert()  
        options_background = pygame.transform.scale(options_background, (WIDTH, HEIGHT))  
    except:
        options_background = None  

    back_button = Button("Back", 50, 50, 100, 50, DARK_BLUE, GREEN, YELLOW, back_to_menu)  
    increase_volume_button = Button("Increase Vol", 50, 100, 150, 50, DARK_BLUE, GREEN, YELLOW, increase_volume)  
    decrease_volume_button = Button("Decrease Vol", 50, 160, 150, 50, DARK_BLUE, GREEN, YELLOW, decrease_volume)  
    increase_brightness_button = Button("Inc Bright", 50, 220, 150, 50, DARK_BLUE, GREEN, YELLOW, increase_brightness)  
    decrease_brightness_button = Button("Dec Bright", 50, 280, 150, 50, DARK_BLUE, GREEN, YELLOW, decrease_brightness)  

    buttons = [back_button, increase_volume_button, decrease_volume_button, 
              increase_brightness_button, decrease_brightness_button]

    while game_state == "options":  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                sys.exit()  
            for button in buttons:
                button.handle_event(event)

        if options_background:  
            screen.blit(options_background, (0, 0))  
        else:
            screen.fill(DARK_BLUE)  

        for button in buttons:
            button.draw(screen)  

        volume_text = font.render(f"Volume: {int(volume * 100)}%", True, WHITE)  
        screen.blit(volume_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))  

        brightness_text = font.render(f"Brightness: {int(brightness * 100)}%", True, WHITE)  
        screen.blit(brightness_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))  
        
        instructions = [  
            "Controls:",
            "SPACE - Jump",
            "LEFT/RIGHT - Move horizontally",
            "SHIFT - Fire missiles (after collecting red coin)",
            "ESC - Return to menu"
        ]
        
        for i, line in enumerate(instructions):  
            text = font.render(line, True, WHITE)  
            screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 + 80 + i*30))  
            
        # تطبيق السطوع
        if brightness < 1.0:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)
            alpha = int(255 * (1.0 - brightness))
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))

        pygame.display.flip()  

def increase_volume():
    global volume
    if volume < 1.0:
        volume += 0.1
        pygame.mixer.music.set_volume(volume)

def decrease_volume():
    global volume
    if volume > 0.0:
        volume -= 0.1
        pygame.mixer.music.set_volume(volume)

def increase_brightness():
    global brightness
    if brightness < 1.0:
        brightness += 0.1

def decrease_brightness():
    global brightness
    if brightness > 0.0:
        brightness -= 0.1
        
        pygame.display.flip()  


def developers_info():  
    global game_state 
    play_menu_music() 
    try:
        developers_background = pygame.image.load("background pic/bbbb.jpg").convert()  
        developers_background = pygame.transform.scale(developers_background, (WIDTH, HEIGHT))  
    except:
        developers_background = None  

    back_button = Button("Back", 50, 50, 100, 50, DARK_BLUE, GREEN, WHITE, back_to_menu)  

    while game_state == "developers":  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                sys.exit()  
            back_button.handle_event(event)  

        if developers_background:  
            screen.blit(developers_background, (0, 0))  
        else:
            screen.fill(DARK_BLUE)  

        back_button.draw(screen)  

        dev_text = font.render("Developed by: BILAL AHMED & ABDUL-MUMIN SHALOUF", True, WHITE)  
        screen.blit(dev_text, (WIDTH // 2 - dev_text.get_width() // 2, HEIGHT // 2 - 50))  
        
        version_text = font.render("we hope you enjoy our game", True, GOLD)  
        screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, HEIGHT // 2 + 20))  
        
        thanks_text = font.render("Special thanks to our doctor :Nesrin Basher", True, WHITE)  
        screen.blit(thanks_text, (WIDTH // 2 - thanks_text.get_width() // 2, HEIGHT // 2 + 80))  
        
        # تطبيق السطوع
        if brightness < 1.0:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)
            alpha = int(255 * (1.0 - brightness))
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))

        pygame.display.flip()  


# اللعبة
while True:  
    if game_state == "menu":  
        main_menu()  
    elif game_state == "story":  # الحالة الجديدة لشاشة القصة
        story_screen()
    elif game_state == "options":  
        options_menu()  
    elif game_state == "developers":  
        developers_info()  
    elif game_state == "playing":  
        clock.tick(FPS)  
        keys = pygame.key.get_pressed()  
        now = pygame.time.get_ticks()  
        elapsed_seconds = (now - start_time) // 1000  

        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                sys.exit()  
            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_ESCAPE:  
                    game_state = "menu"  
                    try:
                        pygame.mixer.music.load("sound/theme.mp3")  
                        pygame.mixer.music.play(-1)  
                    except:
                        print("⚠️ لم يتم العثور على ملف الموسيقى theme.mp3")  

        coin_spawn_interval = 4000  
        if now - last_coin_spawn_time >= coin_spawn_interval:  
            shape = random.choice(["circle", "square", "triangle"])  
            coins.extend(generate_geometric_coins(shape))  
            last_coin_spawn_time = now  

        obstacle_spawn_interval = 1000  
        if current_level == 2:  
            obstacle_spawn_interval = 800  
        elif current_level == 3:  
            obstacle_spawn_interval = 600  

        if now - last_obstacle_spawn_time > obstacle_spawn_interval:  
            if boss:  
                spawn_x = boss.x + boss.width // 2  
                spawn_y = boss.y + boss.height // 2
            else:  
                spawn_x = WIDTH + random.randint(0, 400)  
                spawn_y = random.randint(50, HEIGHT - 80)  

            if current_level == 1:  
                obstacles.append(Obstacle(spawn_x, 6, current_level))  
            elif current_level == 2:  
                obstacles.append(Obstacle(spawn_x, 8, current_level))  
            elif current_level == 3:  
                if random.random() < 0.7:  
                    obstacles.append(Obstacle(spawn_x, 10, current_level))  
                else:
                    obstacles.append(MovingObstacle(spawn_x, 10, current_level))  

            last_obstacle_spawn_time = now  

        if current_level == 1 and elapsed_seconds >= 30 and not boss and not boss_defeated:  
            boss = BossEnemy(level=current_level) 
        elif current_level == 2 and elapsed_seconds >= 40 and not boss and not boss_defeated:  
            boss = BossEnemy(level=current_level)  
        elif current_level == 3 and elapsed_seconds >= 50 and not boss and not boss_defeated:  
            boss = BossEnemy(level=current_level)  

        if boss:  
            boss.update()  
                

        if boss and not boss_defeated:  
            for proj in projectiles[:]:  
                if boss and proj.get_rect().colliderect(boss.get_rect()):  
                    projectiles.remove(proj)  
                    boss.health -= 1  
                    explosions.append(Explosion(proj.x, proj.y))  
                    if missile_hit_sound:  
                        missile_hit_sound.play()  
                    if boss.health <= 0:  
                        boss_defeated = True  
                        victory_time = pygame.time.get_ticks()  
                        boss = None  

        if game_over:  
            if pygame.time.get_ticks() - game_over_time > 3000:  
                reset_game_state(current_level)  
            else:
                continue  

        can_shoot = (  
            (current_level == 1 and red_coin_collected) or 
            (current_level > 1)
        )

        if can_shoot and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):  
            if projectile_count > 0:  
                if len(projectiles) == 0 or projectiles[-1].x - player.x > 60:  
                    projectiles.append(Projectile(player.x + player.width, player.y + player.height // 2))  
                    projectile_count -= 1  
                    if gun_sound:  
                        gun_sound.play()  

        player.update(keys)  

        visible_obstacles = [obs for obs in obstacles if obs.x > -100 and obs.x < WIDTH + 100]  
        for obs in visible_obstacles:  
            obs.update()  

        for coin in coins[:]:  
            coin.update()  
            if coin.x < -50:  
                coins.remove(coin)  

        if red_coin and not red_coin_collected:  
            red_coin.update()  

        for heart in hearts:  
            heart.update()  

        for proj in projectiles:  
            proj.update()  

        for exp in explosions:  
            exp.update()  

        projectiles = [p for p in projectiles if p.x < WIDTH]  
        explosions = [e for e in explosions if e.timer > 0]  
        hearts = [h for h in hearts if h.x + h.width > 0]  

        for proj in projectiles[:]:  
            for obs in obstacles[:]:  
                if proj.get_rect().colliderect(obs.get_rect()):  
                    explosions.append(Explosion(obs.x + obs.width // 2, obs.y + obs.height // 2))  
                    if missile_hit_sound:  
                        missile_hit_sound.play()  
                    try:
                        obstacles.remove(obs)  
                        projectiles.remove(proj)  
                        break  
                    except:
                        pass  

        if current_level == 1 and elapsed_seconds >= 15 and not red_coin and not red_coin_collected:  
            red_coin = Coin(WIDTH + 100, random.randint(50, HEIGHT - 50))  

        if elapsed_seconds >= 60 and not difficulty_increased:  
            for i in range(3):  
                obstacles.append(Obstacle(WIDTH + random.randint(0, 800), speed=7, level=current_level))  
            difficulty_increased = True  

        for obs in obstacles[:]:  
            if obs.x + obs.width < 0:  
                obstacles.remove(obs)  

        player_rect = player.get_rect()  
        for obs in obstacles[:]:  
            if player_rect.colliderect(obs.get_rect()):  
                player.lives -= 1  
                if missile_hit_sound:  
                    missile_hit_sound.play()
                if hurtsound:
                    hurtsound.play()        
                obstacles.remove(obs)  
                if player.lives <= 0:  
                    game_over = True  
                    game_over_time = pygame.time.get_ticks()  
                break  

        for coin in coins:  
            if player.get_rect().colliderect(coin.get_rect()):  
                coin_counter += 1
                coin_score += 1  
                score += 100  
                projectile_count += 10  
                coins.remove(coin)  
                if item_collect_sound:  
                    item_collect_sound.play()  
                break  

        if red_coin and not red_coin_collected and player.get_rect().colliderect(red_coin.get_rect()):  
            red_coin_collected = True  
            player.has_red_coin = True  
            
            try:
                if current_level == 3:  
                    new_image = pygame.image.load("player pic/c51.png").convert_alpha()  
                else:
                    new_image = pygame.image.load("player pic/c61.png").convert_alpha()  
                
                player.image = pygame.transform.scale(new_image, (80, 80))  
            except Exception as e:
                print(f"⚠️ خطأ في تحميل صورة اللاعب: {e}")  
            
            red_coin = None  
            if item_collect_sound:  
                item_collect_sound.play()  

        if random.randint(0, 300) == 1 and len(hearts) < 2 and player.lives < 3:  
            hearts.append(Heart())  

        for heart in hearts[:]:  
            if player.get_rect().colliderect(heart.get_rect()):  
                if player.lives < 3:  
                    player.lives += 1  
                hearts.remove(heart)  
                if item_collect_sound:  
                    item_collect_sound.play()  

        current_background = loaded_backgrounds.get(current_level, loaded_backgrounds[1])  
        if current_background:  
            screen.blit(current_background, (0, 0))  
        else:
            screen.fill(WHITE)  

        player.draw()  
        for obs in obstacles:  
            obs.draw()  
        for coin in coins:  
            coin.draw()  
        if red_coin and not red_coin_collected:  
            if red_coin_img:  
                screen.blit(red_coin_img, (red_coin.x - 15, red_coin.y - 15))  
            else:
                red_coin.draw()  
        for proj in projectiles:  
            proj.draw()  
        for exp in explosions:  
            exp.draw()  
        for heart in hearts:  
            heart.draw()  

        if boss:  
            boss.draw()  

        score += 1  
        text = font.render(f"Score: {score} | Coins: {coin_counter} |Ammo: {projectile_count} | Lives: {player.lives}", True, BLUE)  
        time_text = font.render(f"Time: {elapsed_seconds}s | Level: {current_level}", True, BLUE)  
        screen.blit(text, (10, 10))  
        screen.blit(time_text, (10, 40))  

        if boss_defeated:  
           
            check_victory()
                 
                    
        # تطبيق السطوع
        if brightness < 1.0:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)
            alpha = int(255 * (1.0 - brightness))
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))

        pygame.display.flip()