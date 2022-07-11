from .vi_cleaner import ViCleaner

def main():
        text_cleaned = ViCleaner("asd CĐV asda").clean()
        print(text_cleaned)

if __name__ == "__main__":
    main()