import pandas as pd

def merge_tables(file1, file2, column1, column2, output_file, how='inner'):
    # Загрузка данных из Excel файлов
    table1 = pd.read_excel(file1)
    table2 = pd.read_excel(file2)

    if column1 not in table1.columns:
        raise KeyError(f"Столбец '{column1}' не найден в первой таблице.")
    if column2 not in table2.columns:
        raise KeyError(f"Столбец '{column2}' не найден во второй таблице.")
    
    # Соединение таблиц по столбцам
    merged_table = pd.merge(table1, table2, left_on=column1, right_on=column2, how=how)

    # Печать первых нескольких строк объединенной таблицы
    print("\nMerged Table:")
    print(merged_table.head())

    # Сохранение объединенной таблицы в новый Excel файл
    merged_table.to_excel(output_file, index=False)
    print(f"\nMerged table saved to '{output_file}'")

if __name__ == "__main__":
    file1 = 'C:/Users/Andrew/Desktop/1.xlsx'
    file2 = 'C:/Users/Andrew/Desktop/6.xlsx'
    column1 = 'id'
    column2 = 'id'
    output_file = 'C:/Users/Andrew/Downloads/resULT.xlsx'
    
    merge_tables(file1, file2, column1, column2, output_file, how='left')  # Здесь можно указать 'left', 'right' или 'outer'
