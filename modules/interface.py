from prettytable import PrettyTable
from modules.book import ContactBook
from objects.contact import Contact
from config import headers, contact_headers
from dataclasses import asdict
from dacite import from_dict

class Interface:
    def __init__(self, book: ContactBook, records_per_page: int = 5, current_page: int = 1):
        # Инициализация интерфейса с книгой контактов, текущей страницей и количеством записей на странице
        self.book = book
        self.current_page = current_page
        self.records_per_page = records_per_page

    
    def create_view(self):
         # Отображение контактов на текущей странице
        
        if self.book.len_of_book() == 0:
            print('Контактов пока нет')
        else:
            current_page_data = self.book.read(page = self.current_page, records_per_page = self.records_per_page)
            table_view = PrettyTable(headers)
            for contact_data in current_page_data:
                
                table_view.add_row(asdict(contact_data[1]).values())
            print(table_view)


    def comand_chooser(self):
        # Отображение доступных команд и выбор команды пользователем
        print("1. Следующая страница")
        print("2. Предыдущая страница")
        print("3. Добавить контакт")
        print("4. Изменить контакт")
        print("5. Поиск")
        print("6. Удаление")  
        print("7. Выход")  
        command = int(input('Введите номер команды: ')) 
        page = self.current_page
        match command:
            # Обработка выбора команды пользователем
            case 1:
                self.current_page = min(page + 1, self.book.len_of_book() // self.records_per_page + bool(self.book.len_of_book() % self.records_per_page))
                print('Страница №', self.current_page)
                self.main_poller()
            case 2:
                self.current_page = max(page - 1, 1)
                print('Страница №', self.current_page)
                self.main_poller()
            case 3:
                print('Создание контакта')
                self.user_create()
            case 4:
                print('Изменение контакта')
                self.user_update()
            case 5:
                print('Запускаем поиск')
                self.user_filter()
            case 6:
                number = input('Введите личный номер телефона для удаления: ')
                self.book.delete(number)
                self.main_poller()
            case 7:
                print('Выход из программы...')
                exit()
            case _:
                print('Введена неверная команда')
                self.main_poller()

                  

    
    def user_create(self):
         # Создание нового контакта с вводом данных пользователем
        contact = Contact()
        contact = asdict(contact)
        for header in headers:
            value = input(f"Введите {header.lower()}: ")
            contact_header = contact_headers[header]
            contact[contact_header] = value
        contact = from_dict(data_class=Contact, data=contact)
        self.book.create(contact)
        print('Cоздан контакт: ', contact)
        self.main_poller()

    
    def user_update(self):
         # Изменение существующего контакта с вводом данных пользователем
        index = input("Введите личный номер контакта для изменения: ")
        column = input("Введите название колонки для изменения: ")
        new_value = input("Введите новое значение: ")
        contact_header = contact_headers[column]
        self.book.update(phone=index, column=contact_header, new_value=new_value)
        self.main_poller()


    def user_filter(self):
         # Фильтрация контактов по параметрам, введенным пользователем
        settings = {}
        par_col = int(input('Введите количество параметров поиска: '))
        for i in range(0, par_col):
            key = input('Введите колонку для поиска: ')
            key = contact_headers[key]
            value = input('Введите необходимое значение: ')
            settings[key] = value
        
        result = self.book.search(settings)
        self.create_filter_view(result)
    
    def create_filter_view(self, filter_results):
        # Отображение результатов фильтрации
        table_view = PrettyTable(headers)
        for contact_data in filter_results:
                
            table_view.add_row(asdict(contact_data).values())
        print(table_view)
        self.comand_chooser()
    

    def main_poller(self):
        # Основной цикл интерфейса: отображение контактов и выбор команды
        self.create_view()
        self.comand_chooser()
        
        
        