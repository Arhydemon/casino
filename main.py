from database.database_manager import DatabaseManager

def main() -> None:
    db = DatabaseManager()
    db.create_tables()
    db.close()
    print("я создал базу всё окей чюююююювак")

if __name__ == "__main__":
    main()