from database.database_manager import DatabaseManager

def main() -> None:
    db = DatabaseManager()
    db.create_tables()

    profile = db.fetchone("SELECT * FROM profile LIMIT 1")
    if profile is None:
        db.execute(
            "INSERT INTO profile (login, balance) VALUES (?, ?)",
            ("Ватрушка", 5000))
        print("новый профиль создался, т.к. нихуя до этого не было")

    statistics = db.fetchone("SELECT * FROM statistics LIMIT 1")
    if statistics is None:
        db.execute(
            "INSERT INTO statistics (games_played, wins, total_win) VALUES (?, ?, ?)",
            (0, 0, 0))

    settings = db.fetchone("SELECT * FROM settings LIMIT 1")
    if settings is None:
        db.execute(
            "INSERT INTO settings (sound_enabled) VALUES (?)",
            (0,))
    db.close()

    print("я создал базу всё окей чюююююювак")

if __name__ == "__main__":
    main()