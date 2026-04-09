from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji  # <-- Импортируем библиотеку для эмодзи
import time

# ... (весь код парсинга ранга остаётся без изменений) ...
print("🚀 Запускаю парсер ранга...")

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    driver.get('https://minesweeper.online/ru/player/9606831')
    time.sleep(5)
    rank_element = driver.find_element(By.CLASS_NAME, "top-badge")
    rank_text = rank_element.text
    rank_number = rank_text.replace("TOP", "").strip()
    print(f"🎉 Твой ранг: {rank_number}")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    rank_number = "6307"
finally:
    driver.quit()

# --- 2. СОЗДАНИЕ БАННЕРА (ОБНОВЛЁННАЯ ЧАСТЬ) ---
print("🎨 Создаю баннер...")

WIDTH = 400
HEIGHT = 200
bg_color = (56, 46, 46)
image = Image.new('RGB', (WIDTH, HEIGHT), color=bg_color)
draw = ImageDraw.Draw(image)

# Загружаем обычный шрифт для текста
try:
    # Пытаемся загрузить стандартный шрифт
    font_medium = ImageFont.truetype("ALGER.TTF", 40)
    font_small = ImageFont.truetype("ALGER.TTF", 24)
    font_main = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)
    print("✅ Шрифт DejaVuSans загружен")
except:
    # Если не получилось, используем стандартный
    font_main = ImageFont.load_default()
    font_big = ImageFont.load_default()
    print("⚠️ Использую стандартный шрифт")

lighter_bg = (bg_color[0] + 30, bg_color[1] + 30, bg_color[2] + 30)
draw.rectangle([(5, 5), (WIDTH-5, HEIGHT-5)], outline=lighter_bg, width=3)

# === НОВЫЙ БЛОК ДЛЯ ТЕКСТА С ЭМОДЗИ ===
# Открываем специальный контекст Pilmoji для рисования текста с эмодзи
with Pilmoji(image) as pilmoji:
    # Рисуем текст, как обычно, но Pilmoji сам позаботится об эмодзи
    draw.text((WIDTH//2, 35), "Minesweeper", fill=(200, 200, 200), anchor="mt", font=font_small)
    draw.text((WIDTH//2 - 17, 65), "WORLD RANK", fill=(255, 255, 255), anchor="mt", font=font_small)
    # Вот здесь теперь появится настоящий цветной 🏆!
    pilmoji.text((WIDTH//2 + 67, 67), "🏆", fill=(255, 215, 0), anchor="mt", font=font_main)
    draw.text((WIDTH//2, 105), "Top", fill=(255, 255, 255), anchor="mt", font=font_small)

    total_players = "10728174"
    draw.text((WIDTH//2 - 80, 140), f"{rank_number}", fill=(0, 100, 255), anchor="mt", font=font_medium)
    draw.text((WIDTH//2 - 22, 140), " / ", fill=(255, 255, 255), anchor="mt", font=font_medium)
    draw.text((WIDTH//2 + 80, 140), f"{total_players}", fill=(255, 255, 255), anchor="mt", font=font_medium)

image.save("minesweeper_rank.png")
print(f"💾 Баннер сохранён как 'minesweeper_rank.png'")
print(f"📊 Ранг #{rank_number} отображён на баннере")
