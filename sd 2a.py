import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Настройки подключения к базе данных
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'company_dbb'
}

def get_data():
    try:
        # Создание подключения к базе данных с использованием параметров из DB_CONFIG
        conn = mysql.connector.connect(**DB_CONFIG)
       
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()
       
        # Выполнение SQL-запроса для выборки всех данных из таблицы employees
        cursor.execute("SELECT * FROM employees")
       
        # Получение всех результатов запроса в виде списка кортежей
        data = cursor.fetchall()
       
        # Закрытие соединения с базой данных
        conn.close()
       
        # Возврат полученных данных
        return data
    except Exception as e:
        # В случае ошибки - показ сообщения об ошибке
        messagebox.showerror("Ошибка", f"Не удалось подключиться к базе:\n{e}")
       
        # Возврат пустого списка при ошибке
        return []

# Функция для добавления новой записи в базу данных
def add_new_record():
   
    # Создание нового окна для ввода данных
    add_window = tk.Toplevel()
    add_window.title("Добавление новой записи")
    add_window.geometry("400x300")
   
    tk.Label(add_window, text="ФИО:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    name_entry = tk.Entry(add_window, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=5)
   
    tk.Label(add_window, text="Должность:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    position_entry = tk.Entry(add_window, width=30)
    position_entry.grid(row=1, column=1, padx=10, pady=5)
   
    tk.Label(add_window, text="Отдел:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    dept_entry = tk.Entry(add_window, width=30)
    dept_entry.grid(row=2, column=1, padx=10, pady=5)
   
    tk.Label(add_window, text="Зарплата:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    salary_entry = tk.Entry(add_window, width=30)
    salary_entry.grid(row=3, column=1, padx=10, pady=5)
   
    tk.Label(add_window, text="Дата приема (ГГГГ-ММ-ДД):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    date_entry = tk.Entry(add_window, width=30)
    date_entry.grid(row=4, column=1, padx=10, pady=5)

   # Функция для сохранения записи в базу данных
    def save_record():
       
        # Получение данных из полей ввода
        name = name_entry.get()
        position = position_entry.get()
        dept = dept_entry.get()
        salary = salary_entry.get()
        date = date_entry.get()
       
        # Проверка заполнения всех полей
        if not all([name, position, dept, salary, date]):
            messagebox.showwarning("Предупреждение", "Все поля должны быть заполнены!")
            return
       
        try:
            # Подключение к базе данных
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
           
            # SQL-запрос для вставки новой записи
            query = "INSERT INTO employees (name, position, dept, salary, date) VALUES (%s, %s, %s, %s, %s)"
            values = (name, position, dept, salary, date)
           
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Запись успешно добавлена!")
            add_window.destroy()
            refresh_data()
           
        except Exception as e:
            # Показать сообщение об ошибке
            messagebox.showerror("Ошибка", f"Не удалось добавить запись:\n{e}")
   
    # Создание кнопки для сохранения
    save_btn = tk.Button(add_window, text="Сохранить", command=save_record, width=15)
    save_btn.grid(row=5, column=0, columnspan=2, pady=20)

# Функция для обновления данных в таблице
def refresh_data():
   
    for item in tree.get_children():
        tree.delete(item)
   
    data = get_data()
   
    for row in data:
        tree.insert('', tk.END, values=row)

# Функция для удаления выбранной записи из базы данных
def delete_record():
   
    # Получение выделенной записи в таблице
    selected_item = tree.selection()
   
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите запись для удаления!")
        return
   
    confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранную запись?")
   
    # Если пользователь отказался от удаления, прерываем выполнение функции
    if not confirm:
        return
   
    try:
        # Получение ID записи из выбранного элемента таблицы
        item_values = tree.item(selected_item[0], 'values')
        record_id = item_values[0]  # ID находится в первом столбце
       
        # Подключение к базе данных
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
       
        # SQL-запрос для удаления записи по ID
        query = "DELETE FROM employees WHERE id = %s"

        cursor.execute(query, (record_id,))
       
        conn.commit()
       
        conn.close()
       
        messagebox.showinfo("Успех", "Запись успешно удалена!")
       
        refresh_data()
       
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось удалить запись:\n{e}")
    
def show_data():
    global tree  # Делаем tree глобальной переменной для доступа из других функций
   
    window = tk.Toplevel()
    window.title("Данные из базы")
    window.geometry("800x500") 
   
    # Создаем фрейм для кнопок
    button_frame = tk.Frame(window)
    button_frame.pack(fill=tk.X, padx=10, pady=5)
   
    # Создаем кнопку для добавления новой записи
    add_btn = tk.Button(button_frame, text="Добавить запись", command=add_new_record, width=15)
    add_btn.pack(side=tk.LEFT, padx=5)
   
    # Создаем кнопку для обновления данных
    refresh_btn = tk.Button(button_frame, text="Обновить", command=refresh_data, width=10)
    refresh_btn.pack(side=tk.LEFT, padx=5)

    # СОЗДАЕМ КНОПКУ ДЛЯ УДАЛЕНИЯ ЗАПИСИ
    delete_btn = tk.Button(button_frame, text="Удалить запись", command=delete_record, width=15)
    delete_btn.pack(side=tk.LEFT, padx=5)
   
    data = get_data()
    if data:
        # Создаем таблицу
        tree = ttk.Treeview(window, columns=('id','name','position','dept','salary','date'), show='headings')
        tree.heading('id', text='ID')
        tree.heading('name', text='ФИО')
        tree.heading('position', text='Должность')
        tree.heading('dept', text='Отдел')
        tree.heading('salary', text='Зарплата')
        tree.heading('date', text='Дата приема')
        # Цикл для перебора всех строк в данных (data)
        for row in data:
            tree.insert('', tk.END, values=row)

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Блок else выполняется, если данных нет (data пустой или False)
    else:
    # Создание метки с текстом "Нет данных для отображения"
        label = tk.Label(window, text="Нет данных для отображения", fg="red")
   
    # Размещение метки в окне с вертикальным отступом 50 пикселей
        label.pack(pady=50)  

# Создаем главное окно
root = tk.Tk()
root.title("Главное окно")
root.geometry("300x200")

# Создаем кнопку просмотра
view_btn = tk.Button(root, text="Просмотр данных", command=show_data, width=20, height=2)
view_btn.pack(expand=True)

# Запускаем главный цикл
root.mainloop()