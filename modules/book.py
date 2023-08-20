import json
import os
from dataclasses import asdict
from objects.contact import Contact
from typing import List, Tuple
from dacite import from_dict

class ContactBook:
    def __init__(self, file_name: str):
        # Инициализация книги контактов с именем файла
        self.file_name = file_name
        
    
    def read_contacts_list(self) -> List[Contact]:
         # Чтение списка контактов из файла
        if not os.path.isfile(self.file_name):
                with open(self.file_name, mode='w') as file:
                    file.write('{"contacts" : []}')
                # Если файла не существует, создаем его и возвращаем пустой список
                return []
        else:
            try:
                with open(self.file_name) as file:
                    # Загрузка контактов из файла
                    data: List[dict] = json.load(file)
                    contacts = [Contact(**item) for item in data['contacts']]
                    
                    return contacts
            except:
                # В случае ошибки возвращаем пустой список
                return []
            
    def len_of_book(self) -> int:
        # Возвращает количество контактов в книге
        with open(self.file_name) as file:
            data: List[dict] = json.load(file)
            contacts = [Contact(**item) for item in data['contacts']]
                
            return len(contacts)

    def save_contacts_list(self, contacts_list: List[Contact]):
        # Сохраняет список контактов в файл
        a = []
        if not os.path.isfile(self.file_name):
            with open(self.file_name, mode='w') as file:
                 # Если файла не существует, создаем его
                a.append(contacts_list)
                file.write(json.dumps(a, indent=2))
        else:
            # Сохраняем контакт в файл
            for contact in contacts_list:
                with open(self.file_name, mode='w') as file:
                    a.append(asdict(contact))
                        
                    file.write(json.dumps({'contacts' : a}, indent=2))

    #CRUD
    def create(self, new_contact: Contact):
        # Добавляет новый контакт в книгу
        contacts = self.read_contacts_list()

        contacts.append(new_contact)

        self.save_contacts_list(contacts)
    
    def read(self, page: int, records_per_page: int) -> List[Tuple[int, Contact]]:
        # Чтение контактов с пагинацией
        contacts = self.read_contacts_list()
        
        enumerated_contacts = [(i, contact) for (i, contact) in enumerate(contacts)]

        start_record = (page - 1) * records_per_page
        end_record = min(start_record + records_per_page + 1, len(contacts))

        return enumerated_contacts[start_record:end_record]
    def find_by_phone(self, phone: str) -> int:
        """
        Находит индекс контакта по номеру телефона.
        Возвращает индекс контакта или None, если контакт не найден.
        """
        contacts = self.read_contacts_list()
        for index, contact in enumerate(contacts):
            if contact.mobile_phone == phone:
                return index
        return None
    '''
    def update(self, index, column, new_value):
        contacts = self.read_contacts_list()
        contact = asdict(contacts[index])
        contact[column] = new_value
        contact = from_dict(data_class=Contact, data=contact)
        print(contact)
        contacts[index] = contact
        print(contacts)
        self.save_contacts_list(contacts)
    '''
    def update(self, phone: str, column: str, new_value: str):
        """
        Обновляет контакт по номеру телефона.
        """
        contacts = self.read_contacts_list()
        index = self.find_by_phone(phone)
        if index is not None:
            contact = asdict(contacts[index])
            contact[column] = new_value
            updated_contact = from_dict(data_class=Contact, data=contact)
            contacts[index] = updated_contact
            self.save_contacts_list(contacts)
        else:
            print(f"Контакт с номером телефона {phone} не найден.")

    def delete(self, phone: str):
        """
        Удаляет контакт по номеру телефона.
        """
        index = self.find_by_phone(phone)
        if index is not None:
            contacts = self.read_contacts_list()
            del contacts[index]
            self.save_contacts_list(contacts)
        else:
            print(f"Контакт с номером телефона {phone} не найден.")

    def filter_func(self, settings):
        # Функция фильтрации контактов по заданным параметрам
        def f(x: Contact) -> bool:
            for key, value in settings.items():
                # Оставляем неполное совпадение по фильтру для того, чтобы можно было искать, к примеру, группы компаний 
                # Пример: по поиску "Газпром" выйдет "Газпромнефть", "Газпром-Снабжение" и т.д.
                # Если какой-либо ключ не совпадает, возвращаем False
                if value not in asdict(x)[key]:
                    return False
                    
            # Если все ключи совпадают, возвращаем True
            return True
        return f

    def search(self, settings):
        # Поиск контактов по заданным параметрам
        contacts = self.read_contacts_list()
        
        
        search_result = filter(self.filter_func(settings), contacts)

        return list(search_result)