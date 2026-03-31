from connect import get_connection


def main():
    conn = get_connection()
    cur = conn.cursor()

    # 🔹 insert/update
    cur.callproc('insert_or_update_user', ('Aruzhan', '123456'))

    # 🔹 поиск
    cur.execute("SELECT * FROM search_contacts(%s)", ('Aru',))
    print("Search:", cur.fetchall())

    # 🔹 пагинация
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (5, 0))
    print("Paginated:", cur.fetchall())

    # 🔹 удаление
    cur.callproc('delete_contact', ('Aruzhan',))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()