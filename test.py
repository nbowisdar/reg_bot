import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--with_tg", action="store_true")


args = parser.parse_args()
if args.with_tg:
    pass