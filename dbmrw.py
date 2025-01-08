import argparse
import json
import dbm


def main():
    parser = argparse.ArgumentParser(description="A DBM manipulation tool.")

    parser.add_argument("db_file", type=str, help="path to the DBM file")
    parser.add_argument(
        "db_key", type=str, nargs="?", help="the key for the entry", default=None
    )
    parser.add_argument(
        "db_value", type=str, nargs="?", help="the value (or \delete)", default=None
    )

    args = parser.parse_args()
    db_file = args.db_file.removesuffix(".db")

    if args.db_key is None:
        try:
            with dbm.open(db_file, "r") as db:
                print("{", end="")
                first = True
                for key in db.keys():
                    if not first:
                        print(",", end="")
                    else:
                        first = False
                    key_decoded = key.decode("utf-8")
                    val_decoded = db[key].decode("utf-8")
                    print(f'"{key_decoded}": "{val_decoded}"', end="")
                print("}")

        except dbm.error as e:
            print(f'File "{db_file}.db" does not exist.')

    elif args.db_value is None:
        try:
            with dbm.open(db_file, "r") as db:
                val_decoded = db[args.db_key].decode("utf-8")
                print(f'{{"{args.db_key}": "{val_decoded}"}}')
        except dbm.error as e:
            print(f'File "{db_file}.db" does not exist.')
        except KeyError as e:
            print(f'Key "{args.db_key}" does not exist.')

    elif args.db_value == "@delete":
        try:
            with dbm.open(db_file, "w") as db:
                del db[args.db_key]
                print(f'{{"{args.db_key}": NULL}}')
        except dbm.error as e:
            print(f'File "{db_file}.db" does not exist.')
        except KeyError as e:
            print(f'Key "{args.db_key}" does not exist.')

    else:
        with dbm.open(db_file, "c") as db:
            db[args.db_key] = args.db_value
            print(f'{{"{args.db_key}": "{args.db_value}"}}')


if __name__ == "__main__":
    main()
