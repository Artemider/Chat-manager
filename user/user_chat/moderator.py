from user.Midllvary import rate_limit, ThrottlingMiddleware 
from create_bot import bot, dp
from config import moderator, ignore, chat_ignore
from database.start import base, cur

from aiogram import types, executor, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from time import time
import asyncio
import random
import datetime

'''*******************************************Code*****************************************************************'''
'''бан'''
# Commands "modermenu"
@rate_limit(5, 'modermenu')
async def modermenu(message: types.Message):
	user_id = message.from_user.id
	username = message.from_user.username
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) not in moderator:
		await message.reply('У вас недостатньо прав.')
		return

	await message.answer('/modermenu - меню команд администратора.\
		\n/mute - (число час причина) мут гравця.\
		\n/nmute - зняття муту з гравця.\
		')

#mute
@rate_limit(10, 'mute')
async def mute(message):
	user_id = message.from_user.id

	if str(user_id) not in moderator:
		await message.reply('У вас недостатньо прав.')
		return

	try:
		name1 = message.from_user.get_mention(as_html=True)
		args = message.get_args()
		if not message.reply_to_message:
			await message.reply("Команда має бути відповідю!")
			return
		if not args:
			await message.reply("Команда не має бути пуста!")
			return
		try:
			muteint = int(message.text.split()[1])
			mutetype = message.text.split()[2]
			comment = " ".join(message.text.split()[3:])
		except:
			await message.reply('Не правильно написано!\nПриклад:\n`/мут 1 г причина`')
			return
		if mutetype == "г" or mutetype == "годин" or mutetype == "h":
	
			await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, until_date=int(time()) + muteint*3600)
			await message.answer(f'Адмін: {name1};\n\nПорушник: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>;\nНа скільки: {muteint} {mutetype};\nПричина: {comment}.',  parse_mode='html')
		elif mutetype == "хв" or mutetype == "хвилин" or mutetype == "m":
	
			await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, until_date=int(time()) + muteint*60)
			await message.answer(f'Адмін: {name1};\n\nПорушник: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>;\nНа скільки: {muteint} {mutetype};\nПричина: {comment}.',  parse_mode='html')
		elif mutetype == "д" or mutetype == "днів" or mutetype == "d":
	
			await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, until_date=int(time()) + muteint*86400)
			await message.answer(f'Адмін: {name1};\n\nПорушник: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>;\nНа скільки: {muteint} {mutetype};\nПричина: {comment}.',  parse_mode='html')
	except:
		await message.answer('Ви не можете забанити модератора!')

#nmute
@rate_limit(10, 'nmute')
async def nmute(message):
	user_id = message.from_user.id

	if str(user_id) not in moderator:
		await message.reply('У вас недостатньо прав.')
		return

	usrep = message.reply_to_message.from_user.username
	if not message.reply_to_message:
		await message.reply("Команда має бути відповідю!")
		return

	await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, until_date=int(time()) + 30)
	await message.answer(f'Мут зменшений до 30с для:\n                     <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>',  parse_mode='html')

'''*******************************************bullet*****************************************************************'''

# Commands "lucky"
@rate_limit(5, 'lucky')
async def lucky(message: types.Message):
	user_id = str(message.from_user.id)

	if str(user_id) in moderator:
		await message.reply('Модерації заборонено!')
		return

	markup = InlineKeyboardMarkup()
	bbutton1 = InlineKeyboardButton(text="відміна!", callback_data='bbtn11')
	bbutton11 = InlineKeyboardButton(text="...клац...", callback_data='bbtn21')
	markup.add(bbutton11, bbutton1)

	await message.reply("Готовий до гри?", reply_markup=markup)

@dp.callback_query_handler(text = 'bbtn11')
@rate_limit(3, 'bbtn11')
async def bbtn11(callback_query: types.CallbackQuery):
	await callback_query.message.delete_reply_markup()

@dp.callback_query_handler(text = 'bbtn21')
@rate_limit(3, 'bbtn21')
async def bbtn21(callback_query: types.CallbackQuery):
	chat_id = str(callback_query.message.chat.id)
	user_id = str(callback_query.from_user.id)

	await callback_query.message.delete_reply_markup()
	#sleep(2)
	random_kr = random.randint(1,12)
	if random_kr == 1:
		itemr = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		item = int(itemr[0]) + 100
		c = f"<i>💶</i><b>100</b>"
		cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (item, user_id))
		base.commit()

		await callback_query.message.reply(f'Ви виграли {c}',  parse_mode='html')
	else:
		try:
			await bot.restrict_chat_member(chat_id = chat_id, user_id = user_id, until_date=int(time()) + 450)
			await callback_query.message.reply('Сьогодні удача не на твоїй стороні)')
		except:
			await callback_query.message.reply('З префіксом не можна!')

# Commands "su"
@rate_limit(2, 'su')
async def su(message: types.Message):

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

	await message.reply(f"<b>Героям слава!</b>",  parse_mode='html')


'''*******************************************start*****************************************************************'''

def register_handlers_moderator(dp : Dispatcher):
	dp.register_message_handler(modermenu, commands=["modermenu"])
	dp.register_message_handler(mute, commands=["mute"])
	dp.register_message_handler(nmute, commands=["nmute"])

	#bullet
	dp.register_message_handler(lucky, commands=["lucky"])

	#Слава Україні
	dp.register_message_handler(su, lambda message: message.text.startswith("Слава Україні"))