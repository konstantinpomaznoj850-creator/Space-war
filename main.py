import pygame
import sys
import random
import math
import os
import asyncio

pygame.init()

# В Pygbag на мобильных браузерах звук часто вешает игру, поэтому отключаем его для веба
if sys.platform == "emscripten":
    AUDIO_OK = False
else:
    try:
        pygame.mixer.init()
        AUDIO_OK = True
    except:
        AUDIO_OK = False

def load_sound(filename):
    if not AUDIO_OK: return None
    try:
        base = os.path.dirname(os.path.abspath(__file__))
        return pygame.mixer.Sound(os.path.join(base, filename))
    except:
        return None

snd_shoot   = load_sound("shoot.wav")
snd_laser   = load_sound("laser.wav")
snd_explode = load_sound("explode.wav")
snd_coin    = load_sound("coin.wav")
snd_powerup = load_sound("powerup.wav")
snd_hit     = load_sound("hit.wav")

if sys.platform == "emscripten":
    screen = pygame.display.set_mode((800, 600))
else:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

WIDTH, HEIGHT = screen.get_size()
MIN_DIM = min(WIDTH, HEIGHT)

# Цвета
BLACK = (20, 20, 20)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
PURPLE = (200, 0, 255)
GOLD = (255, 215, 0)
GRAY = (60, 60, 60)
LIGHT_GRAY = (180, 180, 180)
LORE_COLOR = (150, 200, 255)
DARK_RED = (139, 0, 0)
CYAN = (0, 255, 255)
RAINBOW = (255, 0, 128)
BOSS_COLOR = (180, 0, 80)

BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER = (80, 80, 80)
BUTTON_DISABLED = (30, 30, 30)
ACTIVE_COLOR = (0, 200, 100)

title_font = pygame.font.SysFont("Arial", int(MIN_DIM * 0.08), bold=True)
font       = pygame.font.SysFont("Arial", int(MIN_DIM * 0.05), bold=True)
small_font = pygame.font.SysFont("Arial", int(MIN_DIM * 0.035))

LANG = {
    "RU": {
        "play": "ИГРАТЬ", "shop": "МАГАЗИН", "settings": "НАСТРОЙКИ", "exit": "ВЫХОД",
        "achieve": "ДОСТИЖЕНИЯ", "back": "НАЗАД", "coins": "Монеты",
        "ships": "КОРАБЛИ", "upgrades": "УЛУЧШЕНИЯ", "equip": "НАДЕТЬ",
        "equipped": "НАДЕТО", "max_lvl": "МАКС. УРОВЕНЬ", "buy": "КУПИТЬ",
        "cancel": "ОТМЕНА", "cost_lbl": "Цена: ", "desc_lbl": "Описание: ", "lore_lbl": "История: ",
        "pause": "ПАУЗА", "resume": "ПРОДОЛЖИТЬ", "menu": "В МЕНЮ",
        "lang_lbl": "Язык: ", "gfx_lbl": "Графика: ",
        "on": "ВКЛ", "off": "ВЫКЛ", "high": "ВЫСОКАЯ", "low": "НИЗКАЯ",
        "wave": "ВОЛНА", "score": "СЧЕТ", "game_over": "ИГРА ОКОНЧЕНА",
        "earned": "Собрано: ", "bomb": "БОМБА", "dmg_upg": "+1 Урон",
        "spd_upg": "Скорость стрельбы", "ach_title": "ДОСТИЖЕНИЯ",
        "a1": "Первая кровь (1 убийство)", "a2": "Ветеран (100 убийств)",
        "a3": "Бог войны (1000 убийств)", "a4": "Первый босс",
        "a5": "Мясник (5 боссов)", "a6": "Богач (1000 монет)",
        "reward": "Награда: 50 монет",
        "n_scout": "РАЗВЕДЧИК", "n_fighter": "ИСТРЕБИТЕЛЬ", 
        "n_destroyer": "ЭСМИНЕЦ", "n_mothership": "МАТКА",
        "n_bomb": "БОМБА", "n_damage": "УРОН", "n_speed": "СКОРОСТЬ",
        "sh_scout": "Скорострельный", "sh_fighter": "Сбалансированный",
        "sh_destroyer": "Больше бомб", "sh_mother": "Регенерация",
        "d_scout": "Быстрый, но хрупкий. Стреляет чаще других.",
        "d_fighter": "Надежный боец с повышенным уроном.",
        "d_destroyer": "Тяжелый корабль с дополнительным запасом бомб.",
        "d_mother": "Крепость. Медленно восстанавливает здоровье.",
        "d_bomb": "Увеличивает максимальный запас бомб на 1.",
        "d_damage": "Увеличивает урон оружия на 1 за уровень.",
        "d_speed": "Уменьшает задержку между выстрелами.",
        "l_scout": "Первый корабль выпускника академии. Легкий, быстрый и дешевый в обслуживании.",
        "l_fighter": "Ветеран пограничных конфликтов. Сочетает в себе скорость и огневую мощь.",
        "l_destroyer": "Тяжелый корабль поддержки. Создан для уничтожения крупных целей.",
        "l_mothership": "Легендарный флагман. Оснащен нанороботами для самовосстановления.",
        "l_bomb": "Экспериментальный заряд, создающий гравитационный импульс.",
        "l_damage": "Улучшенные боеголовки с обедненным ураном.",
        "l_speed": "Модернизированная система охлаждения орудий.",
        "shield": "ЩИТ!"
    },
    "EN": {
        "play": "PLAY", "shop": "SHOP", "settings": "SETTINGS", "exit": "EXIT",
        "achieve": "ACHIEVEMENTS", "back": "BACK", "coins": "Coins",
        "ships": "SHIPS", "upgrades": "UPGRADES", "equip": "EQUIP",
        "equipped": "EQUIPPED", "max_lvl": "MAX LEVEL", "buy": "BUY",
        "cancel": "CANCEL", "cost_lbl": "Cost: ", "desc_lbl": "Description: ", "lore_lbl": "Lore: ",
        "pause": "PAUSED", "resume": "RESUME", "menu": "MAIN MENU",
        "lang_lbl": "Language: ", "gfx_lbl": "Graphics: ",
        "on": "ON", "off": "OFF", "high": "HIGH", "low": "LOW",
        "wave": "WAVE", "score": "SCORE", "game_over": "GAME OVER",
        "earned": "Earned: ", "bomb": "BOMB", "dmg_upg": "+1 Damage",
        "spd_upg": "Shoot Rate", "ach_title": "ACHIEVEMENTS",
        "a1": "First Blood (1 kill)", "a2": "Veteran (100 kills)",
        "a3": "God of War (1000 kills)", "a4": "First Boss",
        "a5": "Butcher (5 bosses)", "a6": "Rich (1000 coins)",
        "reward": "Reward: 50 coins",
        "n_scout": "SCOUT", "n_fighter": "FIGHTER", 
        "n_destroyer": "DESTROYER", "n_mothership": "MOTHERSHIP",
        "n_bomb": "BOMB", "n_damage": "DAMAGE", "n_speed": "SPEED",
        "sh_scout": "Fast Shooting", "sh_fighter": "Balanced",
        "sh_destroyer": "Extra Bombs", "sh_mother": "Regeneration",
        "d_scout": "Fast but fragile. Shoots more often than others.",
        "d_fighter": "Reliable fighter with increased damage.",
        "d_destroyer": "Heavy ship with extra bomb capacity.",
        "d_mother": "Fortress. Slowly regenerates health.",
        "d_bomb": "Increases max bomb capacity by 1.",
        "d_damage": "Increases weapon damage by 1 per level.",
        "d_speed": "Reduces delay between shots.",
        "l_scout": "The first ship of an academy graduate. Light, fast and extremely cheap to maintain.",
        "l_fighter": "A veteran of border conflicts. Combines speed and firepower.",
        "l_destroyer": "A heavy support ship. Designed to destroy large targets.",
        "l_mothership": "A legendary flagship. Equipped with nanobots for self-repair.",
        "l_bomb": "An experimental charge that creates a gravitational pulse.",
        "l_damage": "Improved warheads with depleted uranium.",
        "l_speed": "Upgraded gun cooling system.",
        "shield": "SHIELD!"
    }
}

lang = "RU"
gfx_high = True

def t(key):
    return LANG[lang].get(key, key)

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines

SHIPS = [
    {"name_key": "n_scout", "hp": 1, "cost": 0, "color": GREEN,
     "size": (int(MIN_DIM*0.07), int(MIN_DIM*0.088)), "desc": "sh_scout", "detail": "d_scout", "lore": "l_scout"},
    {"name_key": "n_fighter", "hp": 2, "cost": 150, "color": CYAN,
     "size": (int(MIN_DIM*0.079), int(MIN_DIM*0.099)), "desc": "sh_fighter", "detail": "d_fighter", "lore": "l_fighter"},
    {"name_key": "n_destroyer", "hp": 3, "cost": 400, "color": ORANGE,
     "size": (int(MIN_DIM*0.0875), int(MIN_DIM*0.105)), "desc": "sh_destroyer", "detail": "d_destroyer", "lore": "l_destroyer"},
    {"name_key": "n_mothership", "hp": 5, "cost": 1000, "color": PURPLE,
     "size": (int(MIN_DIM*0.105), int(MIN_DIM*0.1225)), "desc": "sh_mother", "detail": "d_mother", "lore": "l_mothership"}
]

UPGRADES = [
    {"name_key": "n_bomb",   "base_cost": 100, "desc_key": "bomb", "detail": "d_bomb", "lore": "l_bomb"},
    {"name_key": "n_damage", "base_cost": 150, "desc_key": "dmg_upg", "detail": "d_damage", "lore": "l_damage"},
    {"name_key": "n_speed",  "base_cost": 200, "desc_key": "spd_upg", "detail": "d_speed", "lore": "l_speed"}
]
MAX_UPGRADE_LVL = 5

ACHIEVEMENTS_LIST = [
    {"id": "a1", "cond": lambda: stats["kills"] >= 1, "claimed": False},
    {"id": "a2", "cond": lambda: stats["kills"] >= 100, "claimed": False},
    {"id": "a3", "cond": lambda: stats["kills"] >= 1000, "claimed": False},
    {"id": "a4", "cond": lambda: stats["bosses"] >= 1, "claimed": False},
    {"id": "a5", "cond": lambda: stats["bosses"] >= 5, "claimed": False},
    {"id": "a6", "cond": lambda: stats["coins_earned"] >= 1000, "claimed": False}
]

if sys.platform == "emscripten":
    SAVE_FILE = "/data/shooter_save.txt"
else:
    SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shooter_save.txt")

coins = 0
unlocked_ships = [0]
equipped_ship = 0
upgrade_levels = [0, 0, 0]
stats = {"kills": 0, "bosses": 0, "waves": 0, "coins_earned": 0}

stars = []
for _ in range(60):
    stars.append([random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)])

def load_data():
    global coins, unlocked_ships, equipped_ship, upgrade_levels, lang, gfx_high, stats
    coins = 0
    unlocked_ships = [0]
    equipped_ship = 0
    upgrade_levels = [0, 0, 0]
    stats = {"kills": 0, "bosses": 0, "waves": 0, "coins_earned": 0}
    
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                lines = f.read().splitlines()
                if len(lines) > 0: coins = int(lines[0])
                if len(lines) > 1: unlocked_ships = [int(x) for x in lines[1].split(",")]
                if len(lines) > 2: equipped_ship = int(lines[2])
                if len(lines) > 3: upgrade_levels = [int(x) for x in lines[3].split(",")]
                if len(lines) > 4: lang = lines[4]
                if len(lines) > 5: gfx_high = lines[5] == "1"
                if len(lines) > 7:
                    s = [int(x) for x in lines[7].split(",")]
                    if len(s) >= 4:
                        stats = {"kills": s[0], "bosses": s[1], "waves": s[2], "coins_earned": s[3]}
                if len(lines) > 8:
                    a = lines[8].split(",")
                    for i in range(min(len(a), len(ACHIEVEMENTS_LIST))):
                        ACHIEVEMENTS_LIST[i]["claimed"] = a[i] == "1"
        except Exception as e:
            print(f"Load error: {e}")

def save_data():
    try:
        with open(SAVE_FILE, "w") as f:
            f.write(f"{coins}\n{','.join(map(str, unlocked_ships))}\n{equipped_ship}\n{','.join(map(str, upgrade_levels))}\n")
            f.write(f"{lang}\n{1 if gfx_high else 0}\n")
            f.write(f"{stats['kills']},{stats['bosses']},{stats['waves']},{stats['coins_earned']}\n")
            f.write(f"{','.join(['1' if a['claimed'] else '0' for a in ACHIEVEMENTS_LIST])}\n")
    except Exception as e:
        print(f"Save error: {e}")

load_data()

BASE_ENEMY_HP = 2
HP_INCREASE_PER_WAVE = 2
BASE_SPAWN_DELAY = 1200

state = "MENU"
prev_state = "MENU"
shop_tab = "SHIPS"
settings_prev_state = "MENU"

pending_purchase = None

ZONE_Y = HEIGHT * 0.7
player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 150, 40, 50)
bullets, enemies, powerups, enemy_bullets, particles = [], [], [], [], []
boss = None
boss_max_hp = 0
score = wave = current_kills = 0
bombs = 3
last_shot_time, last_enemy_spawn = 0, 0
pause_time = 0

player_hp = 1
player_max_hp = 1
invulnerable_timer = 0
shield_timer = 0
regen_timer = 0
run_coins = 0

current_weapon = 0
weapon_level = 1
laser_start_time = 0
laser_damage_timer = 0
achievement_popup = ""
popup_timer = 0

btn_w = int(WIDTH * 0.7)
btn_x = (WIDTH - btn_w) // 2
btn_h = int(HEIGHT * 0.08)

menu_start_y = int(HEIGHT * 0.28)
menu_gap = 12
btn_play     = pygame.Rect(btn_x, menu_start_y + (btn_h + menu_gap) * 0, btn_w, btn_h)
btn_shop     = pygame.Rect(btn_x, menu_start_y + (btn_h + menu_gap) * 1, btn_w, btn_h)
btn_achieve  = pygame.Rect(btn_x, menu_start_y + (btn_h + menu_gap) * 2, btn_w, btn_h)
btn_settings = pygame.Rect(btn_x, menu_start_y + (btn_h + menu_gap) * 3, btn_w, btn_h)
btn_exit     = pygame.Rect(btn_x, menu_start_y + (btn_h + menu_gap) * 4, btn_w, btn_h)

btn_lang = pygame.Rect(btn_x, int(HEIGHT*0.35), btn_w, btn_h)
btn_gfx  = pygame.Rect(btn_x, int(HEIGHT*0.35) + btn_h + 30, btn_w, btn_h)
btn_settings_back = pygame.Rect(btn_x, int(HEIGHT*0.8), btn_w, btn_h)

btn_resume         = pygame.Rect(btn_x, int(HEIGHT*0.35), btn_w, btn_h)
btn_shop_pause     = pygame.Rect(btn_x, int(HEIGHT*0.35) + btn_h + 30, btn_w, btn_h)
btn_settings_pause = pygame.Rect(btn_x, int(HEIGHT*0.35) + (btn_h + 30)*2, btn_w, btn_h)
btn_exit_pause     = pygame.Rect(btn_x, int(HEIGHT*0.35) + (btn_h + 30)*3, btn_w, btn_h)

btn_menu_gameover = pygame.Rect(btn_x, int(HEIGHT*0.6), btn_w, btn_h)
btn_achieve_back  = pygame.Rect(btn_x, HEIGHT - btn_h - 50, btn_w, btn_h)

tab_w = (WIDTH - 60) // 2
btn_tab_ships    = pygame.Rect(30, int(HEIGHT*0.2), tab_w, int(btn_h*0.8))
btn_tab_upgrades = pygame.Rect(30 + tab_w + 10, int(HEIGHT*0.2), tab_w, int(btn_h*0.8))
shop_btns = [pygame.Rect(30, int(HEIGHT*0.35) + i*(btn_h+20), WIDTH - 60, btn_h) for i in range(4)]
btn_shop_back = pygame.Rect(btn_x, HEIGHT - btn_h - 50, btn_w, btn_h)

btn_pause = pygame.Rect(WIDTH - 80, 20, 60, 60)
bomb_radius = int(MIN_DIM * 0.11)
bomb_center = (WIDTH - bomb_radius - 30, HEIGHT - bomb_radius - 30)

popup_w = int(WIDTH * 0.85)
popup_h = int(HEIGHT * 0.45)
popup_rect = pygame.Rect((WIDTH - popup_w)//2, (HEIGHT - popup_h)//2, popup_w, popup_h)
popup_btn_w = int(popup_w * 0.4)
popup_btn_h = int(btn_h * 0.8)
popup_btn_y = popup_rect.bottom - popup_btn_h - 20
btn_popup_cancel = pygame.Rect(popup_rect.centerx - popup_btn_w - 10, popup_btn_y, popup_btn_w, popup_btn_h)
btn_popup_buy    = pygame.Rect(popup_rect.centerx + 10, popup_btn_y, popup_btn_w, popup_btn_h)

def reset_game():
    global score, wave, current_kills, shoot_delay, bullet_damage, weapon_level, enemy_spawn_delay, boss, boss_max_hp, bombs
    global bullets, enemies, powerups, enemy_bullets, particles, player, player_hp, player_max_hp, invulnerable_timer, run_coins
    global current_weapon, laser_start_time, laser_damage_timer, pause_time, shield_timer, regen_timer
    global last_shot_time, last_enemy_spawn
    score = 0; wave = 1; current_kills = 0; run_coins = 0
    bullets.clear(); enemies.clear(); powerups.clear(); enemy_bullets.clear(); particles.clear()
    boss = None; boss_max_hp = 0
    shield_timer = 0; regen_timer = 0

    ship = SHIPS[equipped_ship]
    player.width, player.height = ship["size"]
    player_hp = ship["hp"]; player_max_hp = ship["hp"]
    bombs = 3 + upgrade_levels[0]
    if equipped_ship == 2: bombs += 1

    bullet_damage = 1 + upgrade_levels[1]
    if equipped_ship == 1: bullet_damage += 1

    shoot_delay = max(100, 800 - (upgrade_levels[2] * 100))
    if equipped_ship == 0: shoot_delay = max(80, shoot_delay - 150)

    current_weapon = 0; weapon_level = 1; laser_start_time = 0; laser_damage_timer = 0
    enemy_spawn_delay = BASE_SPAWN_DELAY
    invulnerable_timer = 0
    player.center = (WIDTH // 2, HEIGHT - 150)
    pause_time = 0
    
    # Сбрасываем таймеры, чтобы не было мгновенных выстрелов при старте
    last_shot_time = pygame.time.get_ticks()
    last_enemy_spawn = 0

def draw_text(text, font, color, x, y, align="center"):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if align == "center":   rect.center = (x, y)
    elif align == "topleft":  rect.topleft = (x, y)
    elif align == "topright": rect.topright = (x, y)
    elif align == "midtop":   rect.midtop = (x, y)
    screen.blit(surf, rect)

def create_particles(x, y, color):
    if not gfx_high: return
    for _ in range(6):
        particles.append([x, y, random.randint(-6, 6), random.randint(-6, 6), color, 255])

def play_sound(snd):
    try:
        if snd: snd.play()
    except: pass

def check_achievements():
    global coins, achievement_popup, popup_timer
    for a in ACHIEVEMENTS_LIST:
        if not a["claimed"] and a["cond"]():
            a["claimed"] = True
            coins += 50
            achievement_popup = t(a["id"])
            popup_timer = pygame.time.get_ticks()
            play_sound(snd_powerup)

def adjust_timers_after_pause(delta):
    global last_shot_time, last_enemy_spawn, laser_start_time, laser_damage_timer
    global invulnerable_timer, shield_timer, regen_timer, popup_timer
    last_shot_time += delta
    last_enemy_spawn += delta
    laser_start_time += delta
    laser_damage_timer += delta
    invulnerable_timer += delta
    if shield_timer > 0: shield_timer += delta
    if regen_timer > 0: regen_timer += delta
    if popup_timer > 0: popup_timer += delta
    for e in enemies:
        e[4] += delta
    if boss:
        boss["shoot_timer"] += delta
        boss["pattern_timer"] += delta
        boss["minion_timer"] += delta

async def main():
    global state, prev_state, shop_tab, settings_prev_state
    global pending_purchase
    global player, bullets, enemies, powerups, enemy_bullets, particles, boss, boss_max_hp
    global score, wave, current_kills, bombs, last_shot_time, last_enemy_spawn, pause_time
    global player_hp, player_max_hp, invulnerable_timer, shield_timer, regen_timer, run_coins
    global current_weapon, weapon_level, laser_start_time, laser_damage_timer
    global achievement_popup, popup_timer
    global coins, unlocked_ships, equipped_ship, upgrade_levels, lang, gfx_high

    is_dragging = False

    while True:
        current_time = pygame.time.get_ticks()
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data(); pygame.quit(); sys.exit()

            # Управление пальцем/мышью
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                is_dragging = False
            elif event.type == pygame.MOUSEMOTION and is_dragging:
                if state == "PLAY":
                    px = max(player.width//2, min(event.pos[0], WIDTH - player.width//2))
                    py = max(ZONE_Y + player.height//2, min(event.pos[1], HEIGHT - player.height//2))
                    player.center = (px, py)

            if event.type == pygame.MOUSEBUTTONDOWN:
                dist_to_bomb = math.hypot(event.pos[0] - bomb_center[0], event.pos[1] - bomb_center[1])

                if state == "MENU":
                    if btn_play.collidepoint(event.pos):
                        reset_game(); state = "PLAY"
                    elif btn_shop.collidepoint(event.pos):
                        prev_state = "MENU"; state = "SHOP"
                    elif btn_achieve.collidepoint(event.pos):
                        state = "ACHIEVE"
                    elif btn_settings.collidepoint(event.pos):
                        settings_prev_state = "MENU"
                        state = "SETTINGS"
                    elif btn_exit.collidepoint(event.pos):
                        save_data(); pygame.quit(); sys.exit()

                elif state == "ACHIEVE":
                    if btn_achieve_back.collidepoint(event.pos):
                        state = "MENU"

                elif state == "SETTINGS":
                    if btn_lang.collidepoint(event.pos):
                        lang = "EN" if lang == "RU" else "RU"
                    elif btn_gfx.collidepoint(event.pos):
                        gfx_high = not gfx_high
                    elif btn_settings_back.collidepoint(event.pos):
                        save_data(); state = settings_prev_state

                elif state == "PAUSE":
                    if btn_resume.collidepoint(event.pos):
                        current_time = pygame.time.get_ticks()
                        adjust_timers_after_pause(current_time - pause_time)
                        state = "PLAY"
                    elif btn_shop_pause.collidepoint(event.pos):
                        prev_state = "PAUSE"; state = "SHOP"
                    elif btn_settings_pause.collidepoint(event.pos):
                        settings_prev_state = "PAUSE"
                        state = "SETTINGS"
                    elif btn_exit_pause.collidepoint(event.pos):
                        coins += run_coins
                        check_achievements()
                        save_data()
                        state = "MENU"

                elif state == "SHOP":
                    if pending_purchase:
                        if btn_popup_cancel.collidepoint(event.pos):
                            pending_purchase = None
                        elif btn_popup_buy.collidepoint(event.pos):
                            cost = pending_purchase["cost"]
                            if coins >= cost:
                                coins -= cost
                                play_sound(snd_coin)
                                if pending_purchase["type"] == "ship":
                                    idx = pending_purchase["index"]
                                    unlocked_ships.append(idx)
                                    equipped_ship = idx
                                elif pending_purchase["type"] == "upg":
                                    idx = pending_purchase["index"]
                                    upgrade_levels[idx] += 1
                                save_data()
                                pending_purchase = None
                            else:
                                play_sound(snd_hit)
                    else:
                        if btn_shop_back.collidepoint(event.pos):
                            save_data(); state = prev_state
                        elif btn_tab_ships.collidepoint(event.pos):
                            shop_tab = "SHIPS"
                        elif btn_tab_upgrades.collidepoint(event.pos):
                            shop_tab = "UPGRADES"
                        else:
                            for i, btn in enumerate(shop_btns):
                                if btn.collidepoint(event.pos):
                                    if shop_tab == "SHIPS" and i < len(SHIPS):
                                        if i in unlocked_ships:
                                            equipped_ship = i
                                            save_data()
                                        else:
                                            pending_purchase = {"type": "ship", "index": i, "cost": SHIPS[i]["cost"]}
                                    elif shop_tab == "UPGRADES" and i < len(UPGRADES):
                                        current_lvl = upgrade_levels[i]
                                        if current_lvl < MAX_UPGRADE_LVL:
                                            cost = UPGRADES[i]["base_cost"] * (current_lvl + 1)
                                            pending_purchase = {"type": "upg", "index": i, "cost": cost}

                elif state == "GAMEOVER":
                    if btn_menu_gameover.collidepoint(event.pos):
                        state = "MENU"

                elif state == "PLAY":
                    if btn_pause.collidepoint(event.pos):
                        state = "PAUSE"
                        pause_time = pygame.time.get_ticks()
                    elif dist_to_bomb < bomb_radius and bombs > 0:
                        bombs -= 1
                        play_sound(snd_explode)
                        for e in enemies:
                            create_particles(e[0].centerx, e[0].centery, e[3])
                            if random.randint(1, 100) <= 50:
                                powerups.append([pygame.Rect(e[0].centerx - 10, e[0].centery, 20, 20), "coin", 1])
                        enemies.clear(); enemy_bullets.clear()
                        if boss: boss["hp"] -= 50

        screen.fill(BLACK)

        star_limit = 60 if gfx_high else 20
        for idx, s in enumerate(stars):
            if idx >= star_limit: break
            s[1] += s[2]
            if s[1] > HEIGHT:
                s[1] = 0
                s[0] = random.randint(0, WIDTH)
            pygame.draw.circle(screen, GRAY, (s[0], s[1]), s[2])

        if state == "MENU":
            draw_text("SPACE SHOOTER", title_font, YELLOW, WIDTH//2, int(HEIGHT*0.15))
            draw_text(f"{t('coins')}: {coins}", font, GOLD, WIDTH//2, int(HEIGHT*0.22))
            for btn, txt_key in [
                (btn_play,     "play"),
                (btn_shop,     "shop"),
                (btn_achieve,  "achieve"),
                (btn_settings, "settings"),
                (btn_exit,     "exit"),
            ]:
                color = ACTIVE_COLOR if btn.collidepoint((mx, my)) else BUTTON_COLOR
                pygame.draw.rect(screen, color, btn, border_radius=15)
                draw_text(t(txt_key), font, WHITE, btn.centerx, btn.centery)

        elif state == "ACHIEVE":
            draw_text(t("ach_title"), title_font, YELLOW, WIDTH//2, int(HEIGHT*0.1))
            start_y = int(HEIGHT*0.2)
            for i, a in enumerate(ACHIEVEMENTS_LIST):
                rect = pygame.Rect(30, start_y + i*(btn_h+10), WIDTH-60, btn_h)
                pygame.draw.rect(screen, BUTTON_COLOR if not a["claimed"] else ACTIVE_COLOR, rect, border_radius=10)
                draw_text(t(a["id"]), small_font, WHITE if not a["claimed"] else BLACK, rect.x+20, rect.centery, align="topleft")
                if not a["claimed"]:
                    draw_text(t("reward"), small_font, GOLD, rect.right-20, rect.centery, align="topright")

            pygame.draw.rect(screen, BUTTON_HOVER if btn_achieve_back.collidepoint((mx, my)) else BUTTON_COLOR, btn_achieve_back, border_radius=15)
            draw_text(t("back"), font, WHITE, btn_achieve_back.centerx, btn_achieve_back.centery)

        elif state == "SETTINGS":
            draw_text(t("settings"), title_font, YELLOW, WIDTH//2, int(HEIGHT*0.2))
            pygame.draw.rect(screen, BUTTON_COLOR, btn_lang, border_radius=15)
            draw_text(f"{t('lang_lbl')} {'РУССКИЙ' if lang == 'RU' else 'ENGLISH'}", font, WHITE, btn_lang.centerx, btn_lang.centery)
            pygame.draw.rect(screen, BUTTON_COLOR, btn_gfx, border_radius=15)
            draw_text(f"{t('gfx_lbl')} {t('high') if gfx_high else t('low')}", font, WHITE, btn_gfx.centerx, btn_gfx.centery)

            pygame.draw.rect(screen, BUTTON_HOVER if btn_settings_back.collidepoint((mx, my)) else BUTTON_COLOR, btn_settings_back, border_radius=15)
            draw_text(t("back"), font, WHITE, btn_settings_back.centerx, btn_settings_back.centery)

        elif state == "SHOP":
            draw_text(t("shop"), title_font, YELLOW, WIDTH//2, int(HEIGHT*0.1))
            draw_text(f"{t('coins')}: {coins}", font, GOLD, WIDTH//2, int(HEIGHT*0.16))
            pygame.draw.rect(screen, ACTIVE_COLOR if shop_tab == "SHIPS" else BUTTON_COLOR, btn_tab_ships, border_radius=10)
            draw_text(t("ships"), small_font, WHITE, btn_tab_ships.centerx, btn_tab_ships.centery)
            pygame.draw.rect(screen, ACTIVE_COLOR if shop_tab == "UPGRADES" else BUTTON_COLOR, btn_tab_upgrades, border_radius=10)
            draw_text(t("upgrades"), small_font, WHITE, btn_tab_upgrades.centerx, btn_tab_upgrades.centery)

            if shop_tab == "SHIPS":
                for i, btn in enumerate(shop_btns):
                    if i >= len(SHIPS): break
                    ship = SHIPS[i]; is_unlocked = i in unlocked_ships; is_equipped = i == equipped_ship
                    color = ACTIVE_COLOR if is_equipped else ((0, 100, 200) if is_unlocked else BUTTON_COLOR)
                    pygame.draw.rect(screen, color, btn, border_radius=15)
                    
                    preview_h = int(btn_h * 0.75)
                    preview_w = int(preview_h * 0.8)
                    pcx = btn.x + preview_h // 2 + 15
                    pcy = btn.centery
                    pts = [(pcx, pcy - preview_h//2),
                           (pcx + preview_w//2, pcy + preview_h//2),
                           (pcx, pcy + preview_h//2 - preview_h//5),
                           (pcx - preview_w//2, pcy + preview_h//2)]
                    pygame.draw.polygon(screen, ship["color"], pts)
                    pygame.draw.polygon(screen, WHITE, pts, 2)
                    
                    text_x = btn.x + preview_h + 30
                    title_y = btn.y + 15
                    desc_y = title_y + font.get_height() + 5
                    
                    draw_text(f"{t(ship['name_key'])} (HP: {ship['hp']})", font, ship["color"], text_x, title_y, align="topleft")
                    draw_text(t(ship["desc"]), small_font, LIGHT_GRAY, text_x, desc_y, align="topleft")
                    
                    if is_equipped:
                        draw_text(t("equipped"), small_font, WHITE, btn.right - 20, btn.centery, align="topright")
                    elif is_unlocked:
                        draw_text(t("equip"), small_font, WHITE, btn.right - 20, btn.centery, align="topright")
                    else:
                        draw_text(f"{t('buy')}: {ship['cost']}", small_font, GOLD if coins >= ship['cost'] else RED, btn.right - 20, btn.centery, align="topright")
            
            elif shop_tab == "UPGRADES":
                for i, btn in enumerate(shop_btns):
                    if i >= len(UPGRADES): break
                    upg = UPGRADES[i]; lvl = upgrade_levels[i]
                    pygame.draw.rect(screen, BUTTON_COLOR, btn, border_radius=15)
                    
                    text_x = btn.x + 20
                    title_y = btn.y + 15
                    desc_y = title_y + small_font.get_height() + 10
                    
                    draw_text(f"{t(upg['name_key'])} (Lvl {lvl}/{MAX_UPGRADE_LVL})", font, WHITE, text_x, title_y, align="topleft")
                    draw_text(t(upg['desc_key']), small_font, LIGHT_GRAY, text_x, desc_y, align="topleft")
                    
                    if lvl >= MAX_UPGRADE_LVL:
                        draw_text(t("max_lvl"), small_font, ACTIVE_COLOR, btn.right - 20, btn.centery, align="topright")
                    else:
                        cost = upg["base_cost"] * (lvl + 1)
                        draw_text(f"{t('buy')}: {cost}", small_font, GOLD if coins >= cost else RED, btn.right - 20, btn.centery, align="topright")
            
            pygame.draw.rect(screen, BUTTON_HOVER if btn_shop_back.collidepoint((mx, my)) else BUTTON_COLOR, btn_shop_back, border_radius=15)
            draw_text(t("back"), font, WHITE, btn_shop_back.centerx, btn_shop_back.centery)

            if pending_purchase:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 200))
                screen.blit(overlay, (0, 0))

                pygame.draw.rect(screen, (40, 40, 40), popup_rect, border_radius=20)
                pygame.draw.rect(screen, ACTIVE_COLOR, popup_rect, 4, border_radius=20)

                if pending_purchase["type"] == "ship":
                    item = SHIPS[pending_purchase["index"]]
                    item_name = t(item["name_key"])
                    item_detail = t(item["detail"])
                    item_lore = t(item["lore"])
                else:
                    item = UPGRADES[pending_purchase["index"]]
                    item_name = t(item["name_key"])
                    item_detail = t(item["detail"])
                    item_lore = t(item["lore"])

                draw_text(item_name, title_font, YELLOW, popup_rect.centerx, popup_rect.y + 50)
                
                desc_header = small_font.render(t("desc_lbl"), True, LIGHT_GRAY)
                screen.blit(desc_header, (popup_rect.x + 40, popup_rect.y + 100))

                lines = wrap_text(item_detail, small_font, popup_w - 80)
                for i, line in enumerate(lines):
                    draw_text(line, small_font, WHITE, popup_rect.x + 40, popup_rect.y + 130 + i * small_font.get_linesize(), align="topleft")

                lore_y = popup_rect.y + 130 + len(lines) * small_font.get_linesize() + 30
                lore_header = small_font.render(t("lore_lbl"), True, LIGHT_GRAY)
                screen.blit(lore_header, (popup_rect.x + 40, lore_y))
                
                lore_lines = wrap_text(item_lore, small_font, popup_w - 80)
                for i, line in enumerate(lore_lines):
                    draw_text(line, small_font, LORE_COLOR, popup_rect.x + 40, lore_y + 30 + i * small_font.get_linesize(), align="topleft")

                price_color = GOLD if coins >= pending_purchase['cost'] else RED
                draw_text(f"{t('cost_lbl')}{pending_purchase['cost']}", font, price_color, popup_rect.centerx, popup_rect.bottom - 110)

                color_cancel = BUTTON_HOVER if btn_popup_cancel.collidepoint((mx, my)) else BUTTON_COLOR
                pygame.draw.rect(screen, color_cancel, btn_popup_cancel, border_radius=10)
                draw_text(t("cancel"), font, WHITE, btn_popup_cancel.centerx, btn_popup_cancel.centery)

                can_afford = coins >= pending_purchase['cost']
                if can_afford:
                    color_buy = ACTIVE_COLOR if btn_popup_buy.collidepoint((mx, my)) else BUTTON_COLOR
                    text_color = WHITE
                else:
                    color_buy = BUTTON_DISABLED
                    text_color = GRAY

                pygame.draw.rect(screen, color_buy, btn_popup_buy, border_radius=10)
                draw_text(t("buy"), font, text_color, btn_popup_buy.centerx, btn_popup_buy.centery)

        elif state == "PLAY" or state == "PAUSE":
            ship = SHIPS[equipped_ship]

            if state == "PLAY":
                check_achievements()

                if equipped_ship == 3 and player_hp < player_max_hp:
                    if current_time - regen_timer > 5000:
                        player_hp += 1
                        regen_timer = current_time
                        create_particles(player.centerx, player.centery, GREEN)

                if current_weapon == 0:
                    if current_time - last_shot_time > shoot_delay:
                        if weapon_level == 1:
                            bullets.append([pygame.Rect(player.centerx - 3, player.top, 6, 15), 0, -18, 0])
                        elif weapon_level == 2:
                            bullets.append([pygame.Rect(player.centerx - 12, player.top, 6, 15), 0, -18, 0])
                            bullets.append([pygame.Rect(player.centerx + 6, player.top, 6, 15), 0, -18, 0])
                        elif weapon_level >= 3:
                            bullets.append([pygame.Rect(player.centerx - 3, player.top, 6, 15), 0, -18, 0])
                            bullets.append([pygame.Rect(player.centerx - 15, player.top, 6, 15), -4, -18, 0])
                            bullets.append([pygame.Rect(player.centerx + 9, player.top, 6, 15), 4, -18, 0])
                            if weapon_level >= 4:
                                bullets.append([pygame.Rect(player.centerx - 25, player.top, 6, 15), -7, -18, 0])
                                bullets.append([pygame.Rect(player.centerx + 19, player.top, 6, 15), 7, -18, 0])
                        last_shot_time = current_time
                        play_sound(snd_shoot)

                elif current_weapon == 1:
                    cycle_time = current_time - laser_start_time
                    if cycle_time > 5000:
                        laser_start_time = current_time; cycle_time = 0
                    if cycle_time < 3000:
                        if current_time - laser_damage_timer > 100:
                            play_sound(snd_laser)
                            laser_rect = pygame.Rect(player.centerx - 15, 0, 30, player.top)
                            for enemy_data in enemies[:]:
                                if laser_rect.colliderect(enemy_data[0]):
                                    enemy_data[1] -= (bullet_damage // 2) + 1
                                    create_particles(enemy_data[0].centerx, enemy_data[0].centery, YELLOW)
                                    if enemy_data[1] <= 0:
                                        enemies.remove(enemy_data)
                                        score += 10; current_kills += 1; stats["kills"] += 1
                                        play_sound(snd_explode)
                                        if random.randint(1, 100) <= 50:
                                            powerups.append([pygame.Rect(enemy_data[0].centerx - 10, enemy_data[0].centery, 20, 20), "coin", 1])
                                        if current_kills >= 10:
                                            wave += 1; current_kills = 0; stats["waves"] += 1
                                            enemy_spawn_delay = max(300, enemy_spawn_delay - 80)
                            if boss and laser_rect.colliderect(boss["rect"]):
                                boss["hp"] -= (bullet_damage // 2) + 1
                                create_particles(player.centerx, 100, RED)
                                if boss["hp"] <= 0:
                                    score += 500; stats["bosses"] += 1; play_sound(snd_explode)
                                    for _ in range(5):
                                        powerups.append([pygame.Rect(boss["rect"].centerx - 20 + random.randint(-40, 40),
                                                                     boss["rect"].centery + random.randint(-40, 40), 20, 20), "coin", 5])
                                    boss = None; wave += 1; current_kills = 0
                            laser_damage_timer = current_time

                elif current_weapon == 2:
                    if current_time - last_shot_time > 600:
                        play_sound(snd_shoot)
                        for angle in [-40, -20, 0, 20, 40]:
                            rad = math.radians(angle - 90)
                            bullets.append([pygame.Rect(player.centerx - 4, player.top, 8, 8),
                                            math.cos(rad)*15, math.sin(rad)*15, 1])
                        last_shot_time = current_time

                elif current_weapon == 3:
                    if current_time - last_shot_time > 700:
                        play_sound(snd_shoot)
                        bullets.append([pygame.Rect(player.centerx - 15, player.top, 8, 20), 0, -10, 2])
                        bullets.append([pygame.Rect(player.centerx + 7, player.top, 8, 20), 0, -10, 2])
                        last_shot_time = current_time

                is_boss_wave = (wave % 10 == 0)
                if is_boss_wave:
                    if boss is None:
                        boss_max_hp = int(200 * (wave // 10))
                        boss = {"rect": pygame.Rect(WIDTH // 2 - 75, -100, 150, 100),
                                "hp": boss_max_hp, "speed_y": 2, "speed_x": 3,
                                "shoot_timer": current_time, "pattern_timer": current_time,
                                "minion_timer": current_time}
                else:
                    if current_time - last_enemy_spawn > enemy_spawn_delay:
                        enemy_x = random.randint(0, WIDTH - 50)
                        enemy_rect = pygame.Rect(enemy_x, 0, 45, 45)
                        enemy_health = BASE_ENEMY_HP + (wave - 1) * HP_INCREASE_PER_WAVE
                        enemy_type = 0
                        if wave >= 3 and random.randint(1, 100) <= 30: enemy_type = 1
                        if wave >= 5 and random.randint(1, 100) <= 20: enemy_type = 2
                        if wave >= 11 and random.randint(1, 100) <= 25: enemy_type = 3
                        color = RED
                        if enemy_type == 1: color = PURPLE
                        elif enemy_type == 2: color = GREEN
                        elif enemy_type == 3: color = ORANGE
                        enemies.append([enemy_rect, enemy_health, enemy_type, color, current_time])
                        last_enemy_spawn = current_time

                for bullet in bullets[:]:
                    if bullet[3] == 2 and enemies:
                        target = min(enemies, key=lambda e: math.hypot(e[0].centerx - bullet[0].centerx, e[0].centery - bullet[0].centery))
                        dx = target[0].centerx - bullet[0].centerx
                        dy = target[0].centery - bullet[0].centery
                        dist = math.hypot(dx, dy)
                        if dist > 0:
                            bullet[1] += (dx / dist) * 0.6
                            bullet[2] += (dy / dist) * 0.6
                    bullet[0].x += bullet[1]; bullet[0].y += bullet[2]
                    if bullet[0].y < -20 or bullet[0].x < -20 or bullet[0].x > WIDTH + 20:
                        bullets.remove(bullet)
                    elif bullet[3] == 1 and bullet[0].y < HEIGHT // 2:
                        bullets.remove(bullet)

                enemy_speed = 3 + (wave * 0.5)
                for enemy_data in enemies[:]:
                    rect, e_type = enemy_data[0], enemy_data[2]
                    if e_type == 1:
                        rect.y += enemy_speed
                        rect.x += math.sin(current_time * 0.005) * 5
                        rect.x = max(0, min(rect.x, WIDTH - 45))
                    elif e_type == 2:
                        if rect.y > HEIGHT * 0.3:
                            rect.y -= enemy_speed
                            if current_time - enemy_data[4] > 2000:
                                enemy_bullets.append([pygame.Rect(rect.centerx - 4, rect.bottom, 8, 16), 0, 7])
                                enemy_data[4] = current_time
                        else:
                            rect.y += enemy_speed
                    elif e_type == 3:
                        dx = player.centerx - rect.centerx
                        dy = player.centery - rect.centery
                        dist = math.hypot(dx, dy)
                        if dist > 0:
                            rect.x += (dx / dist) * (enemy_speed + 2)
                            rect.y += (dy / dist) * (enemy_speed + 2)
                    else:
                        rect.y += enemy_speed
                    if rect.y > HEIGHT: enemies.remove(enemy_data)

                for eb in enemy_bullets[:]:
                    eb[0].x += eb[1]; eb[0].y += eb[2]
                    if eb[0].y > HEIGHT or eb[0].x < 0 or eb[0].x > WIDTH:
                        enemy_bullets.remove(eb)

                if boss:
                    if boss["rect"].y < 50:
                        boss["rect"].y += boss["speed_y"]
                    else:
                        speed_mult = 2 if boss["hp"] < boss_max_hp * 0.5 else 1
                        boss["rect"].x += boss["speed_x"] * speed_mult
                        if boss["rect"].left < 0 or boss["rect"].right > WIDTH:
                            boss["speed_x"] *= -1

                        if current_time - boss["shoot_timer"] > (1000 / speed_mult):
                            enemy_bullets.append([pygame.Rect(boss["rect"].centerx - 10, boss["rect"].bottom, 20, 30), 0, 8 * speed_mult])
                            boss["shoot_timer"] = current_time

                        if wave >= 20 and current_time - boss["pattern_timer"] > (2500 / speed_mult):
                            play_sound(snd_laser)
                            for angle in range(0, 360, 30):
                                rad = math.radians(angle)
                                enemy_bullets.append([pygame.Rect(boss["rect"].centerx, boss["rect"].centery, 12, 12),
                                                      math.cos(rad) * 5, math.sin(rad) * 5])
                            boss["pattern_timer"] = current_time

                        if current_time - boss["minion_timer"] > (4000 / speed_mult):
                            for _ in range(2):
                                m_x = boss["rect"].centerx + random.randint(-50, 50)
                                enemies.append([pygame.Rect(m_x, boss["rect"].bottom, 30, 30), 2, 0, RED, current_time])
                            boss["minion_timer"] = current_time

                for p_data in powerups[:]:
                    p_data[0].y += 4
                    if p_data[0].y > HEIGHT: powerups.remove(p_data)
                    if p_data[0].colliderect(player):
                        if p_data[1] == "coin":
                            run_coins += p_data[2]; stats["coins_earned"] += p_data[2]; play_sound(snd_coin)
                        elif p_data[1] == "weapon":
                            if current_weapon == 0:
                                weapon_level = min(5, weapon_level + 1); play_sound(snd_powerup)
                        elif p_data[1] == "weapon_type":
                            current_weapon = (current_weapon + 1) % 4
                            laser_start_time = current_time
                            play_sound(snd_powerup)
                        elif p_data[1] == "shield":
                            shield_timer = current_time + 5000
                            play_sound(snd_powerup)
                        powerups.remove(p_data)

                for p in particles[:]:
                    p[0] += p[2]; p[1] += p[3]; p[5] -= 15
                    if p[5] <= 0: particles.remove(p)

                for bullet in bullets[:]:
                    hit_something = False
                    for enemy_data in enemies[:]:
                        if bullet[0].colliderect(enemy_data[0]):
                            bullets.remove(bullet)
                            hit_something = True
                            enemy_data[1] -= bullet_damage
                            if enemy_data[1] <= 0:
                                create_particles(enemy_data[0].centerx, enemy_data[0].centery, enemy_data[3])
                                enemies.remove(enemy_data)
                                score += 10; current_kills += 1; stats["kills"] += 1
                                play_sound(snd_explode)

                                if random.randint(1, 100) <= 50:
                                    powerups.append([pygame.Rect(enemy_data[0].centerx - 10, enemy_data[0].centery, 20, 20), "coin", 1])

                                if current_kills >= 10:
                                    wave += 1; current_kills = 0; stats["waves"] += 1
                                    enemy_spawn_delay = max(300, enemy_spawn_delay - 80)

                                drop_roll = random.randint(1, 100)
                                if drop_roll <= 5:
                                    powerups.append([pygame.Rect(enemy_data[0].centerx - 15, enemy_data[0].centery, 25, 25), "shield"])
                                elif drop_roll <= 25:
                                    powerups.append([pygame.Rect(enemy_data[0].centerx - 15, enemy_data[0].centery, 25, 25), "weapon"])
                                elif drop_roll <= 40:
                                    powerups.append([pygame.Rect(enemy_data[0].centerx - 15, enemy_data[0].centery, 25, 25), "weapon_type"])
                            break

                    if not hit_something and boss and bullet[0].colliderect(boss["rect"]):
                        bullets.remove(bullet)
                        boss["hp"] -= bullet_damage
                        create_particles(bullet[0].centerx, bullet[0].y, DARK_RED)
                        if boss["hp"] <= 0:
                            for _ in range(15):
                                create_particles(boss["rect"].centerx, boss["rect"].centery, DARK_RED)
                            score += 500; stats["bosses"] += 1; play_sound(snd_explode)
                            for _ in range(5):
                                powerups.append([pygame.Rect(boss["rect"].centerx - 20 + random.randint(-40, 40),
                                                             boss["rect"].centery + random.randint(-40, 40), 20, 20), "coin", 5])
                            for _ in range(3):
                                powerups.append([pygame.Rect(boss["rect"].centerx - 15, boss["rect"].centery, 25, 25),
                                                 random.choice(["weapon", "weapon_type"])])
                            boss = None; wave += 1; current_kills = 0

                if current_time > invulnerable_timer and current_time > shield_timer:
                    hit = (any(e[0].colliderect(player) for e in enemies) or
                           any(eb[0].colliderect(player) for eb in enemy_bullets) or
                           (boss and boss["rect"].colliderect(player)))
                    if hit:
                        player_hp -= 1
                        play_sound(snd_hit)
                        invulnerable_timer = current_time + 1500
                        create_particles(player.centerx, player.centery, ship["color"])
                        for e in enemies[:]:
                            if e[0].colliderect(player): enemies.remove(e)
                        if player_hp <= 0:
                            coins += run_coins
                            check_achievements()
                            save_data()
                            state = "GAMEOVER"
                            continue

            pygame.draw.line(screen, GRAY, (0, ZONE_Y), (WIDTH, ZONE_Y), 2)

            for bullet in bullets:
                if bullet[3] == 1:
                    pygame.draw.circle(screen, ORANGE, (bullet[0].centerx, bullet[0].centery), 5)
                elif bullet[3] == 2:
                    pygame.draw.polygon(screen, RAINBOW, [(bullet[0].centerx, bullet[0].top),
                                                         (bullet[0].left, bullet[0].bottom),
                                                         (bullet[0].right, bullet[0].bottom)])
                else:
                    pygame.draw.rect(screen, YELLOW, bullet[0], border_radius=3)

            if current_weapon == 1:
                cycle_time = current_time - laser_start_time
                if cycle_time < 3000:
                    beam_width = 25 if cycle_time % 150 < 75 else 15
                    pygame.draw.rect(screen, RED, (player.centerx - beam_width//2, 0, beam_width, player.top))
                    pygame.draw.rect(screen, WHITE, (player.centerx - beam_width//4, 0, beam_width//2, player.top))
                elif cycle_time < 5000:
                    pygame.draw.rect(screen, GRAY, (player.centerx - 2, 0, 4, player.top))

            for eb in enemy_bullets:
                pygame.draw.circle(screen, CYAN, (eb[0].centerx, eb[0].centery), 6)

            for enemy_data in enemies:
                r = enemy_data[0]
                pygame.draw.polygon(screen, enemy_data[3], [(r.centerx, r.top), (r.right, r.centery),
                                                            (r.centerx, r.bottom), (r.left, r.centery)])

            if boss:
                r = boss["rect"]
                pts = [(r.centerx, r.top), (r.right, r.top + r.height//3),
                       (r.right, r.bottom - r.height//3), (r.centerx, r.bottom),
                       (r.left, r.bottom - r.height//3), (r.left, r.top + r.height//3)]
                current_boss_color = (255, 0, 0) if boss["hp"] < boss_max_hp * 0.5 else BOSS_COLOR
                pygame.draw.polygon(screen, current_boss_color, pts)
                pygame.draw.polygon(screen, DARK_RED, pts, 3)

                hp_percent = max(0, boss["hp"] / boss_max_hp)
                pygame.draw.rect(screen, RED, (50, HEIGHT - 40, WIDTH - 100, 20))
                pygame.draw.rect(screen, GREEN, (50, HEIGHT - 40, (WIDTH - 100) * hp_percent, 20))

            for p_data in powerups:
                if p_data[1] == "coin":
                    pygame.draw.circle(screen, GOLD, (p_data[0].centerx, p_data[0].centery), 12)
                    pygame.draw.circle(screen, YELLOW, (p_data[0].centerx, p_data[0].centery), 8)
                    pygame.draw.circle(screen, WHITE, (p_data[0].centerx, p_data[0].centery), 3)
                elif p_data[1] == "shield":
                    pygame.draw.circle(screen, WHITE, (p_data[0].centerx, p_data[0].centery), 12, 3)
                    pygame.draw.circle(screen, CYAN, (p_data[0].centerx, p_data[0].centery), 8)
                elif p_data[1] == "weapon":
                    pygame.draw.rect(screen, GOLD, p_data[0], border_radius=8)
                elif p_data[1] == "weapon_type":
                    pygame.draw.rect(screen, RAINBOW, p_data[0], border_radius=8)

            for p in particles:
                p_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
                p_surf.fill((p[4][0], p[4][1], p[4][2], p[5]))
                screen.blit(p_surf, (p[0], p[1]))

            if current_time > invulnerable_timer or (current_time // 100) % 2 == 0:
                r = player
                pts = [(r.centerx, r.top), (r.right, r.bottom),
                       (r.centerx, r.bottom - 10), (r.left, r.bottom)]
                pygame.draw.polygon(screen, ship["color"], pts)
                pygame.draw.polygon(screen, WHITE, pts, 2)

            if current_time < shield_timer:
                pygame.draw.circle(screen, CYAN, (player.centerx, player.centery), player.width, 2)
                pygame.draw.circle(screen, WHITE, (player.centerx, player.centery), player.width + 2, 1)

            draw_text(f"{t('score')}: {score}", small_font, WHITE, 20, 20, align="topleft")
            draw_text(f"{t('coins')}: {run_coins}", small_font, GOLD, 20, 20 + small_font.get_height() + 5, align="topleft")
            draw_text(f"HP: {player_hp}/{player_max_hp}", small_font, RED, 20, 20 + (small_font.get_height() + 5)*2, align="topleft")
            draw_text(f"{t('wave')}: {wave}", font, YELLOW, WIDTH//2, 20, align="midtop")

            w_names = ["STANDARD", "LASER", "SHOTGUN", "MISSILES"]
            draw_text(f"WPN: {w_names[current_weapon]}", small_font, WHITE, WIDTH - 100, 90, align="topright")
            if current_weapon == 0:
                draw_text(f"LVL: {weapon_level}", small_font, GOLD, WIDTH - 100, 90 + small_font.get_height() + 5, align="topright")

            pygame.draw.rect(screen, BUTTON_COLOR, btn_pause, border_radius=10)
            pygame.draw.rect(screen, WHITE, (btn_pause.centerx - 12, btn_pause.centery - 15, 8, 30))
            pygame.draw.rect(screen, WHITE, (btn_pause.centerx + 4, btn_pause.centery - 15, 8, 30))

            if bombs > 0:
                pygame.draw.circle(screen, (220, 50, 50), bomb_center, bomb_radius)
                pygame.draw.circle(screen, (255, 150, 150), bomb_center, bomb_radius, 4)
            else:
                pygame.draw.circle(screen, (50, 50, 50), bomb_center, bomb_radius)
                pygame.draw.circle(screen, (100, 100, 100), bomb_center, bomb_radius, 4)
            draw_text(t("bomb"), small_font, WHITE, bomb_center[0], bomb_center[1] - 10)
            draw_text(f"x{bombs}", font, WHITE, bomb_center[0], bomb_center[1] + 15)

            if achievement_popup and current_time - popup_timer < 3000:
                popup_rect_ach = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 50, 400, 100)
                pygame.draw.rect(screen, ACTIVE_COLOR, popup_rect_ach, border_radius=20)
                draw_text("ACHIEVEMENT!", font, WHITE, WIDTH//2, HEIGHT//2 - 20)
                draw_text(achievement_popup, small_font, WHITE, WIDTH//2, HEIGHT//2 + 20)

            if state == "PAUSE":
                pause_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pause_surf.fill((0, 0, 0, 200))
                screen.blit(pause_surf, (0, 0))
                draw_text(t("pause"), title_font, YELLOW, WIDTH//2, int(HEIGHT*0.22))
                for btn, txt_key in [(btn_resume, "resume"),
                                      (btn_shop_pause, "shop"),
                                      (btn_settings_pause, "settings"),
                                      (btn_exit_pause, "menu")]:
                    color = ACTIVE_COLOR if btn.collidepoint((mx, my)) else BUTTON_COLOR
                    pygame.draw.rect(screen, color, btn, border_radius=15)
                    draw_text(t(txt_key), font, WHITE, btn.centerx, btn.centery)

        elif state == "GAMEOVER":
            draw_text(t("game_over"), title_font, RED, WIDTH//2, int(HEIGHT*0.25))
            draw_text(f"{t('score')}: {score}", font, WHITE, WIDTH//2, int(HEIGHT*0.35))
            draw_text(f"{t('wave')}: {wave}", font, YELLOW, WIDTH//2, int(HEIGHT*0.4))
            draw_text(f"{t('earned')} +{run_coins}", font, GOLD, WIDTH//2, int(HEIGHT*0.45))
            pygame.draw.rect(screen, BUTTON_HOVER if btn_menu_gameover.collidepoint((mx, my)) else BUTTON_COLOR, btn_menu_gameover, border_radius=15)
            draw_text(t("menu"), font, WHITE, btn_menu_gameover.centerx, btn_menu_gameover.centery)

        pygame.display.flip()
        await asyncio.sleep(1 / 60)

if __name__ == "__main__":
    asyncio.run(main())
