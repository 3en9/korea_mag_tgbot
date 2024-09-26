# import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
import asyncio
from base import add_basket, new_row, clear_basket, del_position, get_basket, new_order

# Вставьте сюда ваш токен
API_TOKEN = '7556339020:AAEloe-nvDTBpFw-4jv-RD6WgEryZiKzMBw'

# Логирование
# logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

manager_id = 7360205850


# Состояния
class Form(StatesGroup):
    waiting_for_store_number = State()
    waiting_for_product_link = State()
    waiting_for_product_details = State()
    waiting_for_delete_position = State()


# Кнопки главного меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать покупки 🛒")],
        [KeyboardButton(text="Посмотреть корзину 🛍")]
    ],
    resize_keyboard=True
)

# Кнопки корзины
cart_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Редактировать корзину ✏️")],
        [KeyboardButton(text="Сформировать заказ 📦")],
        [KeyboardButton(text="Назад 🔙")]
    ],
    resize_keyboard=True
)

# Кнопки редактирования корзины
edit_cart_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Удалить корзину ❌")],
        [KeyboardButton(text="Удалить позицию 🗑")],
        [KeyboardButton(text="Назад 🔙")]
    ],
    resize_keyboard=True
)
f = open('mags.txt')
txt = list(map(lambda x: x.split(':'), f.read().split('\n')))
f.close()
shop_dict = dict()
shop_list = 'Доступные магазины:\n'
for i in range(len(txt)):
    name = txt[i][0]
    url = ':'.join(txt[i][1:])
    shop_dict[i+1] = name
    shop_list += f'{i+1}. {name} {url}\n'

# print(shop_list)
print(shop_dict)

hi_message = 'Привет!\nС помощью этого бота ты можешь сформировать корзину с товарами, которые Поля отправит тебе из Кореи в Россию 🇰🇷🇷🇺.\nТы можешь просмотреть все доступные магазины и перейти по ссылкам на их официальные корейские сайты. Для удобства переведи их на английский или русский. Сохрани ссылки или артикулы на товары, которые тебе понравились, чтобы потом написать их в бот.\nПосле формирования корзины твой заказ будет направлен менеджеру Дарине, она свяжется с тобой для подтверждения состава корзины и информации по отправлению 📦\nЕсли возникнут вопросы, обращайся к менеджеру @darinasei.\nПриятного шоппинга 💋🛍️'


@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    try:
        new_row(message.from_user.id)
    except:
        pass
    await message.answer(hi_message, reply_markup=main_menu)


@dp.message(lambda message: message.text == "Начать покупки 🛒")
async def start_shopping(message: types.Message, state: FSMContext):
    await message.answer(shop_list)
    await message.answer("Введите номер магазина или название магазина из предложенных:")
    await state.set_state(Form.waiting_for_store_number)


@dp.message(Form.waiting_for_store_number)
async def store_number_entered(message: types.Message, state: FSMContext):
    await state.update_data(store_number=message.text)
    await message.answer("Введите ссылку или артикул товара:")
    await state.set_state(Form.waiting_for_product_link)


@dp.message(Form.waiting_for_product_link)
async def product_link_entered(message: types.Message, state: FSMContext):
    await state.update_data(product_link=message.text)
    await message.answer("Введите особенности (размер, цвет и т.д.):")
    await state.set_state(Form.waiting_for_product_details)


@dp.message(Form.waiting_for_product_details)
async def product_details_entered(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = message.from_user.id
    product = {
        "store": user_data['store_number'],
        "link": user_data['product_link'],
        "details": message.text
    }
    try:
        mag = shop_dict[int(product['store'])]
    except:
        mag = product['store']
    note = 'Магазин: ' + mag+'; Товар: '+product['link']+'; Детали: '+product['details']
    if not get_basket(user_id):
        new_row(user_id)
    add_basket(user_id, note)
    await message.answer("Товар успешно добавлен в корзину!", reply_markup=main_menu)
    await state.clear()


@dp.message(lambda message: message.text == "Посмотреть корзину 🛍")
async def view_cart(message: types.Message):
    user_id = message.from_user.id
    basket = get_basket(user_id)[1]
    if basket != 'NULL':
        basket = basket.split('\n')
        cart_items = "\n".join([f'{i+1}. {basket[i]}' for i in range(len(basket))])
        await message.answer(f"Ваша корзина:\n{cart_items}", reply_markup=cart_menu)
    else:
        await message.answer("Ваша корзина пуста.", reply_markup=main_menu)


@dp.message(lambda message: message.text == "Сформировать заказ 📦")
async def place_order(message: types.Message):
    user_id = message.from_user.id
    basket = get_basket(user_id)[1]
    if basket != 'NULL':
        new_order(user_id, basket)
        try:
            await bot.send_message(manager_id, f'Заказ от @{message.from_user.username}:\n'+basket)
        except:
            await message.answer("Заказ не может быть сформирован, попробуйте позже")
        else:
            clear_basket(user_id)
            await message.answer("Ваш заказ отправлен менеджеру.", reply_markup=main_menu)
    else:
        await message.answer("Ваша корзина пуста.", reply_markup=main_menu)


@dp.message(lambda message: message.text == "Редактировать корзину ✏️")
async def edit_cart(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=edit_cart_menu)


@dp.message(lambda message: message.text == "Удалить корзину ❌")
async def clear_cart(message: types.Message):
    user_id = message.from_user.id
    clear_basket(user_id)
    await message.answer("Корзина была успешно удалена.", reply_markup=main_menu)


@dp.message(lambda message: message.text == "Удалить позицию 🗑")
async def delete_position(message: types.Message, state: FSMContext):
    await message.answer("Введите номер позиции, которую хотите удалить:")
    await state.set_state(Form.waiting_for_delete_position)


@dp.message(Form.waiting_for_delete_position)
async def position_number_entered(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    basket = get_basket(user_id)[1]
    if basket != 'NULL':
        try:
            position_number = int(message.text) - 1
            if 0 <= position_number < len(basket.split('\n')):
                # user_cart[user_id].pop(position_number)
                del_position(user_id, position_number)
                await message.answer("Позиция успешно удалена.", reply_markup=cart_menu)
                await view_cart(message)
            else:
                await message.answer("Неверный номер позиции.", reply_markup=cart_menu)
        except ValueError:
            await message.answer("Введите корректный номер позиции.", reply_markup=cart_menu)
    else:
        await message.answer("Ваша корзина пуста.", reply_markup=main_menu)
    await state.clear()


@dp.message(lambda message: message.text == "Назад 🔙")
async def go_back(message: types.Message):
    await message.answer("Возвращаемся в меню...", reply_markup=main_menu)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
