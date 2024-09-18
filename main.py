
from src.c2 import start as start_c2, Log

if __name__ == '__main__':
    try:
        start_c2()
    except:
        print(Log.Error(f"Error, skipping.."))