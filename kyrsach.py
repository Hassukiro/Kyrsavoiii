# импорт библиотек
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import psycopg2 as ps


# Функции для работы с таблицами
def manage_students():
    student_window = tk.Toplevel(root)
    student_window.title("Управление таблицей 'Студенты'")

    def view_students():
        try:
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            cursor.execute("SELECT идентификатор_студента, фамилия, имя, отчество, группа FROM Студенты")
            rows = cursor.fetchall()
            # Создаем новое окно для отображения данных
            view_window = tk.Toplevel(root)
            view_window.title("Просмотр студентов")
            # Создаем Treeview
            tree = ttk.Treeview(view_window)
            # Определяем столбцы
            tree['columns'] = ('идентификатор_студента', 'фамилия', 'имя', 'отчество', 'группа')
            # Форматируем наши столбцы
            tree.column("#0", width=0, stretch=tk.NO)
            tree.column("идентификатор_студента", anchor=tk.CENTER, width=80)
            tree.column("фамилия", anchor=tk.W, width=120)
            tree.column("имя", anchor=tk.W, width=120)
            tree.column("отчество", anchor=tk.W, width=120)
            tree.column("группа", anchor=tk.CENTER, width=80)
            # Создаем заголовки для каждого столбца
            tree.heading("#0", text="", anchor=tk.W)
            tree.heading("идентификатор_студента", text="ID", anchor=tk.CENTER)
            tree.heading("фамилия", text="фамилия", anchor=tk.W)
            tree.heading("имя", text="имя", anchor=tk.W)
            tree.heading("отчество", text="отчество", anchor=tk.W)
            tree.heading("группа", text="группа", anchor=tk.CENTER)
            # Добавляем данные в Treeview
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            # Упаковываем Treeview в окно
            tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            cursor.close()
            cnxn.close()
        except ps.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении данных: {e}")

    # Функция для удаления данных из таблицы 'Студенты'
    def delete_students():
        student_id = simpledialog.askstring("Удаление", "Введите ID студента для удаления:")
        if student_id:
            try:
                cnxn = connect_to_db()
                cursor = cnxn.cursor()
                cursor.execute("DELETE FROM Студенты WHERE идентификатор_студента = %s", (student_id,))
                cnxn.commit()
                messagebox.showinfo("Успех", "Студент успешно удалён")
                cursor.close()
                cnxn.close()
            except ps.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении данных: {e}")

    def add_students():
        # Создаем новое окно для добавления данных
        add_window = tk.Toplevel(root)
        add_window.title("Добавление студента")
        # Создаем виджеты для ввода данных нового студента
        tk.Label(add_window, text="идентификатор студента:").pack()
        id_entry = tk.Entry(add_window)
        id_entry.pack()
        tk.Label(add_window, text="фамилия:").pack()
        surname_entry = tk.Entry(add_window)
        surname_entry.pack()
        tk.Label(add_window, text="имя:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()
        tk.Label(add_window, text="отчество:").pack()
        patronymic_entry = tk.Entry(add_window)
        patronymic_entry.pack()
        tk.Label(add_window, text="группа:").pack()
        group_entry = tk.Entry(add_window)
        group_entry.pack()

        # Функция для обработки введенных данных и добавления их в базу данных
        def submit_student_data():
            # Получаем введенные данные
            ID = id_entry.get()
            surname = surname_entry.get()
            name = name_entry.get()
            patronymic = patronymic_entry.get()
            group = group_entry.get()
            # Проверяем, что все поля заполнены
            if ID and surname and name and patronymic and group:
                try:
                    cnxn = connect_to_db()
                    cursor = cnxn.cursor()
                    cursor.execute(
                        "INSERT INTO Студенты (идентификатор_студента, фамилия, имя, отчество, группа) VALUES (%s, %s, %s, %s, %s)",
                        (ID, surname, name, patronymic, group))
                    cnxn.commit()
                    messagebox.showinfo("Успех", "Студент успешно добавлен")
                    cursor.close()
                    cnxn.close()
                    add_window.destroy()
                except ps.Error as e:
                    messagebox.showerror("Ошибка", f"Ошибка при добавлении данных: {e}")

        submit_button = tk.Button(add_window, text="Добавить", command=submit_student_data)
        submit_button.pack()

    # Просмотр данных
    view_button = tk.Button(student_window, text="Просмотреть таблицу", command=view_students)
    view_button.pack(fill='x', padx=10, pady=5)
    # Добавление данных
    add_button = tk.Button(student_window, text="Добавить данные", command=add_students)
    add_button.pack(fill='x', padx=10, pady=5)
    # Удаление данных
    delete_button = tk.Button(student_window, text="Удалить данные", command=delete_students)
    delete_button.pack(fill='x', padx=10, pady=5)
    # Возврат в главное меню
    back_button = tk.Button(student_window, text="Назад", command=student_window.destroy)
    back_button.pack(fill='x', padx=10, pady=5)
    pass


def manage_teachers():
    teacher_window = tk.Toplevel(root)
    teacher_window.title("Управление таблицей 'Преподаватели'")

    # Функция для отображения данных
    def view_teachers():
        try:
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            cursor.execute("SELECT идентификатор_преподавателя, фамилия, имя, отчество FROM Преподаватели")
            rows = cursor.fetchall()
            # Создаем новое окно для отображения данных
            view_window = tk.Toplevel(root)
            view_window.title("Просмотр преподавателей")
            # Создаем Treeview
            tree = ttk.Treeview(view_window, columns=("идентификатор_преподавателя", "фамилия", "имя", "отчество"),
                                show="headings")
            # Настраиваем заголовки
            tree.heading("идентификатор_преподавателя", text="идентификатор")
            tree.heading("фамилия", text="фамилия")
            tree.heading("имя", text="имя")
            tree.heading("отчество", text="отчество")
            # Добавляем строки в Treeview
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            # Упаковываем Treeview в окно
            tree.pack(expand=True, fill='both')
            cursor.close()
            cnxn.close()
        except ps.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении данных: {e}")

    # Функция для удаления данных из таблицы 'Преподаватели'
    def teacher_id():
        teacher_id = simpledialog.askstring("Удаление", "Введите ID преподавателя для удаления:")
        if teacher_id:
            try:
                cnxn = connect_to_db()
                cursor = cnxn.cursor()
                cursor.execute("DELETE FROM Преподаватели WHERE идентификатор_преподавателя = %s", (teacher_id,))
                cnxn.commit()
                messagebox.showinfo("Успех", "Преподаватель успешно удалён")
                cursor.close()
                cnxn.close()
            except ps.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении данных: {e}")

    def add_teacher():
        add_window = tk.Toplevel(root)
        add_window.title("Добавление преподавателя")
        tk.Label(add_window, text="фамилия:").pack()
        surname_entry = tk.Entry(add_window)
        surname_entry.pack()
        tk.Label(add_window, text="имя:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()
        tk.Label(add_window, text="отчество:").pack()
        patronymic_entry = tk.Entry(add_window)
        patronymic_entry.pack()
        tk.Label(add_window, text="идентификатор_преподавателя:").pack()
        subject_entry = tk.Entry(add_window)
        subject_entry.pack()

        def submit_teacher_data():
            surname = surname_entry.get()
            name = name_entry.get()
            patronymic = patronymic_entry.get()
            subject = subject_entry.get()
            if surname and name and patronymic and subject:
                try:
                    cnxn = connect_to_db()
                    cursor = cnxn.cursor()
                    cursor.execute(
                        "INSERT INTO Преподаватели (фамилия, имя, отчество, идентификатор_преподавателя) VALUES (%s, %s, %s, %s)",
                        (surname, name, patronymic, subject))
                    cnxn.commit()
                    messagebox.showinfo("Успех", "Преподаватель успешно добавлен")
                    cursor.close()
                    cnxn.close()
                    add_window.destroy()
                except ps.Error as e:
                    messagebox.showerror("Ошибка", f"Ошибка при добавлении данных: {e}")

        submit_button = tk.Button(add_window, text="Добавить", command=submit_teacher_data)
        submit_button.pack()

    # Кнопки для управления таблицей преподавателей
    view_button = tk.Button(teacher_window, text="Просмотреть преподавателей", command=view_teachers)
    view_button.pack(fill='x', padx=10, pady=5)
    # Добавление данных
    add_button = tk.Button(teacher_window, text="Добавить данные", command=add_teacher)
    add_button.pack(fill='x', padx=10, pady=5)
    # Удаление данных
    delete_button = tk.Button(teacher_window, text="Удалить данные", command=teacher_id)
    delete_button.pack(fill='x', padx=10, pady=5)
    back_button = tk.Button(teacher_window, text="Назад", command=teacher_window.destroy)
    back_button.pack(fill='x', padx=10, pady=5)


def manage_subjects():
    subjects_window = tk.Toplevel(root)
    subjects_window.title("Управление таблицей 'Предметы'")

    def view_subjects():
        try:
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM Предметы")
            rows = cursor.fetchall()
            # Создаем новое окно для отображения данных
            view_window = tk.Toplevel(root)
            view_window.title("Просмотр предметов")
            # Создаем Treeview
            tree = ttk.Treeview(view_window, columns=("идентификатор_предмета", "название_предмета"), show="headings")
            # Настраиваем заголовки
            tree.heading("идентификатор_предмета", text="идентификатор_предмета")
            tree.heading("название_предмета", text="название_предмета")
            # Добавляем строки в Treeview
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            # Упаковываем Treeview в окно
            tree.pack(expand=True, fill='both')
            cursor.close()
            cnxn.close()
        except ps.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении данных: {e}")

    def add_subject():
        add_subject_window = tk.Toplevel(root)
        add_subject_window.title("Добавление нового предмета")
        tk.Label(add_subject_window, text="идентификатор предмета:").pack()
        id_subject_entry = tk.Entry(add_subject_window)
        id_subject_entry.pack()

        tk.Label(add_subject_window, text="название предмета:").pack()
        name_subject_entry = tk.Entry(add_subject_window)
        name_subject_entry.pack()

        def submit_subject():
            id_subject = id_subject_entry.get()
            name_subject = name_subject_entry.get()
            # Проверяем только обязательные поля
            if id_subject and name_subject:
                try:
                    cnxn = connect_to_db()
                    cursor = cnxn.cursor()
                    # При подготовке запроса используем None для NULL значений
                    cursor.execute(
                        "INSERT INTO Предметы (идентификатор_предмета, название_предмета) "
                        "VALUES (%s, %s)", (id_subject, name_subject))
                    cnxn.commit()
                    messagebox.showinfo("Успех", "Предмет успешно добавлен")
                    cursor.close()
                    cnxn.close()
                    add_subject_window.destroy()
                except ps.Error as e:
                    messagebox.showerror("Ошибка", f"Ошибка при добавлении предмета: {e}")
            else:
                messagebox.showwarning("Внимание",
                                       "Поля 'идентификатор предмета' и 'название предмета' должны быть заполнены")

        submit_button = tk.Button(add_subject_window, text="Добавить", command=submit_subject)
        submit_button.pack()

    def delete_subject():
        # Запрашиваем ID предмета, который нужно удалить
        id_subject = simpledialog.askstring("Удаление предмета", "Введите идентификатор предмета для удаления:")
        # Если пользователь ввел ID, пытаемся удалить предмет
        if id_subject:
            try:
                cnxn = connect_to_db()
                cursor = cnxn.cursor()
                # Выполняем запрос на удаление
                cursor.execute("DELETE FROM Предметы WHERE идентификатор_предмета = %s", (id_subject,))
                cnxn.commit()
                if cursor.rowcount == 0:
                    messagebox.showwarning("Внимание", "Предмет с таким идентификатором не найден.")
                else:
                    messagebox.showinfo("Успех", "Предмет успешно удален")
                cursor.close()
                cnxn.close()
            except ps.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении предмета: {e}")
        else:
            messagebox.showwarning("Внимание", "идентификатор предмета не введен")

    # Кнопки для управления таблицей предметов
    view_button = tk.Button(subjects_window, text="Просмотреть предметы", command=view_subjects)
    view_button.pack(fill='x', padx=10, pady=5)
    add_button = tk.Button(subjects_window, text="Добавить предмет", command=add_subject)
    add_button.pack(fill='x', padx=10, pady=5)
    delete_button = tk.Button(subjects_window, text="Удалить предмет", command=delete_subject)
    delete_button.pack(fill='x', padx=10, pady=5)
    # Возврат в главное меню
    back_button = tk.Button(subjects_window, text="Назад", command=subjects_window.destroy)
    back_button.pack(fill='x', padx=10, pady=5)


def manage_grades():
    # Создаем новое окно для управления оценками
    grades_window = tk.Toplevel(root)
    grades_window.title("Управление таблицей 'Оценки'")

    # Функция для просмотра оценок
    def view_grades():
        # Создаем новое окно для просмотра оценок
        view_grades_window = tk.Toplevel(grades_window)
        view_grades_window.title("Просмотр оценок")
        # Создаем и наполняем таблицу
        tree = ttk.Treeview(view_grades_window, columns=("id_grade", "id_record", "id_student", "id_subject", "grade"),
                            show="headings")
        tree.heading("id_grade", text="идентификатор оценки")
        tree.heading("id_record", text="идентификатор ведомости")
        tree.heading("id_student", text="идентификатор студента")
        tree.heading("id_subject", text="идентификатор предмета")
        tree.heading("grade", text="Оценка")
        tree.pack(fill='both', expand=True)
        # Заполняем таблицу данными из базы данных
        try:
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM Оценки")
            rows = cursor.fetchall()
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            cursor.close()
            cnxn.close()
        except ps.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении данных: {e}")

    # Функция для добавления оценки
    def add_grade():
        # Создаем новое окно для добавления оценки
        add_grade_window = tk.Toplevel(root)
        add_grade_window.title("Добавление оценки")
        # Создаем виджеты для ввода данных новой оценки
        tk.Label(add_grade_window, text="идентификатор оценки:").pack()
        id_grade_entry = tk.Entry(add_grade_window)
        id_grade_entry.pack()
        tk.Label(add_grade_window, text="идентификатор ведомости:").pack()
        id_record_entry = tk.Entry(add_grade_window)
        id_record_entry.pack()
        tk.Label(add_grade_window, text="идентификатор студента:").pack()
        id_student_entry = tk.Entry(add_grade_window)
        id_student_entry.pack()
        tk.Label(add_grade_window, text="идентификатор предмета:").pack()
        id_subject_entry = tk.Entry(add_grade_window)
        id_subject_entry.pack()
        tk.Label(add_grade_window, text="Оценка:").pack()
        grade_entry = tk.Entry(add_grade_window)
        grade_entry.pack()

        # Функция для обработки введенных данных и добавления их в базу данных
        def submit_grade_data():
            # Получаем введенные данные
            id_grade = id_grade_entry.get()
            id_record = id_record_entry.get()
            id_student = id_student_entry.get()
            id_subject = id_subject_entry.get()
            grade = grade_entry.get()
            # Проверяем, что все поля заполнены
            if id_grade and id_record and id_student and id_subject and grade:
                try:
                    cnxn = connect_to_db()
                    cursor = cnxn.cursor()
                    cursor.execute(
                        "INSERT INTO Оценки (идентификатор_оценки, идентификатор_ведомости, идентификатор_студента, идентификатор_предмета, оценка) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (id_grade, id_record, id_student, id_subject, grade))
                    cnxn.commit()
                    messagebox.showinfo("Успех", "Оценка успешно добавлена")
                    cursor.close()
                    cnxn.close()
                    add_grade_window.destroy()
                except ps.Error as e:
                    messagebox.showerror("Ошибка", f"Ошибка при добавлении оценки: {e}")
            else:
                messagebox.showwarning("Внимание", "Все поля должны быть заполнены")

        # Кнопка для отправки данных
        submit_button = tk.Button(add_grade_window, text="Добавить", command=submit_grade_data)
        submit_button.pack()

    # Функция для удаления оценки
    def delete_grade():
        # Запрашиваем идентификатор оценки, которую нужно удалить
        id_grade = simpledialog.askstring("Удаление оценки", "Введите идентификатор оценки для удаления:")
        # Проверяем, введен ли идентификатор оценки
        if id_grade:
            try:
                # Устанавливаем соединение с базой данных
                cnxn = connect_to_db()
                cursor = cnxn.cursor()
                # Выполняем запрос на удаление
                cursor.execute("DELETE FROM Оценки WHERE идентификатор_оценки = %s", (id_grade,))
                cnxn.commit()
                # Проверяем, была ли удалена строка
                if cursor.rowcount == 0:
                    # Если строка не была удалена, выводим предупреждение
                    messagebox.showwarning("Удаление не выполнено", "Оценка с таким идентификатором не найдена.")
                else:
                    # Если строка была удалена, выводим сообщение об успехе
                    messagebox.showinfo("Успех", "Оценка успешно удалена.")
                cursor.close()
                cnxn.close()
            except ps.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении оценки: {e}")
        else:
            messagebox.showwarning("Предупреждение", "идентификатор оценки не введен.")

    # Кнопки для различных операций
    view_button = tk.Button(grades_window, text="Просмотреть оценки", command=view_grades)
    view_button.pack(fill='x', padx=10, pady=5)
    add_button = tk.Button(grades_window, text="Добавить оценку", command=add_grade)
    add_button.pack(fill='x', padx=10, pady=5)
    delete_button = tk.Button(grades_window, text="Удалить оценку", command=delete_grade)
    delete_button.pack(fill='x', padx=10, pady=5)
    # Возврат в главное меню
    back_button = tk.Button(grades_window, text="Назад", command=grades_window.destroy)
    back_button.pack(fill='x', padx=10, pady=5)


def manage_exam_records():
    # Создаем новое окно для управления экзаменационными ведомостями
    exam_records_window = tk.Toplevel(root)
    exam_records_window.title("Управление 'Экзаменационной ведомостью'")

    def view_exam_records():
        # Создаем новое окно для просмотра экзаменационных ведомостей
        view_records_window = tk.Toplevel(root)
        view_records_window.title("Просмотр экзаменационных ведомостей")
        # Создаем таблицу Treeview для отображения данных
        columns = ('идентификатор ведомости', 'идентификатор предмета', 'дата создания ведомости')
        tree = ttk.Treeview(view_records_window, columns=columns, show='headings')
        # Определяем заголовки для каждой колонки
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        # Размещаем таблицу Treeview в окне
        tree.pack(side='left', fill='both', expand=True)
        # Добавляем полосу прокрутки
        scrollbar = ttk.Scrollbar(view_records_window, orient='vertical', command=tree.yview)
        try:
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            cursor.execute(
                "SELECT идентификатор_ведомости, идентификатор_предмета, дата_создания_ведомости FROM Экзаменационная_ведомость")
            rows = cursor.fetchall()
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            cursor.close()
            cnxn.close()
        except ps.Error as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при получении данных: {e}")

    def add_exam_record():
        # Создаем новое окно для добавления ведомости
        add_record_window = tk.Toplevel(exam_records_window)
        add_record_window.title("Добавление ведомости")
        # Поля для ввода данных новой ведомости
        tk.Label(add_record_window, text="идентификатор ведомости:").pack()
        id_record_entry = tk.Entry(add_record_window)
        id_record_entry.pack()
        tk.Label(add_record_window, text="идентификатор предмета:").pack()
        id_subject_entry = tk.Entry(add_record_window)
        id_subject_entry.pack()
        tk.Label(add_record_window, text="дата создания ведомости (ГГГГ-ММ-ДД):").pack()
        date_record_entry = tk.Entry(add_record_window)
        date_record_entry.pack()

        # Функция для обработки данных и добавления их в базу данных
        def submit_record():
            id_record = id_record_entry.get()
            id_subject = id_subject_entry.get()
            date_record = date_record_entry.get()
            # Проверка заполнения полей
            if id_record and id_subject and date_record:
                try:
                    # Подключаемся к базе данных и вставляем данные
                    cnxn = connect_to_db()
                    cursor = cnxn.cursor()
                    cursor.execute(
                        "INSERT INTO Экзаменационная_ведомость (идентификатор_ведомости, идентификатор_предмета, дата_создания_ведомости) "
                        "VALUES (%s, %s, %s)",
                        (id_record, id_subject, date_record))
                    cnxn.commit()
                    messagebox.showinfo("Успех", "Ведомость успешно добавлена")
                    cursor.close()
                    cnxn.close()
                    add_record_window.destroy()
                except ps.Error as e:
                    messagebox.showerror("Ошибка", f"Ошибка при добавлении ведомости: {e}")
            else:
                messagebox.showwarning("Предупреждение", "Все поля должны быть заполнены")

        # Кнопка подтверждения данных
        submit_button = tk.Button(add_record_window, text="Добавить", command=submit_record)
        submit_button.pack()

    # Функция для удаления ведомости
    def delete_exam_record():
        # Запрашиваем идентификатор ведомости для удаления
        id_record = simpledialog.askstring("Удаление ведомости", "Введите идентификатор ведомости для удаления:")
        if id_record:
            try:
                cnxn = connect_to_db()
                cursor = cnxn.cursor()
                cursor.execute("DELETE FROM Экзаменационная_ведомость WHERE идентификатор_ведомости = %s", (id_record,))
                cnxn.commit()
                messagebox.showinfo("Успех", "Ведомость успешно удалена")
                cursor.close()
                cnxn.close()
            except ps.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении ведомости: {e}")

    view_button = tk.Button(exam_records_window, text="Просмотреть ведомость", command=view_exam_records)
    view_button.pack(fill='x', padx=10, pady=5)
    add_button = tk.Button(exam_records_window, text="Добавить ведомость", command=add_exam_record)
    add_button.pack(fill='x', padx=10, pady=5)
    delete_button = tk.Button(exam_records_window, text="Удалить ведомость", command=delete_exam_record)
    delete_button.pack(fill='x', padx=10, pady=5)
    back_button = tk.Button(exam_records_window, text="Назад", command=exam_records_window.destroy)
    back_button.pack(fill='x', padx=10, pady=5)


def manage_subjects_teachers():
    window = tk.Toplevel()
    window.title("Управление Предметы_Преподаватели")

    def view_table():
        try:
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM Предметы_Преподаватели")
            rows = cursor.fetchall()
            cursor.close()
            cnxn.close()
            # Отображение данных
            display_window = tk.Toplevel(window)
            display_window.title("Данные таблицы Предметы_Преподаватели")
            tree = ttk.Treeview(display_window, columns=('teacher_subject_id, subject_id', 'teacher_id'), show='headings')
            tree.heading('teacher_subject_id', text='идентификатор предмета преподавателя')
            tree.heading('subject_id', text='идентификатор предмета')
            tree.heading('teacher_id', text='идентификатор преподавателя')
            tree.pack(expand=True, fill='both')
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
        except ps.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}")

    def add_data():
        # Функция добавления данных
        def submit():
            teacher_subject_id = teacher_subject_id_entry.get()
            subject_id = subject_id_entry.get()
            teacher_id = teacher_id_entry.get()
            try:
                cnxn = connect_to_db()
                cursor = cnxn.cursor()
                cursor.execute(
                    "INSERT INTO Предметы_Преподаватели (идентификатор_предмета_препода, идентификатор_предмета, идентификатор_преподавателя) VALUES (%s, %s, %s)",
                    (teacher_subject_id, subject_id, teacher_id))
                cnxn.commit()
                cursor.close()
                cnxn.close()
                messagebox.showinfo("Успешно", "Данные добавлены успешно")
                add_window.destroy()
            except ps.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка при добавлении данных: {e}")

        add_window = tk.Toplevel(window)
        add_window.title("Добавление данных")
        tk.Label(add_window, text="идентификатор предмета преподавателя:").pack()
        teacher_subject_id_entry = tk.Entry(add_window)
        teacher_subject_id_entry.pack()
        tk.Label(add_window, text="идентификатор предмета:").pack()
        subject_id_entry = tk.Entry(add_window)
        subject_id_entry.pack()
        tk.Label(add_window, text="идентификатор преподавателя:").pack()
        teacher_id_entry = tk.Entry(add_window)
        teacher_id_entry.pack()
        tk.Button(add_window, text="Добавить", command=submit).pack()

    def delete_data():
        # Функция удаления данных
        def submit():
            id_to_delete = id_entry.get()
            try:
                cnxn = connect_to_db()
                cursor = cnxn.cursor()
                cursor.execute("DELETE FROM Предметы_Преподаватели WHERE идентификатор_предмета_препода = %s", (id_to_delete,))
                cnxn.commit()
                cursor.close()
                cnxn.close()
                messagebox.showinfo("Успешно", "Данные удалены успешно")
                delete_window.destroy()
            except ps.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении данных: {e}")

        delete_window = tk.Toplevel(window)
        delete_window.title("Удаление данных")
        tk.Label(delete_window, text="Введите ID для удаления:").pack()
        id_entry = tk.Entry(delete_window)
        id_entry.pack()
        tk.Button(delete_window, text="Удалить", command=submit).pack()

    view_button = tk.Button(window, text="Просмотреть ведомость", command=view_table)
    view_button.pack(fill='x', padx=10, pady=5)
    add_button = tk.Button(window, text="Добавить ведомость", command=add_data)
    add_button.pack(fill='x', padx=10, pady=5)
    delete_button = tk.Button(window, text="Удалить ведомость", command=delete_data)
    delete_button.pack(fill='x', padx=10, pady=5)
    back_button = tk.Button(window, text="Назад", command=window.destroy)
    back_button.pack(fill='x', padx=10, pady=5)


# Выполнение SQL-запросов
def execute_queries():
    queries_window = tk.Toplevel(root)
    queries_window.title("Выполнение запросов к базе данных")

    # Экзаменационная ведомость определенной группы
    def get_exam_record_details():
        group_name = simpledialog.askstring("Получение данных", "Введите название группы:")
        record_id = simpledialog.askstring("Получение данных", "Введите идентификатор ведомости:")
        if group_name and record_id:
            query = """
                SELECT 
                    ev.идентификатор_ведомости, 
                    ev.дата_создания_ведомости, 
                    st.имя, 
                    st.фамилия, 
                    st.отчество, 
                    oc.оценка, 
                    p.название_предмета,
                    pr.фамилия + ' ' + pr.имя + ' ' + pr.отчество AS Преподаватель
                FROM 
                    Экзаменационная_ведомость ev
                INNER JOIN Оценки oc ON ev.идентификатор_ведомости = oc.идентификатор_ведомости
                INNER JOIN Студенты st ON oc.идентификатор_студента = st.идентификатор_студента
                INNER JOIN Предметы_Преподаватели pp ON ev.идентификатор_предмета = pp.идентификатор_предмета
                INNER JOIN Предметы p ON pp.идентификатор_предмета = p.идентификатор_предмета
                INNER JOIN Преподаватели pr ON pp.идентификатор_преподавателя = pr.идентификатор_преподавателя
                WHERE 
                    st.группа = %s AND ev.идентификатор_ведомости = %s
            """
            execute_sql_query(query, [group_name, record_id])
        else:
            messagebox.showinfo("Информация", "Необходимо ввести и название группы, и идентификатор ведомости.")

    def execute_sql_query(query, params):
        try:
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            # Создаем окно для отображения результатов
            result_window = tk.Toplevel(root)
            result_window.title("Детали ведомости")
            # Определяем колонки для отображения
            columns = ("идентификатор_ведомости", "дата_создания_ведомости", "имя", "фамилия", "отчество", "оценка",
                       "название_предмета", "Преподаватель")
            tree = ttk.Treeview(result_window, columns=columns, show='headings')
            # Настраиваем заголовки колонок
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            tree.pack(expand=True, fill='both')
            # Заполняем таблицу данными
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            # Добавляем скроллбар
            scrollbar = ttk.Scrollbar(result_window, command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)
            cursor.close()
            cnxn.close()
        except ps.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}")

    def get_students_by_group():
        # Запрашиваем название группы у пользователя
        group_name = simpledialog.askstring("Получение данных", "Введите название группы для вывода:")
        if group_name:
            # Формируем SQL-запрос для получения данных студентов определенной группы
            query = f"""
                SELECT 
                    идентификатор_студента, 
                    фамилия, 
                    имя, 
                    отчество, 
                    группа
                FROM 
                    Студенты
                WHERE 
                    группа = %s
            """
            # Вызываем функцию для выполнения SQL-запроса и отображения результатов
            execute_sql_query_and_display_results(query, [group_name])
        else:
            messagebox.showerror("Ошибка ввода", "Необходимо ввести название группы для вывода данных.")

    def execute_sql_query_and_display_results(query, params):
        try:
            # Подключаемся к базе данных
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            # Выполняем запрос с параметрами
            cursor.execute(query, params)
            rows = cursor.fetchall()
            # Закрываем соединение с базой
            cursor.close()
            cnxn.close()
            # Создаем окно для отображения данных
            result_window = tk.Toplevel(root)
            result_window.title("Список студентов группы")
            # Создаем таблицу для отображения данных
            columns = ('идентификатор_студента', 'фамилия', 'имя', 'отчество', 'группа')
            tree = ttk.Treeview(result_window, columns=columns, show='headings')
            # Устанавливаем заголовки для колонок и их ширину
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            # Добавляем данные в таблицу
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            # Размещаем таблицу на экране
            tree.pack(expand=True, fill='both')
            scrollbar = ttk.Scrollbar(result_window, command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)
        except ps.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}")

    def get_average_grade_for_subject():
        # Запрашиваем название предмета у пользователя
        subject_name = simpledialog.askstring("Получение данных", "Введите название предмета:")
        if subject_name:
            # SQL-запрос для расчета средней оценки по предмету
            query = """
            SELECT p.название_предмета, AVG(o.оценка) AS Средняя_оценка
            FROM Оценки o
            INNER JOIN Предметы p ON o.идентификатор_предмета = p.идентификатор_предмета
            WHERE p.название_предмета = %s
            GROUP BY p.название_предмета
            """
            execute_sql_query_and_display(query, [subject_name])
        else:
            messagebox.showinfo("Информация", "Необходимо ввести название предмета.")

    def execute_sql_query_and_display(query, params):
        try:
            # Подключаемся к базе данных
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            # Выполняем запрос с параметрами
            cursor.execute(query, params)
            rows = cursor.fetchall()
            # Создаем окно для отображения данных
            result_window = tk.Toplevel(root)
            result_window.title("Средние оценки за предмет")
            # Создаем таблицу для отображения данных
            columns = ("название предмета", "Средняя оценка")
            tree = ttk.Treeview(result_window, columns=columns, show='headings')
            # Устанавливаем заголовки для колонок
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center")
            # Добавляем данные в таблицу
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            # Размещаем таблицу на экране
            tree.pack(expand=True, fill='both')
            # Добавляем скроллбар
            scrollbar = ttk.Scrollbar(result_window, command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)
            # Закрываем соединение с базой
            cursor.close()
            cnxn.close()
        except ps.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}")

    def get_teachers_fill_report():
        query = """
            SELECT 
                ev.идентификатор_ведомости, 
                ev.дата_создания_ведомости, 
                p.название_предмета,
                pr.фамилия, 
                pr.имя, 
                pr.отчество
            FROM 
                Экзаменационная_ведомость ev
            JOIN 
                Предметы p ON ev.идентификатор_предмета = p.идентификатор_предмета
            JOIN 
                Предметы_Преподаватели pp ON p.идентификатор_предмета = pp.идентификатор_предмета
            JOIN 
                Преподаватели pr ON pp.идентификатор_преподавателя = pr.идентификатор_преподавателя
        """
        execute_sql(query)

    def execute_sql(query):
        cnxn = connect_to_db()
        if cnxn is None:
            return
        try:
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            cnxn.close()
            if not rows:
                messagebox.showinfo("Результат", "Данные не найдены.")
                return
            result_window = tk.Toplevel(root)
            result_window.title("Отчет по преподавателям и ведомостям")
            columns = (
                'идентификатор_ведомости', 'дата_создания_ведомости', 'название_предмета', 'фамилия', 'имя', 'отчество'
            )
            tree = ttk.Treeview(result_window, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            tree.pack(expand=True, fill='both')
            scrollbar = ttk.Scrollbar(result_window, command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}")

    def get_subjects_with_teachers():
        # Используем тройное соединение, чтобы связать предметы с преподавателями через связующую таблицу
        query = """
        SELECT 
            p.название_предмета, 
            pr.фамилия, 
            pr.имя, 
            pr.отчество
        FROM 
            Предметы_Преподаватели pp
        JOIN 
            Предметы p ON pp.идентификатор_предмета = p.идентификатор_предмета
        JOIN 
            Преподаватели pr ON pp.идентификатор_преподавателя = pr.идентификатор_преподавателя
        """
        execute_sql_q(query)

    def execute_sql_q(query):
        try:
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result_window = tk.Toplevel(root)
            result_window.title("Список предметов с преподавателями")
            columns = ("название предмета", "фамилия", "имя", "отчество")
            tree = ttk.Treeview(result_window, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center")
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            tree.pack(expand=True, fill='both')
            scrollbar = ttk.Scrollbar(result_window, command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)
            cursor.close()
            cnxn.close()
        except ps.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}")

    def get_students_with_specific_grade_and_subject():
        # Запрашиваем у пользователя оценку
        grade = simpledialog.askstring("Получение данных", "Введите оценку для поиска студентов:")
        if grade and grade.isdigit():  # Проверяем, что введено числовое значение
            grade = int(grade)  # Преобразуем строку в число
            query = """
            SELECT s.фамилия, s.имя, s.отчество, p.название_предмета, o.оценка
            FROM Студенты s
            JOIN Оценки o ON s.идентификатор_студента = o.идентификатор_студента
            JOIN Предметы p ON o.идентификатор_предмета = p.идентификатор_предмета
            WHERE o.оценка = %s
            """
            execute_sql_pod(query, grade)
        else:
            messagebox.showinfo("Информация", "Необходимо ввести числовую оценку.")

    def execute_sql_pod(query, param):
        try:
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            cursor.execute(query, param)
            rows = cursor.fetchall()
            result_window = tk.Toplevel(root)
            result_window.title("Студенты с оценкой " + str(param))
            columns = ("фамилия", "имя", "отчество", "название предмета", "оценка")
            tree = ttk.Treeview(result_window, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center")
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            tree.pack(expand=True, fill='both')
            scrollbar = ttk.Scrollbar(result_window, command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)
            cursor.close()
            cnxn.close()
        except ps.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}")

    def get_subjects_without_records():
        # SQL запрос для получения списка предметов, по которым не составлены ведомости
        query = """
        SELECT DISTINCT p.идентификатор_предмета, p.название_предмета
        FROM Предметы p
        WHERE NOT EXISTS (
            SELECT * FROM Экзаменационная_ведомость ev
            WHERE ev.идентификатор_предмета = p.идентификатор_предмета
        )
        """
        execute_sql_prov(query)

    def execute_sql_prov(query):
        try:
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result_window = tk.Toplevel(root)
            result_window.title("Предметы без ведомостей")
            columns = ('идентификатор предмета', 'название предмета')
            tree = ttk.Treeview(result_window, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center")
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            tree.pack(expand=True, fill='both')
            scrollbar = ttk.Scrollbar(result_window, command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)
            cursor.close()
            cnxn.close()
        except ps.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}")

    def get_students_with_low_grades():
        # SQL запрос для выбора студентов с оценками 2 или 3
        query = """
        SELECT s.фамилия, s.имя, s.отчество, p.название_предмета, o.оценка
        FROM Студенты s
        JOIN Оценки o ON s.идентификатор_студента = o.идентификатор_студента
        JOIN Предметы p ON o.идентификатор_предмета = p.идентификатор_предмета
        WHERE o.оценка IN (2, 3)
        """
        execute_sql_query_p(query)

    def execute_sql_query_p(query):
        try:
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result_window = tk.Toplevel(root)
            result_window.title("Студенты с оценками 2 и 3")
            columns = ('фамилия', 'имя', 'отчество', 'название предмета', 'оценка')
            tree = ttk.Treeview(result_window, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=150)
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            tree.pack(expand=True, fill='both')
            scrollbar = ttk.Scrollbar(result_window, command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)
            cursor.close()
            cnxn.close()
        except ps.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}")

    def get_students_without_exams():
        try:
            # Подключаемся к базе данных
            cnxn = connect_to_db()
            if cnxn is None:
                return  # Если подключение не удалось, выходим из функции
            cursor = cnxn.cursor()
            # Запрос для выбора студентов, не сдававших экзамены
            query = """
            SELECT s.идентификатор_студента, s.фамилия, s.имя, s.отчество
            FROM Студенты s
            WHERE NOT EXISTS (
                SELECT 1
                FROM Оценки o
                WHERE o.идентификатор_студента = s.идентификатор_студента
            )
            """
            # Выполняем запрос
            cursor.execute(query)
            rows = cursor.fetchall()
            # Колонки для отображения в таблице
            columns = ["идентификатор_студента", "фамилия", "имя", "отчество"]
            # Закрываем соединение с базой
            cursor.close()
            cnxn.close()
            # Отображаем данные в новом окне
            display_data_in_window(rows, columns)
        except ps.Error as e:
            print("Ошибка при выполнении запроса: ", e)

    def display_data_in_window(rows, columns):
        # Создание нового окна
        new_window = tk.Tk()
        new_window.title("Студенты без экзаменов")
        # Создание таблицы
        tree = ttk.Treeview(new_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(side='left', fill='both', expand=True)
        # Заполнение таблицы данными
        for row in rows:
            cleaned_row = tuple(str(item).strip("'\"") for item in row)
            tree.insert('', 'end', values=cleaned_row)
        scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        new_window.mainloop()

    def display_subjects_with_multiple_teachers():
        query = """
        SELECT 
            p.название_предмета, 
            COUNT(pp.идентификатор_преподавателя) AS Количество_преподавателей
        FROM 
            Предметы p
        JOIN 
            Предметы_Преподаватели pp ON p.идентификатор_предмета = pp.идентификатор_предмета
        GROUP BY 
            p.название_предмета
        HAVING 
            COUNT(pp.идентификатор_преподавателя) > 1
        """
        try:
            cnxn = connect_to_db()
            if cnxn is None:
                return  # Если подключение не удалось, выходим из функции
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            cnxn.close()
            # Отображаем данные
            new_window = tk.Tk()
            new_window.title("Предметы с несколькими преподавателями")
            columns = ("название предмета", "Количество преподавателей")
            tree = ttk.Treeview(new_window, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center")
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            tree.pack(expand=True, fill='both')
            scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)
            new_window.mainloop()
        except ps.Error as e:
            print("Ошибка при выполнении запроса: ", e)

    def display_subjects_and_exam_dates():
        query = """
        SELECT 
            p.название_предмета,
            e.дата_создания_ведомости
        FROM 
            Предметы p
        JOIN 
            Экзаменационная_ведомость e ON p.идентификатор_предмета = e.идентификатор_предмета
        ORDER BY 
            e.дата_создания_ведомости
        """
        try:
            cnxn = connect_to_db()
            if cnxn is None:
                return  # Если подключение не удалось, выходим из функции
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            cnxn.close()
            new_window = tk.Tk()
            new_window.title("Предметы и даты экзаменов")
            columns = ("название предмета", "дата экзамена")
            tree = ttk.Treeview(new_window, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center")
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            tree.pack(expand=True, fill='both')
            scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)
            new_window.mainloop()
        except ps.Error as e:
            print("Ошибка при выполнении запроса: ", e)

    def display_students_by_abs():
        # Запрашиваем название группы у пользователя
        group = simpledialog.askstring("Input", "Введите название группы:")
        if not group:
            messagebox.showinfo("Ошибка", "Необходимо ввести название группы.")
            return
        query = """
        SELECT 
   	 фамилия, 
            имя, 
            отчество
        FROM 
            Студенты
        WHERE 
            группа = %s
        ORDER BY 
            фамилия ASC
        """
        try:
            cnxn = connect_to_db()
            if cnxn is None:
                messagebox.showerror("Ошибка подключения", "Не удалось подключиться к базе данных.")
                return  # Если подключение не удалось, выходим из функции
            cursor = cnxn.cursor()
            cursor.execute(query, (group,))
            rows = cursor.fetchall()
            new_window = tk.Tk()
            new_window.title("Студенты группы " + group)
            columns = ("фамилия", "имя", "отчество")
            tree = ttk.Treeview(new_window, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center")
            for row in rows:
                cleaned_row = tuple(str(item).strip("'\"") for item in row)
                tree.insert('', 'end', values=cleaned_row)
            tree.pack(expand=True, fill='both')
            scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)
            new_window.mainloop()
            cursor.close()
            cnxn.close()
        except ps.Error as e:
            messagebox.showerror("Ошибка выполнения запроса", f"Ошибка при выполнении запроса: {e}")

    buttons = [
        ("Экзаменационная ведомость определенной группы", get_exam_record_details),
        ("Список группы", get_students_by_group),
        ("Средняя оценка", get_average_grade_for_subject),
        ("Отчет о ведомости", get_teachers_fill_report),
        ("Отчет о предметах", get_subjects_with_teachers),
        ("Оценки студентов", get_students_with_specific_grade_and_subject),
        ("Предметы без оценок", get_subjects_without_records),
        ("Плохие оценки студентов", get_students_with_low_grades),
        ("Студенты, не сдавшие экзамен", get_students_without_exams),
        ("Предметы, которые ведут несколько преподавателей", display_subjects_with_multiple_teachers),
        ("дата проведения экзамена", display_subjects_and_exam_dates),
        ("Сортировка студентов по фамилии", display_students_by_abs)
    ]
    for text, command in buttons:
        tk.Button(queries_window, text=text, command=command).pack(fill='x', padx=10, pady=5)
    back_button = tk.Button(queries_window, text="Назад", command=queries_window.destroy)
    back_button.pack(fill='x', padx=10, pady=5)


def show_main_menu():
    # Функция для отображения главного меню после входа
    login_frame.pack_forget()
    main_menu_frame.pack()


# Глобальные переменные для хранения имени пользователя и пароля
global_username = None
global_password = None


# Функция входа в систему
def login():
    global global_username, global_password
    username = entry_username.get()
    password = entry_password.get()
    try:
        global_username = username  # Сохраняем имя пользователя
        global_password = password  # Сохраняем пароль
        cnxn = ps.connect(
            host='localhost',
            user= global_username,
            password=global_password,
            database='postgres'
        )

        messagebox.showinfo("Успех", "Вы успешно вошли в систему!")
        cnxn.close()
        show_main_menu()
    except ps.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка входа в систему: {e}")


def connect_to_db():
    global global_username, global_password
    try:

        return ps.connect(
            host='localhost',
            user= global_username,
            password= global_password,
            database='postgres'
        )
    except Exception as e:
        messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к базе данных: {e}")
        return None


# Главное окно
root = tk.Tk()
root.title("Система входа в SQL")
# Фрейм для входа пользователя
login_frame = tk.Frame(root)
login_frame.pack(pady=20)
# Виджеты для входа в систему
label_username = tk.Label(login_frame, text="имя пользователя")
label_username.pack()
entry_username = tk.Entry(login_frame)
entry_username.pack()
label_password = tk.Label(login_frame, text="Пароль")
label_password.pack()
entry_password = tk.Entry(login_frame, show="*")
entry_password.pack()
button_login = tk.Button(login_frame, text="Войти", command=login)
button_login.pack()
main_menu_frame = tk.Frame(root)
# Кнопки для главного меню
button_queries = tk.Button(main_menu_frame, text="Запросы", command=execute_queries)
button_queries.pack(fill='x', padx=10, pady=5)
button_students = tk.Button(main_menu_frame, text="Таблица 'Студенты'", command=manage_students)
button_students.pack(fill='x', padx=10, pady=5)
button_teachers = tk.Button(main_menu_frame, text="Таблица 'Преподаватели'", command=manage_teachers)
button_teachers.pack(fill='x', padx=10, pady=5)
button_subjects = tk.Button(main_menu_frame, text="Таблица 'Предметы'", command=manage_subjects)
button_subjects.pack(fill='x', padx=10, pady=5)
button_grades = tk.Button(main_menu_frame, text="Таблица 'Оценки'", command=manage_grades)
button_grades.pack(fill='x', padx=10, pady=5)
button_exam_records = tk.Button(main_menu_frame, text="Таблица 'Экзаменационная ведомость'",
                                command=manage_exam_records)
button_exam_records.pack(fill='x', padx=10, pady=5)
button_pp = tk.Button(main_menu_frame, text="Таблица 'Предметы_Преподаватели'", command=manage_subjects_teachers)
button_pp.pack(fill='x', padx=10, pady=5)
# Запуск главного цикла Tkinter
root.mainloop()
