from collections import UserDict
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date, timedelta


@dataclass
class Field:
    value: str

    def __str__(self) -> str:
        return self.value


class Name(Field):
    def __init__(self, value: str):
        self._validate_name(value)
        super().__init__(value)

    @staticmethod
    def _validate_name(value: str):
        if not value.isalpha():
            raise ValueError(f"Invalid name '{value}'. Name must contain only letters.")

    def __repr__(self):
        return f"Name: {self.value}"


class Phone(Field):
    def __init__(self, value: str):
        self._validate_phone(value)
        super().__init__(value)

    @staticmethod
    def _validate_phone(value: str):
        if not value.isdigit():
            raise ValueError(f"Wrong phone number format '{value}' must consist of digits only.")
        if not len(value) == 10:
            raise ValueError(f"Wrong phone number format '{value}' must contain exactly 10 digits.")

    def __repr__(self):
        return f"Phone: {self.value}"


class Record:
    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.phones: list[Phone] = []
        self.birthday = None

    def add_phone(self, phone: str) -> None:
        # Validate before anything else
        new_phone = Phone(phone)
        # Check for duplicates
        if any(p.value == new_phone.value for p in self.phones):
            raise ValueError(f"Phone number '{phone}' already exists for {self.name}.")
        self.phones.append(new_phone)

    def remove_phone(self, phone: str) -> None:
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return None
        raise ValueError(f"Phone number '{old_phone}' not found.")

    def find_phone(self, phone: str) -> None:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str) -> None:
        if birthday:
            self.birthday = Birthday(birthday)

    def __str__(self):
        phones = '\n    '.join(p.value for p in self.phones) or '—'
        bday = f"\n  Birthday: {self.birthday.value}" if self.birthday else ""
        return f"{self.name.value}:\n  Phones:\n    {phones}{bday}"

    def __repr__(self) -> str:
        phones_str = '; '.join(p.value for p in self.phones)
        if self.birthday:
            return f"Contact name: {self.name}, phones: {phones_str}, birthday: {self.birthday}"
        else:
            return f"Contact name: {self.name}, phones: {phones_str}"


class Birthday(Field):
    def __init__(self, value: str):
        date_format = "%d.%m.%Y"
        try:
            datetime.strptime(value, date_format)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

    @property
    def as_date(self):
        return datetime.strptime(self.value, "%d.%m.%Y").date()


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value.lower()] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name.lower())

    def delete(self, name: str) -> None:
        try:
            self.data.pop(name)
        except KeyError:
            raise KeyError(f"No record found with the name: {name}")

    def find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0)
        return birthday

    def date_to_string(self, date):
        return date.strftime('%d.%m.%Y')

    def get_upcoming_birthdays(self, days=7):
        today = date.today()

        for record in self.data.values():
            bd = getattr(record, "birthday", None)
            if not bd:
                continue

            birthday_this_year = bd.as_date.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if 0 <= (birthday_this_year - today).days <= days:
                if birthday_this_year.weekday() >= 5:
                    birthday_this_year = self.adjust_for_weekend(birthday_this_year)

                congratulation_date_str = self.date_to_string(birthday_this_year)
                yield {"name": record.name.value, "congratulation_date": congratulation_date_str}

    def show_upcoming_birthdays(self):
        return list(self.get_upcoming_birthdays())

    def __str__(self) -> str:
        if not self.data:
            return "Address Book is empty."
        return '\n'.join(str(record) for record in self.data.values())


# book = AddressBook()

# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
# john_record.add_birthday("21.10.2025")
# book.add_record(john_record)

# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# jane_record.add_birthday("20.12.2025")
# book.add_record(jane_record)

# jake_record = Record("Jake")
# jake_record.add_phone("9865433210")
# book.add_record(jake_record)

# seven_days = book.get_upcoming_birthdays(days=7)
# for bday in seven_days:
#     print(bday)
# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john.phones)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

# # Видалення запису Jane
# book.delete("Jane")
