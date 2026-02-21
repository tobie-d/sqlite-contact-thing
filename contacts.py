import time
import sqlite3

Running = True # so the user can use the app until they decide to close it
connection = sqlite3.connect("contacts.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT)")

print("Welcome to simple contact list db app.")
time.sleep(1)
print("Choose from the following options.")
time.sleep(1)
print("1. Add contact")
print("2. View all contacts")
print("3. Search all contacts")
print("4. Update contact")
print("5. Delete contact")
print("6. Exit")

while Running:
    choice = input("Enter number of option: ")
    if choice == "1": # add
        name = input("What is the name of your contact: ")
        phone = input("What is their phone number: ")
        email = input("What is their email: ")
        cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        connection.commit()
        print(f"Contact added: {name}!")# confirmation
    elif choice == "2": # view all
        cursor.execute("SELECT * FROM contacts")
        results = cursor.fetchall()
        if not results: print("No contacts saved"); continue
        for row in results:
            print(f"Name: {row[1]} | Phone: {row[2]} | Email: {row[3]}")
            print("-" * 65)
    elif choice == "3": # search all
        search_by_list = ["phone", "name", "email"]
        search_by = input("Please search by: Name, Phone or Email: ").lower()
        if search_by not in search_by_list:
            print("Make sure you choose from the options given.")
        else:
            search_input = "%" + input("Search by what you picked: ") + "%"# allow for searching similar so you don't need the exact name
            cursor.execute(f"SELECT * FROM contacts WHERE LOWER({search_by}) LIKE LOWER(?)", (search_input,))
            results = cursor.fetchall()
            if not results: print("No contacts found"); continue
            for row in results:
                print(f"Name: {row[1]} | Phone: {row[2]} | Email: {row[3]}")
                print("\n")

    elif choice == "4": # update
        search_input = "%" + input("Please enter a name: ") + "%"
        cursor.execute(f"SELECT * FROM contacts WHERE lower( name ) LIKE LOWER(?)", (search_input,))
        results = cursor.fetchall()
        if not results: print("No contacts found"); continue
        for row in results:
            print(f"Id: {row[0]} | Name: {row[1]} | Phone: {row[2]} | Email: {row[3]}")
        update_id = input("Which ID would you like to edit?: ")
        search_by_list = ["phone", "name", "email"]
        search_by = input("Please select from: Name, Phone or Email: ").lower()
        if search_by not in search_by_list:
            print("Make sure you choose from the options given.")
        else:
            new_value = input("What would you like to change it to?: ")
            cursor.execute(f"UPDATE contacts SET {search_by} = ? WHERE id = ?", (new_value, update_id,))
            connection.commit()
            print("Contact Updated!")


    elif choice == "5": # delete
        search_input = "%" + input("Please enter a name: ") + "%"
        cursor.execute(f"SELECT * FROM contacts WHERE lower( name ) LIKE LOWER(?)", (search_input,))
        results = cursor.fetchall()
        if not results: print("No contacts found"); continue
        for row in results:
            print(f"Id: {row[0]} | Name: {row[1]} | Phone: {row[2]} | Email: {row[3]}")
        delete_id = input("What ID would you like to delete?: ")
        cursor.execute("DELETE FROM contacts WHERE id = ?", (delete_id,))
        connection.commit()
        print("Contact Deleted!")

    elif choice == "6": # exit
        print("Goodbye!")
        connection.close()
        time.sleep(2)
        Running = False

    else:
        print("Please choose a number from the list!")
        
    connection.close()
