from classes import AddressBook, Record
from functools import wraps


def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, TypeError) as e:
            return str(e)
        except Exception as e:
            return f"Unexpected error: {e}"
    return wrapper


def parse_input(user_input):
    # Parses user input into command and arguments.
    parts = user_input.split()
    if not parts:  # empty command check
        return "", []
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args


def find_record(name, book: AddressBook):
    record = book.find(name)
    if record:
        return record
    raise KeyError(f"No contact found with the name '{name}'")

@input_error
def change_number(args, book: AddressBook):
    if len(args) != 3:
        raise ValueError("Use: change [name] [old number] [new number]")
    name, old_number, new_number, *_ = args
    record = find_record(name, book)
    record.edit_phone(old_number, new_number)
    return f"Contact '{name}' changed: {old_number} → {new_number}"


@input_error
def add_contact(args, book: AddressBook):
    if len(args) == 1:
        name = args[0]
        phone = None
    elif len(args) >= 2:
        name, phone = args[:2]
    else:
        raise ValueError("Invalid number of arguments. Use: add [name] [optional phone]")
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"Contact with the name: {name} was created."
        if phone:
            record.add_phone(phone)
            message = f"Contact with the name: {name} and phone number: {phone} was created."
    else:
        message = f"The record with the name: {name} already exists"
        if phone:
            record.add_phone(phone)
            message = f"The phone number: {phone} was added to {name}'s contact"
    return message

@input_error
def find_contact(args, book: AddressBook):
    if len(args) == 1:
        name = args[0]
    else:
        raise ValueError("Invalid number of arguments. Use: phone [name]")
    record = find_record(name, book)
    if record.phones:
        phones = ', '.join(map(str, record.phones))
        return f"{name}'s phones: {phones}"
    else:
        return f"The contact with the name: {name} has no phones yet"


@input_error
def add_bd(args, book: AddressBook):
    if len(args) == 2:
        name, birthday = args[:2]
    else:
        raise ValueError("Invalid number of arguments. Use: Add-birtday [name] [birthday] in the format: DD.MM.YYYY")
    record = find_record(name, book)
    record.add_birthday(birthday)
    return f"The birthday date was added to {name}'s record"


@input_error
def show_bd(args, book: AddressBook):
    if len(args) == 1:
        name = args[0]
    else:
        raise ValueError("Invalid number of arguments. Use: Show-birthday [name]")
    record = find_record(name, book)
    bd = getattr(record, "birthday", None)
    if bd:
        return bd
    else:
        return f"No birthday date has been added to {name}'s record"


@input_error
def show_up_bds(book: AddressBook):
    birthdays = book.show_upcoming_birthdays()
    if birthdays:
        return "\n".join(
            [f"{len(birthdays)} upcoming birthdays found!"] +
            [f"Name: {b['name']}, Congratulations date: {b['congratulation_date']}" for b in birthdays]
            )
    else:
        return "No upcoming birthdays found in the next 7 days."


@input_error
def show_all(book: AddressBook):
    return str(book)


def main():
    book = AddressBook()
    print(r"""
   _____             .___    .__           _________  
  /     \   ____   __| _/_ __|  |   ____   \______  \ 
 /  \ /  \ /  _ \ / __ |  |  \  | _/ __ \      /    / 
/    Y    (  <_> ) /_/ |  |  /  |_\  ___/     /    /  
\____|__  /\____/\____ |____/|____/\___  >   /____/   
        \/            \/               \/             
  ________ ________  .______________                  
 /  _____/ \_____  \ |   \__    ___/                  
/   \  ___  /   |   \|   | |    |                     
\    \_\  \/    |    \   | |    |                     
 \______  /\_______  /___| |____|                     
        \/         \/                                 
          """)
    print("Welcome to the assistant bot!\n"
          "Please use the following commands:\n"
          "1. hello\n"
          "2. add\n"
          "3. phone\n"
          "4. change\n"
          "5. all\n"
          "6. add-birtday\n"
          "7. show-birthday\n"
          "8. birthdays\n"
          "9. close or Exit\n")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_number(args, book))

        elif command == "phone":
            print(find_contact(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_bd(args, book))

        elif command == "show-birthday":
            print(show_bd(args, book))

        elif command == "birthdays":
            print(show_up_bds(book))

        else:
            print("Invalid command!")


if __name__ == "__main__":
    main()
