import discord
import random
import time
import json
import re
from discord.ext import commands
 
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # для получения содержимого сообщений
bot = commands.Bot(command_prefix='!', intents=intents)
bank = 0
balance = 0
inventar = []
rouletka = ["red", "black"]
total = bank + balance
# Словари для хранения времени последнего вызова команд
last_work_time = {}
last_crime_time = {}
last_slut_time = {}


data_file = "data.json"  # Файл для хранения данных

# Функция для загрузки данных
def load_data():
    global balance
    global bank
    global total
    try:
        with open("data.txt", "r") as f:
            for line in f.readlines():
                if line.startswith("balance="):
                    balance = int(line.split("=")[1].strip())
                elif line.startswith("bank="):
                    bank = int(line.split("=")[1].strip())
        total = bank + balance
    except FileNotFoundError:
        balance = 0
        bank = 0
        total = 0
# Функция для сохранения данных
def save_data():
    with open("data.txt", "w") as f:
        f.write(f"balance={balance}\n")
        f.write(f"bank={bank}\n")
        f.write(f"total={total}\n")

@bot.command()
async def hello(ctx):
    await ctx.send("Привет!")




@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    load_data()

@bot.command()
async def work(ctx):
    global balance
    global total
    user_id = ctx.author.id
    current_time = time.time()

    wait_time = 3600  # 1 час в секундах

    # Проверка времени последнего вызова команды work
    if user_id in last_work_time:
        elapsed_time = current_time - last_work_time[user_id]
        if elapsed_time < wait_time:
            remaining_time = wait_time - elapsed_time
            await ctx.send(f"Вы должны подождать еще {int(remaining_time // 60)} минут(ы) перед новым использованием команды work.")
            return

    # Выполнение команды
    rm = random.randint(20, 250)
    await ctx.send(f"Вы поработали дворником и получили {rm} малины.")
    balance += rm
    last_work_time[user_id] = current_time  # Обновляем время последнего вызова
    total = bank + balance
    save_data()
@bot.command()
async def crime(ctx):
    global balance
    global total
    user_id = ctx.author.id
    current_time = time.time()

    wait_time = 3600  # 1 час в секундах

    # Проверка времени последнего вызова команды crime
    if user_id in last_crime_time:
        elapsed_time = current_time - last_crime_time[user_id]
        if elapsed_time < wait_time:
            remaining_time = wait_time - elapsed_time
            await ctx.send(f"Вы должны подождать еще {int(remaining_time // 60)} минут(ы) перед новым использованием команды crime.")
            return

    # Выполнение команды
    rc = random.randint(1, 3)
    rcc = random.randint(300, 700)
    if rc == 1:
        await ctx.send(f"Вы попытались обворовать богатого мужчину, но он вас заметил и потревовал {rcc} малины.")
        balance -= rcc
    elif rc == 2:
        await ctx.send(f"Вы пробрались на поля, чтобы выкрасть урожай, но вас нашли и вы заплатили штраф в размере {rcc} малины.")
        balance -= rcc
    else:
        await ctx.send(f"Вы побили бездомного и забрали у него {rcc} малины. Как вам не стыдно!")
        balance += rcc
    total = bank + balance
    last_crime_time[user_id] = current_time  # Обновляем время последнего вызова
    save_data()
@bot.command()
async def slut(ctx):
    global balance
    global total
    user_id = ctx.author.id
    current_time = time.time()

    wait_time = 3600  # 1 час в секундах

    # Проверка времени последнего вызова команды slut
    if user_id in last_slut_time:
        elapsed_time = current_time - last_slut_time[user_id]
        if elapsed_time < wait_time:
            remaining_time = wait_time - elapsed_time
            await ctx.send(f"Вы должны подождать еще {int(remaining_time // 60)} минут(ы) перед новым использованием команды slut.")
            return

    # Выполнение команды
    rs = random.randint(1, 2)
    rss = random.randint(100, 400)
    if rs == 1:
        await ctx.send(f"Вы получили в подарок акции неизвестной компании и продали их за {rss} малины.")
        balance += rss
    else:
        await ctx.send(f"Вы заболели и отдали за лекарства {rss} малины.")
        balance -= rss
    total = bank + balance
    last_slut_time[user_id] = current_time  # Обновляем время последнего вызова
    save_data()
@bot.command()
async def money(ctx):
    global balance
    global bank
    global total
    await ctx.send(f"Деньги: {balance}")
    await ctx.send(f"Банк: {bank}")
    await ctx.send(f"Общий счет: {total}")

@bot.command()
async def inventory(ctx):
    if not inventar:
        await ctx.send("Ваш инвентарь пуст.")
    else:
        await ctx.send(", ".join(inventar))

@bot.command()
async def sbros(ctx):
    global balance, total, bank
    await ctx.send(f"Ваш баланс обнулен")
    balance = 0
    bank = 0
    await ctx.send(f"У вас целых {balance} малины")
    total = bank + balance
    save_data()

@bot.command()
async def roulette(ctx, bet: int, color: str):
    global balance
    global total
    
    if bet <= 0:
        await ctx.send("Ставка должна быть больше 0.")
        return

    if bet > balance:
        await ctx.send("У вас недостаточно малины для этой ставки.")
        return

    roulet_result = random.choice(rouletka)  # Случайный выбор между красным и черным

    await ctx.send(f"Вы ставите на **{color}**. Выпало: **{roulet_result}**.")
    balance -= bet  # Уменьшаем баланс на сумму ставки

    if color.lower() == "red":  # Если игрок ставит на красный
        if roulet_result == "red":
            await ctx.send(f"Вы победили и выиграли {bet * 2} малины!")
            balance += bet * 2  # Увеличиваем баланс
        else:
            await ctx.send(f"Вы проиграли и не получили ничего.")
    elif color.lower() == "black":  # Если игрок ставит на черный
        if roulet_result == "black":
            await ctx.send(f"Вы победили и выиграли {bet * 2} малины!")
            balance += bet * 2  # Увеличиваем баланс
        else:
            await ctx.send(f"Вы проиграли и не получили ничего.")
    else:
        await ctx.send("Недопустимый цвет. Пожалуйста, ставьте на **red** или **black**.")
    total = bank + balance
    save_data()
@bot.command()
async def money_money(ctx, a: int):
    global balance
    global total
    if a < 0:
        await ctx.send("Вы не можете получить отрицательное количество малин.")
        return

    await ctx.send(f"Вы получили {a} малины.")
    balance += a  # Увеличиваем баланс
    total = bank + balance
    save_data()
@bot.command()
async def deposit(ctx, a: str):
    global balance
    global bank
    global total
    if a.lower() == 'all':
        bank += balance
        balance = 0
        await ctx.send("Вы положили всю свою малину на банковский счет")
    else:
        a = int(a)
        if a > balance:
            await ctx.send("У вас недостаточно средств для депозита!")
            return
        balance -= a
        bank += a
        await ctx.send(f"Вы положили {a} на свой банковский счет")
    total = bank + balance
    save_data()
@bot.command()
async def withdraw(ctx, a: str):
    global balance
    global bank
    global total
    if a.lower() == "all":
        balance += bank
        bank = 0 
        await ctx.send("Вы сняли всю малину с банковского счета ")
    else:
        a = int(a)
        if a > bank:
            await ctx.send("У вас нет столько средств")
            return
        balance += a
        bank -= a
        await ctx.send(f"Вы сняли {a} малины со своего банковского счета")
    total = bank + balance
    save_data()


bot.run("token")

  
