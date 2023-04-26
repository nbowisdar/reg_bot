import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--with_tg", "-tg", action="store_true")


args = parser.parse_args()
print(args)
if args.with_tg:
    print(True)
