import pandas as pd

def add_record(file_name, data):

    df = pd.read_csv(file_name)
    new_row = pd.DataFrame(data, index = [0])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(file_name, index=False)
    print("Запись добавлена в файл:", data)

def edit_record(file_name, index, column, new_value):
    df = pd.read_csv(file_name)
    df.at[index, column] = new_value
    df.to_csv(file_name, index=False)
    print("Запись изменена:", df.loc[index])


def delete_record(file_name, index):
    df = pd.read_csv(file_name)
    df = df.drop(index)
    df.to_csv(file_name, index=False)
    print("Запись удалена")