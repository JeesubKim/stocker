from db.dbms import DBMS

from monitor.manager import run_monitoring_items

tables = ['stock_history','stock_item','stock_market']


def main():
    db = DBMS()
    print("Start here")
    # for table in tables:
    #     print(db.select(table))


    run_monitoring_items()


if __name__ == "__main__":
    main()