from app.config import executor
from app.server import dp

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
