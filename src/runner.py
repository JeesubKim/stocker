from db.dbms import DBMS


tables = ['stock_history','stock_item','stock_market']


def main():
    db = DBMS()
    print("Start here")
    for table in tables:
        print(db.select(table))


if __name__ == "__main__":
    main()