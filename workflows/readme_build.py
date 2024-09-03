import os

from manifestos import ReadMe


def main():
    ReadMe().build()
    os.system('git add README.md')
    os.system('git commit -m "Updated README"')


if __name__ == "__main__":
    main()
