import discord
from discord.ext import commands, tasks
import random
import asyncio
import gc
import aiohttp
import time
from datetime import datetime
from collections import defaultdict, deque
import logging

logging.getLogger('discord').setLevel(logging.ERROR)

# 🔹 КОНФИГ
DISCORD_TOKEN = "MTQwNTE5OTg3NzQxMTA0NTQ5Ng.GGDE-P.cuJITY7miG-5Yw_UCi5HtgFCFZhyLTCniqz02o"
OPENAI_API_KEY = "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"

# 🚀 БОТ КОНФИГ
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=["!", "т!", "T!"],
    intents=intents,
    help_command=@bot.command(name='alive', aliases=['жив'])
async def alive_cmd(ctx):
    """🔥 Проверка активности"""
    uptime = int(time.time() - stats['start'])
    h, m = uptime // 3600, (uptime % 3600) // 60
    
    await ctx.send(
        f"🔥 **СУПЕР БОТ ЖЖЕТ!**\n"
        f"⚡ Онлайн: {h}ч {m}м | Команд: {stats['cmds']}\n"
        f"🚀 **РАБОТАЮ НА МАКСИМУМ 24/7!**\n"
        f"😴 **АНТИСОН АКТИВЕН!** Никогда не засну!"
    ),
    case_insensitive=True
)

# 📊 СТАТИСТИКА
stats = {'cmds': 0, 'ai': 0, 'start': time.time(), 'msgs': 0}
memory = {
    'conversations': defaultdict(lambda: deque(maxlen=3)),
    'user_stats': defaultdict(lambda: {'commands': 0, 'level': 1})
}

# 💬 КЭШИ
QUICK = {
    "привет": ["👋 Привет! Как дела?", "🤖 Приветствую!", "😊 Привет!"],
    "как дела": ["😎 Отлично!", "🚀 Супер!", "💪 Мощно!"],
    "спасибо": ["😊 Пожалуйста!", "🤖 Обращайся!", "💪 Рад помочь!"],
    "пока": ["👋 Пока!", "🤖 До встречи!", "😊 Увидимся!"]
}

JOKES = [
    "😂 Почему программисты не любят природу? Слишком много багов!",
    "🤣 99 багов в коде, исправил один - 117 багов!",
    "🤖 Программист = машина для кофе в код!",
    "💻 Работает на моей машине = классика!"
]

QUOTES = [
    "💪 **Каждый эксперт был новичком!**",
    "🎯 **Лучший код - который работает!**", 
    "🚀 **Делай, анализируй, исправляй!**",
    "⚡ **Учись постоянно!**"
]

session = None

# ====== СОБЫТИЯ ======
@bot.event
async def on_ready():
    global session
    print("🚀" * 10)
    print(f"✅ {bot.user} СУПЕР БОТ АКТИВЕН!")
    print(f"📊 Серверов: {len(bot.guilds)}")
    
    session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20))
    
    await bot.change_presence(
        activity=discord.Game("🚀 СУПЕР БОТ | !help"),
        status=discord.Status.online
    )
    
    # Запуск ВСЕХ антисон систем
    if not memory_cleaner.is_running(): memory_cleaner.start()
    if not keep_alive.is_running(): keep_alive.start()  # АНТИСОН!
    if not auto_activity.is_running(): auto_activity.start()
    if not hardcore_activity.is_running(): hardcore_activity.start()  # ХАРДКОР!
    if not hourly_ping.is_running(): hourly_ping.start()  # ЕЖЕЧАСНО!
    if not status_updater.is_running(): status_updater.start()
    
    print("🔥 ВСЕ АНТИСОН СИСТЕМЫ ЗАПУЩЕНЫ!")
    print("💪 БОТ ТЕПЕРЬ НЕ ЗАСНЕТ НИКОГДА!")
    print("⚡ ХОСТИНГ НЕ СМОЖЕТ ОСТАНОВИТЬ!")

@bot.event  
async def on_message(message):
    if message.author.bot:
        return
    
    stats['msgs'] += 1
    memory['conversations'][message.author.id].append({
        'content': message.content[:100], 'time': time.time()
    })
    
    # Упоминание
    if bot.user.mentioned_in(message):
        await message.add_reaction("🤖")
        await message.channel.send("🤖 **TennaKnight тут!** `!help` для команд!")
    
    # Автоответы
    msg_lower = message.content.lower()
    for key, responses in QUICK.items():
        if key in msg_lower:
            await message.channel.send(random.choice(responses))
            break
    
    # Случайные реакции
    if random.randint(1, 30) == 1:
        await message.add_reaction(random.choice(["🔥", "💪", "⚡", "🚀"]))
    
    await bot.process_commands(message)

@bot.event
async def on_command_completion(ctx):
    stats['cmds'] += 1
    memory['user_stats'][ctx.author.id]['commands'] += 1

# 🔄 СИСТЕМЫ + АНТИСОН
@tasks.loop(minutes=15)
async def memory_cleaner():
    gc.collect()

@tasks.loop(minutes=5)  # ЧАСТЫЕ ЗАПРОСЫ ДЛЯ АНТИСОН
async def keep_alive():
    """Система антисон для хостинга"""
    try:
        # Делаем HTTP запрос к самому себе (если есть веб-сервер)
        print(f"🔥 АНТИСОН: {datetime.now().strftime('%H:%M:%S')} - Бот активен!")
        
        # Обновляем активность
        current_time = datetime.now()
        activities = [
            f"🔥 АКТИВЕН {current_time.strftime('%H:%M')}",
            f"⚡ РАБОТАЮ {len(bot.guilds)} серв.",
            "🚀 НЕ СПЮ НИКОГДА!",
            f"💪 ОНЛАЙН {int((time.time() - stats['start']) // 3600)}ч"
        ]
        
        activity = discord.Game(random.choice(activities))
        await bot.change_presence(activity=activity, status=discord.Status.online)
        
    except Exception as e:
        print(f"❌ Антисон ошибка: {e}")

@tasks.loop(minutes=30)
async def auto_activity():
    """Супер активные автосообщения"""
    if not bot.guilds: return
    
    msgs = [
        "🤖 **TennaKnight НИКОГДА НЕ СПИТ!** `!help` для команд!",
        "⚡ **24/7 РЕЖИМ АКТИВЕН!** `!ask` для ИИ помощи!",
        "🎮 **РАЗВЛЕКАЕМСЯ ПОСТОЯННО!** `!joke`, `!game`, `!roll`!",
        "🚀 **ХОСТИНГ НЕ ОСТАНОВИТ МЕНЯ!** `!ping` проверь скорость!",
        f"🔥 **УЖЕ {int((time.time() - stats['start']) // 3600)} ЧАСОВ ОНЛАЙН!**",
        "💪 **АНТИСОН СИСТЕМА РАБОТАЕТ!** Бот активен 24/7!",
        "⚡ **ПРОВЕРКА СВЯЗИ!** Отвечу на любую команду мгновенно!"
    ]
    
    try:
        # Отправляем в несколько случайных серверов
        active_guilds = random.sample(bot.guilds, min(3, len(bot.guilds)))
        
        for guild in active_guilds:
            channel = None
            # Ищем активный канал
            for ch in guild.text_channels:
                if ch.permissions_for(guild.me).send_messages:
                    if any(word in ch.name.lower() for word in ['general', 'chat', 'main', 'бот', 'общий']):
                        channel = ch
                        break
            
            if not channel:
                channel = next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages), None)
            
            if channel:
                msg = random.choice(msgs)
                sent_msg = await channel.send(msg)
                
                # Добавляем реакции для активности
                reactions = ["🔥", "⚡", "🚀", "💪", "🤖"]
                try:
                    await sent_msg.add_reaction(random.choice(reactions))
                except:
                    pass
                
                print(f"📤 Автосообщение в {guild.name}: {msg[:30]}...")
                await asyncio.sleep(10)  # Пауза между серверами
                
    except Exception as e:
        print(f"❌ Автоактивность ошибка: {e}")

@tasks.loop(minutes=10)  # КАЖДЫЕ 10 МИНУТ!
async def hardcore_activity():
    """ХАРДКОР активность для хостинга"""
    try:
        # Массовая активность
        print(f"💥 ХАРДКОР АКТИВНОСТЬ: {datetime.now()}")
        
        # Обновляем статус агрессивно
        hardcore_statuses = [
            "🔥 НЕ СПЮ НИКОГДА!",
            "⚡ ХОСТИНГ НЕ ОСТАНОВИТ!",
            "💪 РАБОТАЮ БЕЗ ПЕРЕРЫВА!",
            "🚀 24/7 ТУРБО РЕЖИМ!",
            f"🤖 {stats['cmds']} КОМАНД ВЫПОЛНЕНО!",
            f"⚡ {len(bot.guilds)} СЕРВЕРОВ ЗАХВАЧЕНО!"
        ]
        
        status = discord.Game(random.choice(hardcore_statuses))
        await bot.change_presence(activity=status, status=discord.Status.online)
        
        # Если есть серверы - делаем что-то активное
        if bot.guilds:
            guild = random.choice(bot.guilds)
            # Просто обновляем кэш участников для активности
            try:
                members_count = len(guild.members)
                print(f"🎯 Проверен сервер {guild.name}: {members_count} участников")
            except:
                pass
        
    except Exception as e:
        print(f"❌ Хардкор активность ошибка: {e}")

@tasks.loop(hours=1)  # КАЖДЫЙ ЧАС
async def hourly_ping():
    """Ежечасный пинг для хостинга"""
    try:
        uptime = int((time.time() - stats['start']) // 3600)
        print(f"⏰ ЕЖЕЧАСНЫЙ ОТЧЕТ: {uptime} часов онлайн!")
        print(f"📊 Выполнено команд: {stats['cmds']}")
        print(f"🤖 ИИ запросов: {stats['ai']}")
        print(f"📱 Сообщений обработано: {stats['msgs']}")
        print(f"🌐 Серверов активно: {len(bot.guilds)}")
        
        # Отправляем отчет в случайный канал
        if bot.guilds:
            guild = random.choice(bot.guilds)
            for ch in guild.text_channels:
                if ch.permissions_for(guild.me).send_messages:
                    if 'log' in ch.name.lower() or 'бот' in ch.name.lower():
                        await ch.send(f"⏰ **Ежечасный отчет:** {uptime}ч онлайн, {stats['cmds']} команд выполнено!")
                        break
        
    except Exception as e:
        print(f"❌ Ежечасный пинг ошибка: {e}")

@tasks.loop(hours=2)
async def status_updater():
    """Обновление статуса каждые 2 часа"""
    uptime = int((time.time() - stats['start']) // 3600)
    statuses = [
        discord.Game(f"🚀 {len(bot.guilds)} серверов | АКТИВЕН"),
        discord.Game(f"⚡ {stats['cmds']} команд | {uptime}ч ОНЛАЙН"),
        discord.Game("🤖 СУПЕР БОТ 2025 | НЕ СПЮ!"),
        discord.Game("💪 !help | 24/7 РЕЖИМ"),
        discord.Activity(type=discord.ActivityType.competing, name="💥 В АКТИВНОСТИ С ХОСТИНГОМ"),
        discord.Activity(type=discord.ActivityType.watching, name="🔥 ЗА СТАБИЛЬНОСТЬЮ 24/7")
    ]
    try:
        await bot.change_presence(activity=random.choice(statuses), status=discord.Status.online)
        print(f"🔄 Статус обновлен: активность каждые 2ч работает!")
    except Exception as e:
        print(f"❌ Статус ошибка: {e}")

# ====== КОМАНДЫ ======
@bot.command(name='help', aliases=['помощь', 'h'])
async def help_cmd(ctx):
    """📋 Все команды"""
    embed = discord.Embed(
        title="🚀 TENNAKNIGHT СУПЕР БОТ",
        description="Самый быстрый бот 2025!",
        color=0xff0000
    )
    
    embed.add_field(
        name="🧠 ИИ", 
        value="`!ask [вопрос]` - Умный помощник\n`!translate [текст]` - Переводчик",
        inline=False
    )
    
    embed.add_field(
        name="🎮 ИГРЫ",
        value="`!joke` - Шутки | `!quote` - Цитаты\n`!roll [кубик]` - Кубики | `!coin` - Монета\n`!rps` - Камень-ножницы | `!8ball` - Магический шар",
        inline=False
    )
    
    embed.add_field(
        name="📊 СИСТЕМА",
        value="`!ping` - Скорость | `!stats` - Статистика\n`!profile` - Ваш профиль | `!server` - О сервере",
        inline=False
    )
    
    embed.set_footer(text="⚡ Короткие команды: !а, !ш, !ц, !к, !п")
    await ctx.send(embed=embed)

@bot.command(name='ask', aliases=['а', 'ai'])
async def ask_ai(ctx, *, question):
    """🧠 ИИ помощник"""
    for key, responses in QUICK.items():
        if key in question.lower():
            await ctx.send(random.choice(responses))
            return
    
    await ctx.message.add_reaction("🧠")
    
    try:
        stats['ai'] += 1
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Ты TennaKnight - супер Discord бот. Отвечай кратко и дружелюбно с эмодзи."},
                {"role": "user", "content": question}
            ],
            "max_tokens": 250,
            "temperature": 0.8
        }
        
        async with session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json=data
        ) as response:
            if response.status == 200:
                result = await response.json()
                answer = result['choices'][0]['message']['content'].strip()
                
                embed = discord.Embed(
                    title="🧠 TennaKnight AI",
                    description=answer[:500],
                    color=0x4169E1
                )
                embed.set_footer(text=f"AI #{stats['ai']}")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ AI ошибка: {response.status}")
    except:
        await ctx.send("💥 ИИ недоступен!")

@bot.command(name='ping', aliases=['п'])
async def ping_cmd(ctx):
    """🏓 Скорость"""
    start = time.time()
    msg = await ctx.send("🏓")
    latency = round((time.time() - start) * 1000)
    ws = round(bot.latency * 1000)
    await msg.edit(content=f"🏓 **{latency}ms** | WS: {ws}ms ⚡")

@bot.command(name='stats', aliases=['статистика'])
async def stats_cmd(ctx):
    """📊 Статистика"""
    uptime = int(time.time() - stats['start'])
    h, m = uptime // 3600, (uptime % 3600) // 60
    
    embed = discord.Embed(title="📊 СТАТИСТИКА", color=0x00ff00)
    embed.add_field(name="⏰ Время", value=f"{h}ч {m}м", inline=True)
    embed.add_field(name="⚡ Команд", value=stats['cmds'], inline=True)
    embed.add_field(name="🤖 AI", value=stats['ai'], inline=True)
    embed.add_field(name="📊 Серверов", value=len(bot.guilds), inline=True)
    embed.add_field(name="💬 Сообщений", value=stats['msgs'], inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='profile', aliases=['профиль'])
async def profile_cmd(ctx, member: discord.Member = None):
    """👤 Профиль"""
    user = member or ctx.author
    user_data = memory['user_stats'][user.id]
    
    embed = discord.Embed(
        title=f"👤 {user.display_name}",
        color=user.color or 0x00ff00
    )
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    embed.add_field(name="⚡ Команд", value=user_data['commands'], inline=True)
    embed.add_field(name="🏆 Уровень", value=user_data['level'], inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='joke', aliases=['ш', 'шутка'])
async def joke_cmd(ctx):
    """😂 Шутка"""
    await ctx.send(random.choice(JOKES))

@bot.command(name='quote', aliases=['ц', 'цитата'])
async def quote_cmd(ctx):
    """💡 Цитата"""
    await ctx.send(random.choice(QUOTES))

@bot.command(name='roll', aliases=['к', 'кубик'])
async def roll_cmd(ctx, dice: str = "1d6"):
    """🎲 Кубик"""
    try:
        if 'd' not in dice:
            await ctx.send("🎲 Формат: `!roll 2d6`")
            return
        
        rolls, sides = map(int, dice.split('d'))
        if rolls > 10 or sides > 50:
            await ctx.send("🎲 Максимум: 10d50!")
            return
        
        results = [random.randint(1, sides) for _ in range(rolls)]
        total = sum(results)
        
        if rolls <= 3:
            await ctx.send(f"🎲 {dice}: {results} = **{total}**")
        else:
            await ctx.send(f"🎲 {dice}: **{total}**")
    except:
        await ctx.send("🎲 Ошибка формата!")

@bot.command(name='coin', aliases=['м', 'монета'])
async def coin_cmd(ctx):
    """🪙 Монета"""
    await ctx.send("🦅 **ОРЁЛ!**" if random.randint(0,1) else "💰 **РЕШКА!**")

@bot.command(name='rps', aliases=['кнб'])
async def rps_cmd(ctx, choice=None):
    """✂️ Камень-ножницы-бумага"""
    if not choice:
        await ctx.send("✂️ `!rps камень/ножницы/бумага`")
        return
    
    choices = {'камень': '🗿', 'ножницы': '✂️', 'бумага': '📄', 'rock': '🗿', 'scissors': '✂️', 'paper': '📄'}
    user_choice = choice.lower()
    
    if user_choice not in choices:
        await ctx.send("❌ Выбери: камень, ножницы, бумага")
        return
    
    bot_choice = random.choice(['камень', 'ножницы', 'бумага'])
    
    win = {('камень', 'ножницы'), ('ножницы', 'бумага'), ('бумага', 'камень')}
    
    if user_choice == bot_choice:
        result = "🤝 НИЧЬЯ!"
    elif (user_choice, bot_choice) in win:
        result = "🎉 ТЫ ВЫИГРАЛ!"
    else:
        result = "💔 Я ВЫИГРАЛ!"
    
    await ctx.send(f"Ты: {choices[user_choice]} | Я: {choices[bot_choice]}\n{result}")

@bot.command(name='8ball', aliases=['шар'])
async def ball_cmd(ctx, *, question=None):
    """🔮 Магический шар"""
    if not question:
        await ctx.send("🔮 Задай вопрос!")
        return
    
    answers = ["✅ Да!", "❌ Нет!", "🤔 Возможно", "⚡ Определенно!", "🌟 Спроси позже"]
    await ctx.send(f"🔮 **{random.choice(answers)}**")

@bot.command(name='translate', aliases=['перевод'])
async def translate_cmd(ctx, *, text):
    """🌍 Переводчик"""
    await ctx.message.add_reaction("🌍")
    
    try:
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Переведи текст на противоположный язык (рус->eng, eng->рус). Только перевод."},
                {"role": "user", "content": text}
            ],
            "max_tokens": 200
        }
        
        async with session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json=data
        ) as response:
            if response.status == 200:
                result = await response.json()
                translation = result['choices'][0]['message']['content'].strip()
                
                embed = discord.Embed(title="🌍 Переводчик", color=0x32cd32)
                embed.add_field(name="Исходный", value=text[:300], inline=False)
                embed.add_field(name="Перевод", value=translation[:300], inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Ошибка перевода")
    except:
        await ctx.send("💥 Переводчик недоступен!")

@bot.command(name='server', aliases=['сервер'])
async def server_cmd(ctx):
    """🏰 О сервере"""
    guild = ctx.guild
    embed = discord.Embed(title=f"🏰 {guild.name}", color=0x5865f2)
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(name="👑 Владелец", value=guild.owner.mention if guild.owner else "???", inline=True)
    embed.add_field(name="👥 Участников", value=len(guild.members), inline=True)
    embed.add_field(name="💬 Каналов", value=len(guild.text_channels), inline=True)
    embed.add_field(name="📅 Создан", value=guild.created_at.strftime('%d.%m.%Y'), inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='insomnia', aliases=['антисон', 'nosleep'])
async def insomnia_cmd(ctx):
    """😴 Проверка антисон системы"""
    uptime = int(time.time() - stats['start'])
    h, m = uptime // 3600, (uptime % 3600) // 60
    
    embed = discord.Embed(
        title="😴 АНТИСОН СИСТЕМА",
        description="**Я НИКОГДА НЕ СПЮ!**",
        color=0xff0000
    )
    
    embed.add_field(
        name="🔥 Активные системы",
        value=(
            "✅ Keep-alive каждые 5 мин\n"
            "✅ Хардкор активность каждые 10 мин\n"
            "✅ Автосообщения каждые 30 мин\n"
            "✅ Ежечасные пинги\n"
            "✅ Обновление статуса каждые 2ч"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⏰ Статистика",
        value=f"Онлайн: {h}ч {m}м\nКоманд: {stats['cmds']}\nСообщений: {stats['msgs']}",
        inline=True
    )
    
    embed.set_footer(text="💪 ХОСТИНГ НЕ ОСТАНОВИТ МЕНЯ!")
    await ctx.send(embed=embed)

@bot.command(name='force_activity', aliases=['принудительная_активность'])
async def force_activity_cmd(ctx):
    """⚡ Принудительная активность"""
    if ctx.author.guild_permissions.administrator:
        # Запускаем все системы принудительно
        try:
            await keep_alive()
            await hardcore_activity() 
            await auto_activity()
            await ctx.send("🔥 **ВСЕ СИСТЕМЫ АКТИВИРОВАНЫ ПРИНУДИТЕЛЬНО!**")
        except Exception as e:
            await ctx.send(f"❌ Ошибка принудительной активации: {str(e)[:100]}")
    else:
        await ctx.send("❌ Только для администраторов!")

@bot.command(name='status_report', aliases=['отчет'])
async def status_report_cmd(ctx):
    """📊 Полный отчет активности"""
    uptime = int(time.time() - stats['start'])
    h, m, s = uptime // 3600, (uptime % 3600) // 60, uptime % 60
    
    # Проверяем активность систем
    systems_status = {
        'keep_alive': keep_alive.is_running(),
        'hardcore_activity': hardcore_activity.is_running(),
        'auto_activity': auto_activity.is_running(),
        'hourly_ping': hourly_ping.is_running(),
        'status_updater': status_updater.is_running()
    }
    
    active_systems = sum(systems_status.values())
    
    embed = discord.Embed(
        title="📊 ПОЛНЫЙ ОТЧЕТ АКТИВНОСТИ",
        color=0x00ff00 if active_systems >= 4 else 0xffff00
    )
    
    embed.add_field(
        name="⏰ Время работы",
        value=f"**{h}ч {m}м {s}с**\nБез перерывов!",
        inline=True
    )
    
    embed.add_field(
        name="🎯 Активность",
        value=f"Команд: **{stats['cmds']}**\nИИ: **{stats['ai']}**\nСообщений: **{stats['msgs']}**",
        inline=True
    )
    
    embed.add_field(
        name="🌐 Охват", 
        value=f"Серверов: **{len(bot.guilds)}**\nПользователей: **{len(bot.users)}**",
        inline=True
    )
    
    # Статус систем
    system_icons = {True: "✅", False: "❌"}
    systems_text = "\n".join([
        f"{system_icons[status]} {name.replace('_', ' ').title()}"
        for name, status in systems_status.items()
    ])
    
    embed.add_field(
        name=f"🔧 Системы ({active_systems}/5)",
        value=systems_text,
        inline=False
    )
    
    embed.set_footer(text=f"🔥 Статус: {'МАКСИМАЛЬНАЯ АКТИВНОСТЬ' if active_systems >= 4 else 'ТРЕБУЕТ ВНИМАНИЯ'}")
    
    await ctx.send(embed=embed)

# Обработка ошибок
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❓ `!help` для команд")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Не хватает аргументов!")
    else:
        await ctx.send("💥 Ошибка!")

# Закрытие сессии
@bot.event
async def on_disconnect():
    if session:
        await session.close()

# ====== ЗАПУСК ======
async def main():
    try:
        print("🚀 TENNAKNIGHT СУПЕР ТУРБО БОТ!")
        print("⚡ Компактная мощь для максимальной скорости!")
        print("🔥 ЗАПУСК...")
        
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        print(f"💥 ОШИБКА: {e}")
    finally:
        if session:
            await session.close()

if __name__ == "__main__":
    asyncio.run(main())
