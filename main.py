import re
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, value):
        if self.validate(value):
            super().__init__(value)
        else:
            raise ValueError("Phone number must be 10 digits.")

    def validate(self, value):
        return bool(re.fullmatch(r'\d{10}', value))


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        if any(phone.value == phone_number for phone in self.phones):
            print(f"Phone number '{phone_number}' is already added.")
            return

        try:
            phone = Phone(phone_number)
            self.phones.append(phone)
        except ValueError as e:
            print(f"Invalid phone number '{phone_number}': {e}")

    def remove_phone(self, phone_number):
        try:
            Phone(phone_number)
        except ValueError as e:
            print(f"Invalid phone number '{phone_number}': {e}")
            return

        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return

        print(f"Phone number '{phone_number}' not found. Nothing was removed.")

    def edit_phone(self, old_number, new_number):
        try:
            old_phone = Phone(old_number)
        except ValueError as e:
            print(f"Invalid phone number '{old_number}': {e}")
            return

        try:
            new_phone = Phone(new_number)
        except ValueError as e:
            print(f"Invalid phone number '{new_number}': {e}")
            return

        for i, phone in enumerate(self.phones):
            if phone.value == old_phone.value:
                self.phones[i] = new_phone
                print(
                    f"Phone number '{old_number}' changed to '{new_number}'.")
                return

        print(f"Phone number '{old_number}' not found. Cannot edit.")

    def find_phone(self, phone_number):
        try:
            Phone(phone_number)
        except ValueError as e:
            print(f"Invalid phone number '{phone_number}': {e}")
            return

        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        print(f"Phone number '{phone_number}' not found.")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value in self.data:
            print(f"Contact with name '{record.name.value}' already exists.")
            return
        self.data[record.name.value] = record

    def find(self, name):
        record = self.data.get(name)
        if record is None:
            print(f'Contact with name "{name}" not found.')
            return
        return record

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            print(f'Name "{name}" not found in the address book.')


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
