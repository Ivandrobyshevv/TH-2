from controller.controller import parser_init
from database.models.main import register_models


def main():
    register_models()
    parser_init()


if __name__ == "__main__":
    main()
