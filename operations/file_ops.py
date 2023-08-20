import pandas as pd

def create_empty_csv(file_name, headers):
    df = pd.DataFrame(columns=headers)
    df.to_csv(file_name, index=False)
    print(f"Создан пустой файл {file_name} с заголовками: {', '.join(headers)}")