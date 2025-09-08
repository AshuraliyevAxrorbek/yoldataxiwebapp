import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router

API_TOKEN = "7890336132:AAHtFWGqDDxLWjc-Gp6C68_naRQIOCDnkCo"  # o'zingizning tokeningizni yozing

# Router
router = Router()

# Holatlar (FSM)
class DriverForm(StatesGroup):
    name = State()
    car_model = State()
    car_color = State()
    car_number = State()
    route = State()
    confirm = State()

# Start komandasi
@router.message(F.text == "/start")
async def start_cmd(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚖 Haydovchi bo‘lish")],
        ],
        resize_keyboard=True
    )
    await message.answer("Assalomu alaykum! 👋\nYo‘ldaTaxi haydovchilari tizimiga xush kelibsiz!", reply_markup=kb)

# Haydovchi bo‘lish tugmasi
@router.message(F.text == "🚖 Haydovchi bo‘lish")
async def driver_start(message: types.Message, state: FSMContext):
    await message.answer("Ism va familiyangizni kiriting:")
    await state.set_state(DriverForm.name)

# Ism va familiya
@router.message(DriverForm.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    # Mashina modellari ro‘yxati
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Gentra"), KeyboardButton(text="Cobalt")],
            [KeyboardButton(text="Damas"), KeyboardButton(text="Nexia 3")],
            [KeyboardButton(text="Malibu"), KeyboardButton(text="Tracker")],
        ],
        resize_keyboard=True
    )
    await message.answer("🚗 Mashina modelini tanlang:", reply_markup=kb)
    await state.set_state(DriverForm.car_model)

# Mashina modeli
@router.message(DriverForm.car_model)
async def get_car_model(message: types.Message, state: FSMContext):
    await state.update_data(car_model=message.text)
    await message.answer("Mashina rangini yozing:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(DriverForm.car_color)

# Mashina rangi
@router.message(DriverForm.car_color)
async def get_car_color(message: types.Message, state: FSMContext):
    await state.update_data(car_color=message.text)
    await message.answer("🚘 Mashina raqamini kiriting (masalan: 01A123BC):")
    await state.set_state(DriverForm.car_number)

# Mashina raqami
@router.message(DriverForm.car_number)
async def get_car_number(message: types.Message, state: FSMContext):
    await state.update_data(car_number=message.text)

    # Qaysi viloyatdan - qayerga
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Farg‘ona ➝ Toshkent")],
            [KeyboardButton(text="Andijon ➝ Toshkent")],
            [KeyboardButton(text="Namangan ➝ Toshkent")],
        ],
        resize_keyboard=True
    )
    await message.answer("📍 Qaysi yo‘nalishda qatnaysiz?", reply_markup=kb)
    await state.set_state(DriverForm.route)

# Yo‘nalish
@router.message(DriverForm.route)
async def get_route(message: types.Message, state: FSMContext):
    await state.update_data(route=message.text)
    data = await state.get_data()

    text = (
        "✅ Ma’lumotlaringiz:\n\n"
        f"👤 Ism-familiya: {data['name']}\n"
        f"🚗 Mashina: {data['car_model']} ({data['car_color']})\n"
        f"🔢 Raqam: {data['car_number']}\n"
        f"📍 Yo‘nalish: {data['route']}\n\n"
        "Hammasi to‘g‘rimi?"
    )

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Tasdiqlash")],
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True
    )
    await message.answer(text, reply_markup=kb)
    await state.set_state(DriverForm.confirm)

# Tasdiqlash
@router.message(DriverForm.confirm, F.text == "✅ Tasdiqlash")
async def confirm_data(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer("🎉 Ma’lumotlaringiz muvaffaqiyatli saqlandi!\nTez orada siz bilan bog‘lanamiz.", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

# Bekor qilish
@router.message(DriverForm.confirm, F.text == "❌ Bekor qilish")
async def cancel_data(message: types.Message, state: FSMContext):
    await message.answer("❌ Ma’lumot yuborish bekor qilindi.", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

# Main
async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
