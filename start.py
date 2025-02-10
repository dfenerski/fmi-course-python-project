from click import command, option
from services.cli import BEAR_COEFFICIENT
from services.cli.functions.main import main as main2
from services.cli.functions.main2 import main2 as main3


@command()
@option('--count', default=1, help='Number of greetings.')
@option('--name', prompt='Your name',
        help='The person to greet.')
def main(count, name):
    print("Hello from monorepo-1!")
    print(BEAR_COEFFICIENT)
    print(main2())
    print(main3())


if __name__ == "__main__":
    main()
