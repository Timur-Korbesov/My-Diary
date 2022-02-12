import datetime
import sys
import sqlite3
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDateEdit, QDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM profile_inf").fetchall()
        con.close()

        if len(result) != 0:
            self.menu()
        else:
            self.stud_profile()

    def menu(self):
        uic.loadUi('menu.ui', self)
        self.setWindowTitle('Мой Дневник')
        self.grades_analyze_btn.clicked.connect(self.analyze_grades)
        self.student_profile.clicked.connect(self.stud_profile)
        self.settings_dnevnik.clicked.connect(self.help)
        self.grades_btn.clicked.connect(self.all_grades)

    def analyze_grades(self):
        uic.loadUi('graph_selection.ui', self)
        self.setWindowTitle("Выбор графика")

        self.return_2.clicked.connect(self.menu)

        self.positiv_graph.clicked.connect(self.created_pos_graph)
        self.negative_graph.clicked.connect(self.created_neg_graph)

    def created_pos_graph(self):
        uic.loadUi('positive_graph.ui', self)

        self.setWindowTitle("Интервал для положительного графика")

        self.result_edit.hide()

        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()
        count = cur.execute("SELECT item FROM list_items").fetchall()
        con.close()

        for i in range(len(count)):
            count[i] = count[i][0]

        self.items_list.addItems(count)

        self.return_2.clicked.connect(self.analyze_grades)

        self.result_graph.clicked.connect(self.output_pos_graph)

    def created_neg_graph(self):
        uic.loadUi('negative_graph.ui', self)

        self.setWindowTitle("Интервал для отрицательного графика")

        self.result_edit.hide()

        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()
        count = cur.execute("SELECT item FROM list_items").fetchall()
        con.close()

        for i in range(len(count)):
            count[i] = count[i][0]

        self.items_list.addItems(count)

        self.return_2.clicked.connect(self.analyze_grades)

        self.result_graph.clicked.connect(self.output_neg_graph)

    def output_pos_graph(self):
        start_day, start_month, start_year = map(int, self.start_date.text().split("."))
        end_day, end_month, end_year = map(int, self.end_date.text().split("."))

        self.result_edit.hide()
        self.result_edit.setEnabled(False)

        start_date = dt.date(start_year, start_month, start_day)
        end_date = dt.date(end_year, end_month, end_day)

        self.positiv_x = []
        self.positiv_y4 = []
        self.positiv_y5 = []

        if start_date > end_date:
            self.result_edit.show()
            return
        elif (end_date - start_date).days > 7:
            self.result_edit.setText("Вы выбрали слишком большой интервал.")
            self.result_edit.show()
            return
        else:
            all_date = start_date
            con = sqlite3.connect("sql_table/profile_table.db")
            cur = con.cursor()
            while (end_date - all_date).days != 0:
                x_year, x_month, x_day = str(all_date).split("-")
                self.positiv_x.append(".".join([x_day, x_month]))
                self.positiv_y4.append(len(cur.execute(
                    f"SELECT items, gradess FROM all_grades WHERE data = '{'.'.join([x_day, x_month, x_year])}'"
                    f" AND gradess = 4 AND items = (SELECT id FROM list_items WHERE item = '{self.items_list.currentText()}')").fetchall()))
                self.positiv_y5.append(len(cur.execute(
                    f"SELECT items, gradess FROM all_grades WHERE data = '{'.'.join([x_day, x_month, x_year])}'"
                    f" AND gradess = 5 AND items = (SELECT id FROM list_items WHERE item = '{self.items_list.currentText()}')").fetchall()))
                all_date += datetime.timedelta(days=1)
            x_year, x_month, x_day = str(all_date).split("-")
            self.positiv_x.append(".".join([x_day, x_month]))
            self.positiv_y4.append(len(cur.execute(
                f"SELECT items, gradess FROM all_grades WHERE data = '{'.'.join([x_day, x_month, x_year])}'"
                f" AND gradess = 4 AND items = (SELECT id FROM list_items WHERE item = '{self.items_list.currentText()}')").fetchall()))
            self.positiv_y5.append(len(cur.execute(
                f"SELECT items, gradess FROM all_grades WHERE data = '{'.'.join([x_day, x_month, x_year])}'"
                f" AND gradess = 5 AND items = (SELECT id FROM list_items WHERE item = '{self.items_list.currentText()}')").fetchall()))
            con.close()

        y_4 = self.positiv_y4
        y_5 = self.positiv_y5

        width = 0.4

        x_indexes = np.arange(len(self.positiv_x))
        plt.xticks(x_indexes, self.positiv_x)
        plt.xlabel("Дата получения оценки (день.месяц)")
        plt.title("График положительных оценок")
        plt.ylabel("Количество оценок")
        if not any(y_5):
            plt.bar(x_indexes, y_4, label="4", width=width)
        elif not any(y_4):
            plt.bar(x_indexes, y_5, label="5", width=width)
        else:
            plt.bar(x_indexes - (width / 2), y_4, label="4", width=width)
            plt.bar(x_indexes + (width / 2), y_5, label="5", width=width)
        plt.legend()
        plt.show()

    def output_neg_graph(self):
        start_day, start_month, start_year = map(int, self.start_date.text().split("."))
        end_day, end_month, end_year = map(int, self.end_date.text().split("."))

        self.result_edit.hide()
        self.result_edit.setEnabled(False)

        start_date = dt.date(start_year, start_month, start_day)
        end_date = dt.date(end_year, end_month, end_day)

        self.negativ_x = []
        self.negativ_y2 = []
        self.negativ_y3 = []

        if start_date > end_date:
            self.result_edit.show()
            return
        elif (end_date - start_date).days > 6:
            self.result_edit.setText("Вы выбрали слишком большой интервал.")
            self.result_edit.show()
            return
        else:

            all_date = start_date
            con = sqlite3.connect("sql_table/profile_table.db")
            cur = con.cursor()
            while (end_date - all_date).days != 0:
                x_year, x_month, x_day = str(all_date).split("-")
                self.negativ_x.append(".".join([x_day, x_month]))
                self.negativ_y2.append(len(cur.execute(f"SELECT items, gradess FROM all_grades WHERE data ="
                                                       f" '{'.'.join([x_day, x_month, x_year])}'"
                                                       f" AND gradess = 2 AND items = (SELECT id FROM list_items WHERE item = '{self.items_list.currentText()}')").fetchall()))
                self.negativ_y3.append(len(cur.execute(f"SELECT items, gradess FROM all_grades WHERE data ="
                                                       f" '{'.'.join([x_day, x_month, x_year])}'"
                                                       f" AND gradess = 3 AND items = (SELECT id FROM list_items WHERE item = '{self.items_list.currentText()}')").fetchall()))
                all_date += datetime.timedelta(days=1)
            x_year, x_month, x_day = str(all_date).split("-")
            self.negativ_x.append(".".join([x_day, x_month]))
            self.negativ_y2.append(len(cur.execute(f"SELECT items, gradess FROM all_grades WHERE data ="
                                                   f" '{'.'.join([x_day, x_month, x_year])}'"
                                                   f" AND gradess = 2 AND items = (SELECT id FROM list_items WHERE item = '{self.items_list.currentText()}')").fetchall()))
            self.negativ_y3.append(len(cur.execute(f"SELECT items, gradess FROM all_grades WHERE data ="
                                                   f" '{'.'.join([x_day, x_month, x_year])}'"
                                                   f" AND gradess = 3 AND items = (SELECT id FROM list_items WHERE item = '{self.items_list.currentText()}')").fetchall()))
            con.close()


        y_2 = self.negativ_y2
        y_3 = self.negativ_y3

        width = 0.4

        x_indexes = np.arange(len(self.negativ_x))
        plt.xticks(x_indexes, self.negativ_x)
        plt.xlabel("Оценки")
        plt.title("График отрицательных оценок")
        plt.ylabel("Количество оценок")

        if not any(y_3):
            plt.bar(x_indexes, y_2, label="2", width=width)
        elif not any(y_2):
            plt.bar(x_indexes, y_3, label="3", width=width)
        else:
            plt.bar(x_indexes - (width / 2), y_2, label="2", width=width)
            plt.bar(x_indexes + (width / 2), y_3, label="3", width=width)

        plt.legend()
        plt.show()

    def stud_profile(self):
        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()
        result = cur.execute("""SELECT name FROM profile_inf""").fetchall()
        con.close()

        if not result:
            uic.loadUi('profile.ui', self)
            self.setWindowTitle('Создание профиля')
            self.return_2.hide()

            self.return_2.clicked.connect(self.menu)

            self.save_btn.clicked.connect(self.created_profile)
        else:
            uic.loadUi('settings_profiles.ui', self)
            self.setWindowTitle('Настройки профиля')

            self.my_profile.clicked.connect(self.edit_profile)

            self.my_profile_edit.clicked.connect(self.edit_my_profile)

            self.return_2.clicked.connect(self.menu)

    def created_profile(self):
        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()

        inf1, inf2, inf3, inf4 = self.surname_student.text(), self.name_student.text(), self.date_birthday.text(), \
                                 self.class_number.currentText()

        cur.execute(""f"INSERT INTO profile_inf VALUES ('{inf1}', '{inf2}', '{inf3}', {inf4})""").fetchall()
        con.commit()

        n_class = cur.execute("SELECT number_class FROM profile_inf").fetchall()[0][0]
        con.close()

        file = open("new_class.txt", "w+", encoding="utf-8")
        file.write(str(n_class))
        file.close()

        self.surname_student.setEnabled(False)
        self.name_student.setEnabled(False)
        self.date_birthday.setEnabled(False)
        self.class_number.setEnabled(False)

        self.name_page.setText("Мой профиль")

        self.save_btn.hide()
        self.return_2.show()

    def edit_profile(self):
        uic.loadUi('profile_view.ui', self)
        self.setWindowTitle('Мой профиль')

        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()
        res = cur.execute("""SELECT * FROM profile_inf""").fetchall()
        con.close()

        self.return_2.clicked.connect(self.stud_profile)

        self.surname_student.setText(res[0][0])
        self.surname_student.setEnabled(False)

        self.name_student.setText(res[0][1])
        self.name_student.setEnabled(False)

        self.date_birthday.setText(res[0][2])
        self.date_birthday.setEnabled(False)

        self.class_number.setText(str(res[0][3]))
        self.class_number.setEnabled(False)

    def edit_my_profile(self):
        uic.loadUi('profile_edit.ui', self)

        self.setWindowTitle('Редактирование профиля')

        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()
        res = cur.execute("""SELECT * FROM profile_inf""").fetchall()
        con.close()

        self.return_2.clicked.connect(self.stud_profile)

        self.surname_student.setText(res[0][0])

        self.name_student.setText(res[0][1])

        self.class_number.setCurrentIndex(res[0][3] - 1)

        self.save_btn.clicked.connect(self.save_inf_profile)

    def save_inf_profile(self):
        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()

        inf1, inf2, inf3, inf4 = self.surname_student.text(), self.name_student.text(), self.date_birthday.text(), \
                                 self.class_number.currentText()

        cur.execute(""f"UPDATE profile_inf SET surname = '{inf1}', name = '{inf2}', date_br = '{inf3}',"
                    f"number_class = {int(inf4)}""").fetchall()
        con.commit()
        con.close()

        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()
        class_numb = cur.execute("""SELECT number_class FROM profile_inf""").fetchall()[0][0]
        con.close()

        file = open("new_class.txt", "r", encoding="utf-8")
        text_file = file.readlines()

        if str(class_numb) not in text_file:
            con = sqlite3.connect("sql_table/profile_table.db")
            cur = con.cursor()
            cur.execute("""DELETE from all_grades""").fetchall()
            con.commit()

            cur.execute("""DELETE from list_items""").fetchall()
            con.commit()
            con.close()

        file = open("new_class.txt", "w", encoding="utf-8")
        file.close()

        with open("new_class.txt", "w+", encoding="utf-8") as file:
            file.write(str(class_numb))

        self.surname_student.setEnabled(False)
        self.name_student.setEnabled(False)
        self.date_birthday.setEnabled(False)
        self.class_number.setEnabled(False)

        self.label_5.setText("Мой профиль")

        self.save_btn.hide()

    def all_grades(self):
        uic.loadUi('my_grades.ui', self)
        self.setWindowTitle('Успеваемость')

        self.return_2.clicked.connect(self.menu)
        self.add_grade_btn.clicked.connect(self.new_grade)
        self.add_item_btn.clicked.connect(self.add_new_item)
        self.my_grades_btn.clicked.connect(self.my_grades)
        self.remove_grades_btn.clicked.connect(self.remove_grade)

    def remove_grade(self):
        uic.loadUi("discard_my_grade.ui", self)
        self.setWindowTitle("Удаление оценок")

        self.return_2.clicked.connect(self.all_grades)
        self.discard_grades.clicked.connect(self.grade_remove)

        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()
        count = cur.execute("""SELECT item FROM list_items""").fetchall()
        con.close()

        res = []

        for el in count:
            res.append(el[0])

        self.grade.addItems(['2', '3', '4', '5'])
        self.items_box.addItems(res)
        self.my_calendar.clicked.connect(self.add_date)

        self.error_line.setEnabled(False)
        self.error_line.hide()

        self.result_label.hide()

        self.grade_date.setEnabled(False)

    def grade_remove(self):
        if self.grade_date.text():
            self.error_line.hide()

            calendar_day, calendar_month, calendar_year = map(int, self.grade_date.text().split("."))
            calendar_date = dt.date(calendar_year, calendar_month, calendar_day)

            con = sqlite3.connect("sql_table/profile_table.db")
            cur = con.cursor()
            date_birthday = cur.execute("SELECT date_br FROM profile_inf").fetchall()[0][0]
            con.close()

            day_birthday, month_birthday, year_bithday = map(int, date_birthday.split("."))
            date_birthday = dt.date(year_bithday, month_birthday, day_birthday)

            if calendar_date.weekday() == 6 or calendar_date.strftime("%B") in ["June", "July", "August"] or \
                    calendar_date < date_birthday or (calendar_date.year - date_birthday.year) <= 5:
                self.error_line.setText("Недопустимая дата")
                self.result_label.hide()
                self.error_line.show()
                return

            con = sqlite3.connect("sql_table/profile_table.db")
            cur = con.cursor()
            my_grade = cur.execute(f"SELECT * FROM all_grades WHERE items = (SELECT id FROM list_items WHERE item ="
                                   f" '{self.items_box.currentText()}') AND"
                                   f" gradess = '{self.grade.currentText()}' AND data = '{self.grade_date.text()}'").fetchall()
            con.close()

            if len(my_grade) == 0:
                self.result_label.setText("Оценка не найдена")
                self.result_label.show()
                return

            con = sqlite3.connect("sql_table/profile_table.db")
            cur = con.cursor()

            cur.execute(
                f"DELETE FROM all_grades WHERE items = (SELECT id FROM list_items WHERE item = '{self.items_box.currentText()}') AND gradess = '{self.grade.currentText()}' AND data = '{self.grade_date.text()}'").fetchall()
            con.commit()
            con.close()

            self.result_label.setText("Ваша оценка успешно удалена")
            self.result_label.show()

            self.error_line.hide()

            self.grade_date.setText("")

        else:
            self.result_label.hide()
            self.error_line.setText("Дата не выбрана")
            self.error_line.show()
            return

    def add_new_item(self):
        uic.loadUi('my_items.ui', self)

        self.add_result_label.hide()
        self.add_result_label.setEnabled(False)

        self.setWindowTitle('Добавление предметов')

        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()
        res = cur.execute("SELECT item FROM list_items").fetchall()
        con.close()

        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()
        class_student = cur.execute("SELECT number_class FROM profile_inf").fetchall()
        con.close()

        self.all_lessons = ["Физкультура", "Немецкий язык", "Английский язык", "Испанский язык",
                            "Родной язык", "Родная литература", "Технология", "Русский язык", "Литература", "Музыка",
                            "Пение"]

        if 1 <= class_student[0][0] <= 6:
            self.all_lessons.extend(["Математика", "ИЗО"])
            if class_student[0][0] == 6:
                self.all_lessons.append("Обществознание")
            if class_student[0][0] >= 5:
                self.all_lessons.extend(["География", "История", "Биология", "Информатика"])
        else:
            self.all_lessons.extend(["Алгебра", "Геометрия", "Обществознание", "География", "История",
                                     "Биология", "ОБЖ", "Физика", "Химия", "Черчение", "Экономика", "Астрономия", "Информатика"])

        self.all_lessons.sort()

        self.lessons_box.addItems(self.all_lessons)

        all_items = []

        for i in res:
            all_items.append(i[0])

        self.list_all_items.addItems(all_items)

        self.add_item_btn.clicked.connect(self.save_item)
        self.return_2.clicked.connect(self.all_grades)

    def save_item(self):
        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()
        res = cur.execute("SELECT item FROM list_items WHERE item = ?", (self.lessons_box.currentText(),)).fetchall()
        con.close()

        if not res:
            con = sqlite3.connect("sql_table/profile_table.db")
            cur = con.cursor()
            cur.execute("""INSERT INTO list_items(item) VALUES(?)""", (self.lessons_box.currentText(),)).fetchall()
            con.commit()
            con.close()

            self.list_all_items.addItem(self.lessons_box.currentText())
            self.add_result_label.setText("Предмет успешно добавлен")
            self.add_result_label.show()
            return
        else:
            self.add_result_label.setText("Предмет уже есть в списке")
            self.add_result_label.show()
            return

    def new_grade(self):
        uic.loadUi('add_new_grade.ui', self)
        self.setWindowTitle('Добавление оценок')

        self.error_line.setEnabled(False)
        self.error_line.hide()

        self.result_label.hide()

        self.grade_date.setEnabled(False)
        self.return_2.clicked.connect(self.all_grades)

        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()
        count = cur.execute("""SELECT item FROM list_items""").fetchall()
        con.close()

        res = []

        for el in count:
            res.append(el[0])

        self.grade.addItems(['2', '3', '4', '5'])
        self.items_box.addItems(res)
        self.my_calendar.clicked.connect(self.add_date)
        self.add_grades.clicked.connect(self.add_new_grade)

    def add_date(self):
        date = self.my_calendar.selectedDate().toString("dd-MM-yyyy")
        date = date.split("-")

        self.grade_date.setText(".".join(date))

    def add_new_grade(self):
        if self.grade_date.text():
            self.error_line.hide()

            calendar_day, calendar_month, calendar_year = map(int, self.grade_date.text().split("."))
            calendar_date = dt.date(calendar_year, calendar_month, calendar_day)

            con = sqlite3.connect("sql_table/profile_table.db")
            cur = con.cursor()
            date_birthday = cur.execute("SELECT date_br FROM profile_inf").fetchall()[0][0]
            con.close()

            day_birthday, month_birthday, year_bithday = map(int, date_birthday.split("."))
            date_birthday = dt.date(year_bithday, month_birthday, day_birthday)

            if calendar_date.weekday() == 6 or calendar_date.strftime("%B") in ["June", "July", "August"] or \
                    calendar_date < date_birthday or (calendar_date.year - date_birthday.year) <= 5:
                self.error_line.setText("Недопустимая дата")
                self.result_label.hide()
                self.error_line.show()
                return

            con = sqlite3.connect("sql_table/profile_table.db")
            cur = con.cursor()

            cur.execute(
                f"INSERT INTO all_grades VALUES((SELECT id FROM list_items WHERE item = '{self.items_box.currentText()}'), ?, ?)",
                (self.grade.currentText(), self.grade_date.text())).fetchall()
            con.commit()
            con.close()

            self.result_label.show()

            self.error_line.hide()

            self.grade_date.setText("")

        else:
            self.result_label.hide()
            self.error_line.setText("Дата не выбрана")
            self.error_line.show()
            return

    def my_grades(self):
        uic.loadUi('view_my_grades.ui', self)
        self.setWindowTitle('Мои оценки')

        con = sqlite3.connect("sql_table/profile_table.db")
        cur = con.cursor()
        count = cur.execute("SELECT item FROM list_items").fetchall()
        con.close()

        for i in range(len(count)):
            count[i] = count[i][0]

        self.items_list.addItems(count)

        self.return_2.clicked.connect(self.all_grades)

        self.result_edit.hide()
        self.result_edit.setEnabled(False)

        self.view_grades_btn.clicked.connect(self.view_my_grades)

    def view_my_grades(self):
        self.result_edit.hide()

        self.interval_grades.clear()
        s_date = self.start_date.text().split(".")
        e_date = self.end_date.text().split(".")

        start = dt.date(int(s_date[2]), int(s_date[1]), int(s_date[0]))
        end = dt.date(int(e_date[2]), int(e_date[1]), int(e_date[0]))

        if start > end:
            self.result_edit.show()
        else:
            con = sqlite3.connect("sql_table/profile_table.db")
            cur = con.cursor()
            count = cur.execute(
                f"SELECT * FROM all_grades WHERE items = (SELECT id FROM list_items WHERE item = '{self.items_list.currentText()}')").fetchall()
            con.close()

            grades_and_data = []

            con = sqlite3.connect("sql_table/profile_table.db")
            cur = con.cursor()
            for date in count:
                day, month, year = date[2].split(".")
                data_now = dt.date(int(year), int(month), int(day))
                grade = cur.execute(f"SELECT item FROM list_items WHERE id = {date[0]}").fetchall()
                if start <= data_now <= end:
                    grades_and_data.append(
                        f"{grade[0][0]} - {date[1]}  {str(day) + '.' + str(month) + '.' + str(year)}")

            self.interval_grades.addItem("Предмет - Оценка   Дата\n")

            self.interval_grades.addItems(grades_and_data)

    def help(self):
        uic.loadUi("help.ui", self)

        self.setWindowTitle("Помощь")
        self.help_text.setEnabled(False)

        self.return_2.clicked.connect(self.menu)


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
