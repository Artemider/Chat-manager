from user.Midllvary import rate_limit, ThrottlingMiddleware 
from create_bot import bot, dp
from config import ignore, chat_ignore, moderator, db_item, db_item_two, VIP, db_item_ignore
from database.start import base, cur

from aiogram import types, executor, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from math import floor
import time
import asyncio
import datetime
import random

'''*******************************************Func*****************************************************************'''

async def get_key(d, value, args):
	for k, v in d.items():
		if k == value:
			return v

async def balance(size, VP):

	lvl = floor(int(size)/100) + 1
	a = int(lvl) * -10

	if a >= 20:
		a = 19

	random_du = random.randint(a,20)

	if VP == True:
		random_du = random.randint(1,10)

	size_up = int(size) + random_du

	if size_up <= 0:
		random_du = random.randint(10,20)
		size_up = int(size) + random_du

	balance = [lvl, size_up, random_du]

	return balance

async def items(random_items, user_id, lucky):
	if random_items <= 90 and random_items >= 86:
		comment = '\nВи отримали: "💪".'

		frihand = cur.execute('SELECT frihand FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		frihand = frihand[0]
		frihand = int(frihand) + (1 * int(lucky))

		cur.execute('UPDATE inventory SET frihand == ? WHERE user_id == ?', (frihand, user_id))
		base.commit()

	elif random_items <= 85 and random_items >= 84:
		comment = '\nВи отримали: "⛽".'

		pump = cur.execute('SELECT pump FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		pump = pump[0]
		pump = int(pump) + (1 * int(lucky))

		cur.execute('UPDATE inventory SET pump == ? WHERE user_id == ?', (pump, user_id))
		base.commit()

	elif random_items == 83:
		comment = '\nВи отримали: "🧼".'

		grease = cur.execute('SELECT grease FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		grease = grease[0]
		grease = int(grease) + (1 * int(lucky))

		cur.execute('UPDATE inventory SET grease == ? WHERE user_id == ?', (grease, user_id))
		base.commit()

	elif random_items == 1:
		comment = '\nВи отримали: "🐰".'

		rabot = cur.execute('SELECT rabot FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		rabot = rabot[0]
		rabot = int(rabot) + 1

		cur.execute('UPDATE inventory SET rabot == ? WHERE user_id == ?', (rabot, user_id))
		base.commit()

	elif random_items <= 82 and random_items >= 77:
		comment = '\nВи отримали: "💼".'

		item_case = cur.execute('SELECT item_case FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item_case = item_case[0]
		item_case = int(item_case) + (1 * int(lucky))

		cur.execute('UPDATE inventory SET item_case == ? WHERE user_id == ?', (item_case, user_id))
		base.commit()

	elif random_items == 5:
		random_ = random.randint(0,3)
		if random_ == 1:
			comment = '\nВи отримали: "🔍".'
	
			magnifier = cur.execute('SELECT magnifier FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			magnifier = magnifier[0]
			magnifier = int(magnifier) + 1
	
			cur.execute('UPDATE inventory SET magnifier == ? WHERE user_id == ?', (magnifier, user_id))
			base.commit()
		else:
			comment = " "
	else:
		comment = " "

	return comment


'''*******************************************Code*****************************************************************'''

# Commands "Start"
@rate_limit(5, 'start')
async def comand_start(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = message.from_user.first_name
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	dt = datetime.datetime.now()
	data = datetime.date.today()

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	try:
		a = await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>. Я готовий!',  parse_mode='html')
	except:
		first_name = username
		if first_name == None:
			first_name = "Fredd"

		a = await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>. Я готовий!',  parse_mode='html')

	print(a.to_python)
	if message.chat.type == "private": pass
	if message.chat.type == "group" or message.chat.type == "supergroup" or message.chat.type == "channel":

		#try:
		#	num = cur.execute('SELECT * FROM chatlist ORDER BY number_chat DESC').fetchmany(1)
		#	num = num[0]
		#	num = num[0]
		#	number_chat = int(num) + 1

		#except:
		#	number_chat = 1

		num = cur.execute('SELECT MAX(number_chat) FROM chatlist').fetchone()
		number_chat = num[0] + 1 if num[0] else 1

		if chat_name != None: chat_name = chat_name
		if chat_name == None: chat_id = NoneName
		try:
			#awalist = []
			#chat_list = cur.execute('SELECT * FROM chatlist').fetchmany(10000)

			#for x in chat_list:
			#	chat_id_bd = x[2]
			#	awalist.append(chat_id_bd)
			try:
				siz = cur.execute('SELECT chat_id FROM chatlist WHERE chat_id == ?', (chat_id,)).fetchone()
				siz = str(siz[0])
			except:
				siz = str(1)

			if chat_id != siz:#not in awalist:
				cur.execute('INSERT INTO chatlist VALUES(?, ?, ?, ?)', (number_chat, chat_name, chat_id, data))
				base.commit()
				await bot.send_message(chat_id = 1101984099, text = f'<b>Nick</b>: <i><b><a href="tg://user?id={user_id}">{message.from_user.first_name}</a></b></i>.\n<b>Name</b>: {chat_name}.\n<b>Id</b>: {chat_id}.\n<b>Data</b>: {data}.',  parse_mode='html')
		except: pass

# Commands "Help"
@rate_limit(5, 'help')
async def help(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = message.from_user.first_name
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	markup = InlineKeyboardMarkup()
	button = InlineKeyboardButton(text="Про бота:", callback_data='btn1')
	button1 = InlineKeyboardButton(text="Команди:", callback_data='btn2')
	button2 = InlineKeyboardButton(text="Допомога автору:", callback_data='btn3')
	button3 = InlineKeyboardButton(text="Документація:", url='https://youtu.be/eBGIQ7ZuuiU?si=gil6xUlu9COnlPRI')
	markup.add(button, button1).add(button2).add(button3)

	await message.reply("Ось ця інформація, має бути корисна для вас", reply_markup=markup)

#Button1
@dp.callback_query_handler(text = 'btn1')
@rate_limit(3, 'btn1')
async def but1(callback_query: types.CallbackQuery):
	await callback_query.message.answer('<i>Бот створений, щоб привнести хаос у ваш чат.</i>',  parse_mode='html')
	await callback_query.message.delete_reply_markup()

#Button2
@dp.callback_query_handler(text = 'btn2')
@rate_limit(3, 'btn2')
async def but2(callback_query: types.CallbackQuery):
	await callback_query.message.answer('<b>start</b> - <i>запуск бота</i>.\
	\n<b>help</b> - <i>допомога</i>.\
	\n<b>dickup</b> - <i>збільшити пипірку</i>.\
	\n<b>topdick</b> - <i>топ</i>.\
	\n<b>profile</b> - <i>профіль</i>.\
	\n<b>use</b> - <i>(предмет) використати предмет</i>.\
	\n<b>give</b> - <i>(кількість) (предмет) передати предмет</i>.\
	\n<b>buy</b> - <i>(кількість) (предмет) купити предмет</i>.\
	\n<b>mine</b> - <i>отримати <b>coin</b></i>.\
	\n<b>shop</b> - <i>каталог предметів</i>.\
	\n<b>sell</b> - <i>(число) (предмет) (ціна) продати на аукціон</i>.\
	\n<b>kauf</b> - <i>(id товару) покупка на аукціоні</i>.\
	\n<b>market</b> - <i>подивитись аукціон</i>.\
	\n<b>cancel</b> - <i>(id товару) відмінити виставлення лоту</i>.\
	\n<b>case</b> - <i>відкрити скриню</i>.\
	\n<b>upname</b> - <i>оновлює нік</i>.\
	\n<b>bonuscode</b> - <i>(код) код з предметами</i>.\
	\n<b>lucky</b> - <i>рулетка на 100💶</i>.\
	',  parse_mode='html')
	await callback_query.message.delete_reply_markup()

#Button3
@dp.callback_query_handler(text = 'btn3')
@rate_limit(3, 'btn3')
async def but3(callback_query: types.CallbackQuery):
	await callback_query.message.answer('<b><i>Якщо хочеш підтримати автора:</i></b>\
		<b>5168 7520 2402 4112</b>',  parse_mode='html')
	await callback_query.message.delete_reply_markup()

'''*******************************************dickup*****************************************************************'''

# Commands "DickUp"
@rate_limit(2, 'dickup')
async def dickup(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title
	random_items = random.randint(0,100)

	time_dickup_bd = int(time.time()) + int(1200)

	lucky = 1
	print_lk = " "


	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	try:
		size = cur.execute('SELECT size FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
		size = size[0]

		try:
			time_dickup = cur.execute('SELECT time_dickup FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
			time_dickup = time_dickup[0]
	
			if int(time_dickup) > int(time.time()):
				raise SyntaxError(x)
		except:

			abc_time = int(time_dickup) - int(time.time())
			m = floor(int(abc_time)/60) 
			s = int(abc_time) - int(m*60) 
	
			if len(str(m)) < 2:
				m = str(0) + str(m)
	
			if len(str(s)) < 2:
				s = str(0) + str(s)
	
			await message.reply(f'Ви уже <b>збільшували пипірку</b>, наступний раз буде через <b>{m}:{s}</b>.',  parse_mode='html')
			return

	except:
		size = 0
	
	#---rabot---
	try:
		rabot = cur.execute('SELECT rabot FROM effect WHERE user_id == ?', (user_id,)).fetchone()
		rabot = int(rabot[0])

		if random_items <= 90 and random_items >= 77 and rabot > 0:

			lucky = random.randint(2,4)

			print_lk = f"\n<b>Удача</b>, ваші предмети збільшились у <b>{lucky}</b> раза."
			rabot = rabot - 1

			cur.execute('UPDATE effect SET rabot == ? WHERE user_id == ?', (rabot, user_id,))
			base.commit()
	except: pass

	#---grease---
	try:
		autofiller = cur.execute('SELECT autofiller FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		autofiller = int(autofiller[0])

		grease = cur.execute('SELECT grease FROM effect WHERE user_id == ?', (user_id,)).fetchone()
		grease = int(grease[0])
	
		if grease >= 1 and autofiller == 0:
			time_dickup_bd = int(time.time()) + int(300)
			
			grease = grease - 1

			cur.execute('UPDATE effect SET grease == ? WHERE user_id == ?', (grease, user_id,))
			base.commit()

		if autofiller >= 1:
			time_dickup_bd = int(time.time()) + int(180)
	except: pass

	VP = False
	if user_id in VIP:
		VP = True

	#func
	balanc = await balance(size, VP)
	lvl = balanc[0]
	size_up = balanc[1]
	random_du = balanc[2]

	try:
		siz = cur.execute('SELECT user_id FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
		siz = siz[0]
	except:
		#if user_id != siz:#not in awalist:
		cur.execute('INSERT INTO inventory VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, 75, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
		base.commit()
		cur.execute('INSERT INTO effect VALUES(?, ?, ?)', (user_id, 0, 0))
		base.commit()
		cur.execute('INSERT INTO bonuscode VALUES(?, ?, ?, ?, ?, ?)', (user_id, 1, 1, 1, 1, 1))
		base.commit()
		
		try:
			await message.reply(f'<i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i> ви збільшили свою пипірку на <b>{random_du}</b> см.\nВаш новий рахунок: <b>{random_du}</b> см.',  parse_mode='html')
			cur.execute('INSERT INTO size_table_dickup VALUES(?, ?, ?, ?, ?, ?)', (first_name, user_id, lvl, size_up, chat_id, time_dickup_bd,))
			base.commit()
			return
		except:
			first_name = username
			if first_name == None:
				first_name = "Fredd"

			await message.reply(f'<i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i> ви збільшили свою пипірку на <b>{random_du}</b> см.\nВаш новий рахунок: <b>{random_du}</b> см.',  parse_mode='html')
			cur.execute('INSERT INTO size_table_dickup VALUES(?, ?, ?, ?, ?, ?)', (first_name, user_id, lvl, size_up, chat_id, time_dickup_bd,))
			base.commit()
			return

	machine = cur.execute('SELECT machine FROM inventory WHERE user_id == ?', (user_id,)).fetchone()

	if int(machine[0]) > 0:
		balancd = await balance(size_up, False)
		lvl = balancd[0]
		size_up = balancd[1]
		random_du2 = balancd[2]
		#print([size, balanc, balancd, lvl, random_du2])

		random_du = int(random_du) + int(random_du2)


	cur.execute('UPDATE size_table_dickup SET size == ? WHERE user_id == ?', (size_up, user_id))
	base.commit()
	cur.execute('UPDATE size_table_dickup SET time_dickup == ? WHERE user_id == ?', (time_dickup_bd, user_id))
	base.commit()

	cur.execute('UPDATE size_table_dickup SET lvl == ? WHERE user_id == ?', (lvl, user_id))
	base.commit()

	#func
	comment = await items(random_items, user_id, lucky)

	text = f"<i><b>{first_name}</b></i>, ви збільшили свою пипірку на <b>{random_du}</b> см.\nВаш новий рахунок: <b>{size_up}</b> см.{comment}{print_lk}"

	#if chat_id == "-1001839081568":
	#	text = f"<i><b>{first_name}</b></i>, ви збільшили свою пипірку на <b>{random_du}</b> см.\nВаш новий рахунок: <b>{size_up}</b> см.{comment}{print_lk}\n\n<b>!!!<i>Через велику кількість спаму в чаті, бот переходить в @pipup_comm</i>!!!</b>"#(05.01.2023)

	try:
		await message.reply(f'{text}',  parse_mode='html')
	except:
		first_name = username
		if first_name == None:
			first_name = "Fredd"
		await message.reply(f'{text}',  parse_mode='html')

# Commands "topdick"
@rate_limit(2, 'topdick')
async def topdick(message: types.Message):

	#first_name, user_id, size integer, chat_id, time_dickup integer

	user_id = str(message.from_user.id)
	username = message.from_user.username
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	topdick = cur.execute('SELECT * FROM size_table_dickup ORDER BY size DESC').fetchmany(10)

	a = 0

	awalist = []
	for x in topdick:
		a += 1
		lc1 = x[0]
		lc2 = x[1]
		lc3 = x[3]

		awalist.append((f'<b>{a})</b><b>{lc1}</b> === <b>{lc3}</b> см;'))
	awatitle = '\n'.join(map(''.join,awalist))
	await message.answer(awatitle,  parse_mode='html')

'''*******************************************profile/use*****************************************************************'''

# Commands "profile"
@rate_limit(2, 'profile')
async def profile(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = message.from_user.first_name
	chat_id = str(message.chat.id)
	chat_name = message.chat.title
	medal = ""

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	try:
		s = cur.execute('SELECT * FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
		i = cur.execute('SELECT * FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		e = cur.execute('SELECT * FROM effect WHERE user_id == ?', (user_id,)).fetchone()

		inv_item = {"💪":["Frihand", i[2]], "⛽":["Pump", i[3]], "⚖️":["Libra", i[9]], "🧼":["Grease", i[4]], "🐰":["Rabot", i[5]], "💼":["Case", i[6]], "🔍":["Magnifier", i[7]], "🎛️":["Machine", i[8]], "🦾":["Ironhand", i[10]], "🧴":["Autofiller", i[11]], "🪙":["Treasury", i[12]], "🏅":["Medal", i[13]]}

		if int(i[13]) > 0:
			medal = "🏅"

		linv = []
		for k, v in inv_item.items():
			if int(v[1]) != 0:
				linv.append(f"   <i>{v[0]} {k}</i> == <b>{v[1]}</b>\n")

		inventory = ''.join(linv)

		name = s[0]
		size = s[3]
		lvl = s[2]

		lc2 = i[1]

		ef1 = e[1]
		ef2 = e[2]

		#if i == 0:


		if username == None:
			username = name

		title = f'<b>Ваш Профіль</b>\n\
			Nick: <i><b><a href="tg://user?id={user_id}">{username}</a></b></i>{medal}\n\
			Lvl: <b>{lvl}</b>\n\
			Coin: <b>{lc2}</b>\n\
			Size: <b>{size}</b>\n\
			------------------------------\n{inventory}\
			------------------------------\n\
			<i>grease</i> °= <b>{ef1}</b>\n\
			<i>rabot</i> °= <b>{ef2}</b>\n\
			------------------------------\n\
			'

		await message.answer(f'{title}',  parse_mode='html')
	except:
		await message.answer("Спробуйте: '/dickup'",  parse_mode='html')
		return

# Commands "use"
@rate_limit(2, 'use')
async def use(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = message.from_user.first_name
	chat_id = str(message.chat.id)
	chat_name = message.chat.title
	args = message.get_args()

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	if not args:
		await message.reply('Неправильно написано!\nПриклад:\n/use 🥚\n/use 1 🥚')
		return


	num = 1
	if args not in db_item.keys() and args not in db_item_two.keys():
		try:
			num = int(message.text.split()[1])
			args = message.text.split()[2]
		except: pass
	try:
		if args not in db_item.keys() and args not in db_item_two.keys():
			await message.answer(f"<b>Цього знаку, немає у Базі Даних!</b>",  parse_mode='html')
			return
	
		if args in db_item.keys():
			kind_item_name = db_item[args][0]
		if args in db_item_two.keys():
			db_ite = await get_key(db_item, db_item_two[args], args)
			kind_item_name = db_ite[0]
			args = db_item_two[args]
	
		if args in ["💼", "🎛️", "🧴", "🪙"]:
			await message.answer(f"<b>{args}</b>, працює по-іншому, /help.",  parse_mode='html')
			return
	
		if args not in ["💪", "💪🏻", "🦾", "🏅"]:
			kind_item = cur.execute(f'SELECT {kind_item_name} FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		
			if int(kind_item[0]) < 1*num:
				await message.answer(f"У вас немає <b>{args}</b>, попросіть у когось.",  parse_mode='html')
				return
		
			kind_item = int(kind_item[0]) - 1*num
		
			cur.execute(f'UPDATE inventory SET {kind_item_name} == ? WHERE user_id == ?', (kind_item, user_id))
			base.commit()
	
		if args == "💪" or args == "💪🏻":
			frihand = cur.execute('SELECT frihand FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		
			if int(frihand[0]) <= 0:
				await message.answer(f"У вас немає <b>{args}</b>, попросіть у когось.",  parse_mode='html')
				return
		
			time_dickup = cur.execute('SELECT time_dickup FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
			time_dickup = time_dickup[0]
		
			if int(time.time()) >= int(time_dickup):
				await message.answer(f"Ви <b>не використaли {args}</b> - у вас уже закінчився кулдаун.",  parse_mode='html')
				return
			frihand = int(frihand[0]) - 1
		
			cur.execute('UPDATE size_table_dickup SET time_dickup == ? WHERE user_id == ?', (int(time.time()), user_id))
			base.commit()
		
			cur.execute('UPDATE inventory SET frihand == ? WHERE user_id == ?', (frihand, user_id))
			base.commit()
		
			comment = "\nКулдаун знятий, можете збільшувати пипірку."
		
	
		if args == "⛽" or args == "⛽️":
			size = cur.execute('SELECT size FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
			size = int(size[0]) + 50*num
			
			lvl = floor(int(size)/100) + 1
	
			cur.execute('UPDATE size_table_dickup SET size == ? WHERE user_id == ?', (size, user_id))
			base.commit()
	
			cur.execute('UPDATE size_table_dickup SET lvl == ? WHERE user_id == ?', (lvl, user_id))
			base.commit()
	
			comment = f"\nПипірка збільшилась на <b>{50*num} см</b>"

		if args == "⚖️" or args == "⚖️":
			size_r = 0
			while num != 0:
				num -= 1
				random_items = random.randint(1,2)
				size_rs = 100
				if random_items == 2: size_rs = -100
				size_r = size_r + size_rs

			size = cur.execute('SELECT size FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
			size = int(size[0]) + size_r
			
			lvl = floor(int(size)/100) + 1
	
			cur.execute('UPDATE size_table_dickup SET size == ? WHERE user_id == ?', (size, user_id))
			base.commit()
	
			cur.execute('UPDATE size_table_dickup SET lvl == ? WHERE user_id == ?', (lvl, user_id))
			base.commit()
	
			comment = f"\nПипірка збільшилась на <b>{size_r} см</b>"			
	
		if args == "🧼" or args == "🧼":	
			grease = cur.execute('SELECT grease FROM effect WHERE user_id == ?', (user_id,)).fetchone()
	
			grease = int(grease[0])
			grease = grease + 5*num
	
			cur.execute('UPDATE effect SET grease == ? WHERE user_id == ?', (grease, user_id))
			base.commit()
	
			comment = f"\n<b>Змазка</b> допоможе вам на <b>{5*num}</b> наступних /dickup!"
	
		if args == "🐰" or args == "🐰":	
			rabot = cur.execute('SELECT rabot FROM effect WHERE user_id == ?', (user_id,)).fetchone()
	
			rabot = int(rabot[0])
			rabot = rabot + 5*num
	
			cur.execute('UPDATE effect SET rabot == ? WHERE user_id == ?', (rabot, user_id))
			base.commit()
	
			comment = f"\n<b>Удача</b> вам усміхнеться <b>{5*num}</b> раз!"
	
		if args == "🔍" or args == "🔍":	
			size = cur.execute('SELECT size FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
			size = int(size[0]) + 1250*num
			
			lvl = floor(int(size)/100) + 1
	
			cur.execute('UPDATE size_table_dickup SET size == ? WHERE user_id == ?', (size, user_id))
			base.commit()
		
	
			cur.execute('UPDATE size_table_dickup SET lvl == ? WHERE user_id == ?', (lvl, user_id))
			base.commit()

			comment = f"\nПипірка збільшилась на <b>{1250*num} см</b>"

		if args == "🦾":	
			ironhand = cur.execute('SELECT ironhand FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			time_dickup = cur.execute('SELECT time_dickup FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
			time_ironhand = cur.execute('SELECT time_ironhand FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			time_dickup = time_dickup[0]
			time_ironhand = time_ironhand[0]
		
			if int(ironhand[0]) <= 0:
				await message.answer(f"У вас немає <b>{args}</b>!",  parse_mode='html')
				return
		
			if int(time.time()) >= int(time_dickup):
				await message.answer(f"Ви <b>не використaли {args}</b> - у вас уже закінчився кулдаун.",  parse_mode='html')
				return

			if int(time.time()) <= int(time_ironhand):

				abc_time = int(time_ironhand) - int(time.time())
				m = floor(int(abc_time)/60) 
				s = int(abc_time) - int(m*60) 
	
				if len(str(m)) < 2:
					m = str(0) + str(m)
	
				if len(str(s)) < 2:
					s = str(0) + str(s)
	
				await message.reply(f'Ви уже <b>використaли {args}</b>, наступний раз буде через <b>{m}:{s}</b>.',  parse_mode='html')
				return

		if args == "🏅":	
			medal = cur.execute('SELECT medal FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		
			if int(medal[0]) <= 0:
				await message.answer(f"У вас немає <b>{args}</b>!",  parse_mode='html')
				return

			await bot.send_sticker(chat_id = chat_id, sticker="CAACAgIAAxkBAAELLGFlovUHAaHnF6AsWpiQv8If_aXSfwACSgIAAladvQrJasZoYBh68DQE")
			await message.reply(f'<b>Ви переможець!</b> Не втрачайте позиції /dickup.',  parse_mode='html')
			return
		
			comment = "\nКулдаун знятий, можете збільшувати пипірку."
	
		await message.answer(f"Ви <b>успішно</b> використали <b>{args}</b>.{comment}",  parse_mode='html')
	except:
		await message.answer(f"<b>У вас немає цього предмета!</b>\nСпробуйте: '/dickup'",  parse_mode='html')
	

# Commands "give"
@rate_limit(2, 'give')
async def give(message: types.Message):

	user_id = str(message.from_user.id)
	args = message.get_args()
	username = message.from_user.username
	first_name = message.from_user.first_name
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	if not message.reply_to_message:
		await message.reply("Команда має бути відповідю!")
		return


	reply_user_id = str(message.reply_to_message.from_user.id)
	reply_username = message.reply_to_message.from_user.username
	reply_first_name = message.reply_to_message.from_user.first_name

	if not args:
		await message.reply("Команда не має бути пуста!")
		return

	try:
		if reply_user_id == user_id:
			await message.reply("Передавайте іншим користувачам!")
			return	
		
		try:
			givint = int(message.text.split()[1])
			givtype = message.text.split()[2]
		except:
			await message.reply('Неправильно написано!\nПриклад:\n/give 1 🥚')
			return
	
		if 0 > givint:
			await message.answer(f"<b>Не можна передавати від'ємні предмети!</b>",  parse_mode='html')
			return
	
		if givtype not in db_item.keys() and givtype not in db_item_two:
			await message.answer(f"<b>Цього знаку, немає у Базі Даних!</b>",  parse_mode='html')
			return

		if givtype in db_item.keys():
			kind_item_name = db_item[givtype][0]
		if givtype in db_item_two.keys():
			db_ite = await get_key(db_item, db_item_two[givtype], givtype)
			kind_item_name = db_ite[0]
			givtype = db_item_two[givtype]

		kind_item = cur.execute(f'SELECT {kind_item_name} FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		
		if int(kind_item[0]) < givint:
			await message.answer(f"У вас замало <b>{givtype}</b>, попросіть у когось.",  parse_mode='html')
			return
		
		kind_item = int(kind_item[0]) - givint
		cur.execute(f'UPDATE inventory SET {kind_item_name} == ? WHERE user_id == ?', (kind_item, user_id))
		base.commit()
		
		try:
			reply_kind_item = cur.execute(f'SELECT {kind_item_name} FROM inventory WHERE user_id == ?', (reply_user_id,)).fetchone()
			reply_kind_item = int(reply_kind_item[0]) + givint
			cur.execute(f'UPDATE inventory SET {kind_item_name} == ? WHERE user_id == ?', (reply_kind_item, reply_user_id))
			base.commit()
		except:
			await message.answer(f"<b>Цього користувача, немає у Базі Даних!</b>",  parse_mode='html')
			return
	
		comment = f'Ви <b>успішно</b> передали <b>{givint}{givtype}</b>'
	
		try:
	
			await message.answer(f"{comment} користувачу <b>{reply_first_name}</b>.",  parse_mode='html')
		except:
	
			if reply_username == None:
				reply_username = "Fredd"
			await message.answer(f"{comment} користувачу <b>{reply_username}</b>.",  parse_mode='html')
	
	except:
		await message.answer(f"<b>У вас немає цього предмета!</b>\nСпробуйте: '/dickup'",  parse_mode='html')

'''*******************************************upname*****************************************************************'''

# Commands "upname"
@rate_limit(2, 'upname')
async def upname(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = message.from_user.first_name
	chat_id = str(message.chat.id)
	chat_name = message.chat.title
	args = message.get_args()
	
	if str(user_id) in ignore:
		return

	if str(chat_id) in chat_ignore:
		await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>.\n!!!<i>Бот перейшов в @pipup_comm</i>!!!!',  parse_mode='html')
		return

	try:
		cur.execute('UPDATE size_table_dickup SET first_name == ? WHERE user_id == ?', (first_name, user_id))
		base.commit()

		await message.answer(f"<b>Успішно!</b>",  parse_mode='html')
	except:
		await message.answer(f"<b>Вас немає в базі даних!</b>\nСпробуйте: '/dickup'",  parse_mode='html')

'''*******************************************start*****************************************************************'''

def register_handlers_user(dp : Dispatcher):

	#Code
	dp.register_message_handler(comand_start, commands=["start"])
	dp.register_message_handler(help, commands=["help"])

	#dickup
	dp.register_message_handler(dickup, commands=["dickup"])
	#dp.register_message_handler(topdickchat, commands=["topdickchat"])
	dp.register_message_handler(topdick, commands=["topdick"])

	#profile/use
	dp.register_message_handler(profile, commands=["profile"])
	dp.register_message_handler(profile, lambda message: message.text.startswith("Профіль"))
	dp.register_message_handler(use, commands=["use"])
	dp.register_message_handler(use, lambda message: message.text.startswith("Юз"))
	dp.register_message_handler(give, commands=["give"])
	dp.register_message_handler(give, lambda message: message.text.startswith("Дати"))

	#upname
	dp.register_message_handler(upname, commands=["upname"])