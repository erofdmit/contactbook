import pandas as pd
from operations.dataops import *
from config import *

while True:
        
        print('______________________________________________________')
        df = pd.read_csv(file_name, dtype=str)
        start_index = (page - 1) * records_per_page
        end_index = start_index + records_per_page
        if len(df) == 0:
            print("Контактов пока нет.")
        else:
            print(df.iloc[start_index:end_index])
        
        
        print("1. Следующая страница")
        print("2. Предыдущая страница")
        print("3. Добавить контакт")
        print("4. Изменить контакт")
        print("5. Удалить контакт")
        print("6. Выход")
        
        choice = input("Выберите команду (1/2/3/4/5/6): ")
        
        if choice == "1":
            
            max_page = (len(df) - 1) // records_per_page + 1
            page = min(page + 1, max_page)
        elif choice == "2":
            page -= 1
            if page < 1:
                page = 1
        elif choice == "3":
            new_record = []
            for header in headers:
                value = input(f"Введите {header.lower()}: ")
                new_record.append(value)
            add_record(file_name, dict(zip(headers, new_record)))
        elif choice == "4":
            index = int(input("Введите индекс контакта для изменения: "))
            column = input("Введите название колонки для изменения: ")
            new_value = input("Введите новое значение: ")
            edit_record(file_name, index, column, new_value)
        elif choice == "5":
            index = int(input("Введите индекс контакта для удаления: "))
            delete_record(file_name, index)
        elif choice == "6":
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите команду из списка.")
      