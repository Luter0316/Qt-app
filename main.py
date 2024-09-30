# В файле data_painter.txt содержится информация о самых известных художниках. Формат файла следующий: в каждых семи
# строках - индекс, имя, годы жизни, стиль (или стили через запятую), страна, ссылка на страницу в википедии,
# количество картин. В главном окне приложения отобразите таблицу со следующей информацией о каждом художнике: имя,
# сколько лет прожил, страна, количество картин. В главном меню приложения должны быть пункты для выполнения
# следующих действий: выбор списка художников по стране, веку, стилю (списки отображаются в главном окне приложения),
# возможность отбора по нескольким параметрам одновременно, реализация гиперссылки на страницу в википедии.
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QMainWindow, QVBoxLayout, QDialog, \
    QDialogButtonBox, QComboBox, QFormLayout, QLabel, QWidget

from painter import createListOfPainters

rawData = createListOfPainters()


class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Выберите фильтры")
        self.setFixedSize(200, 120)

        layout = QFormLayout()

        country = QLabel("Страна: ")
        self.country_field = QComboBox()
        self.country_field.addItems(rawData[1])
        self.country_field.setCurrentIndex(-1)
        layout.addRow(country, self.country_field)

        time = QLabel("Век: ")
        self.time_field = QComboBox()
        self.time_field.addItems(rawData[2])
        self.time_field.setCurrentIndex(-1)
        layout.addRow(time, self.time_field)

        style = QLabel("Стиль: ")
        self.style_field = QComboBox()
        self.style_field.addItems(rawData[3])
        self.style_field.setCurrentIndex(-1)
        layout.addRow(style, self.style_field)

        buttonBox = QDialogButtonBox()
        buttonBox.addButton("Очистить", QDialogButtonBox.ButtonRole.RejectRole)
        buttonBox.addButton("Применить", QDialogButtonBox.ButtonRole.AcceptRole)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addRow(buttonBox)

        self.setLayout(layout)


class Window(QMainWindow):
    def creatingTable(self, lst):
        table = QTableWidget()
        table.setRowCount(len(lst))

        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['Имя', 'Годы жизни', 'Страна', 'Количество картин'])

        for i in range(len(lst)):
            table.setCellWidget(i, 0,
                                QLabel(" <a href=" + lst[i].getLink() + ">" + lst[i].getName() + "</a>",
                                       openExternalLinks=True))
            table.setItem(i, 1, QTableWidgetItem(lst[i].getAge()))
            table.setItem(i, 2, QTableWidgetItem(lst[i].getCountry()))
            table.setItem(i, 3, QTableWidgetItem(lst[i].getPaintCount()))

        # table.setColumnCount(6)
        # table.setHorizontalHeaderLabels(['Имя', 'Годы жизни', 'Стиль', 'Страна', 'Ссылка', 'Количество картин'])
        # for i in range(len(lst)):
        #     table.setItem(i, 0, QTableWidgetItem(lst[i].getName()))
        #     table.setItem(i, 1, QTableWidgetItem(lst[i].getYearsOfLife()))
        #     table.setItem(i, 2, QTableWidgetItem(lst[i].getStyle()))
        #     table.setItem(i, 3, QTableWidgetItem(lst[i].getCountry()))
        #     table.setCellWidget(i, 4,
        #                         QLabel(" <a href=" + lst[i].getLink() + ">" + lst[i].getLink() + "</a>",
        #                                openExternalLinks=True))
        #     table.setItem(i, 5, QTableWidgetItem(lst[i].getPaintCount()))

        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        return table

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список художников")
        self.setFixedSize(540, 700)

        self.CustomDialog = None

        self.dataLst = rawData[0]

        self.table = self.creatingTable(self.dataLst)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        container = QWidget()
        container.setLayout(self.layout)

        self.customMenu()
        self.setCentralWidget(container)

    def customMenu(self):
        menuBar = self.menuBar()
        menuBar.resize(100, 20)
        menuDialogs = menuBar.addMenu("Фильтр")
        actionLabel = menuDialogs.addAction("Отфильтровать")
        actionLabel.triggered.connect(self.filter)

    @Slot()
    def filter(self):  # Фильтрация по выбранным параметрам (с сохранением экземляра ссылки)
        if self.CustomDialog is None:
            # Если ссылка отсутствует
            self.CustomDialog = CustomDialog()
            self.filtering()
        else:
            # Если ссылка существует
            self.filtering()

    # Фильтрация
    def filtering(self):
        if self.CustomDialog.exec():
            filteredLst = self.dataLst.copy()
            countryCB = self.CustomDialog.country_field.currentText()
            timeCB = self.CustomDialog.time_field.currentText()
            styleCB = self.CustomDialog.style_field.currentText()

            if countryCB != "":
                for p in self.dataLst:
                    if not (countryCB in p.getCountry()):
                        filteredLst.remove(p)
            if timeCB != "":
                for p in self.dataLst:
                    if p in filteredLst:
                        time = p.getYearsOfLife().strip().split('-')
                        bornDate = time[0].strip()
                        deathDate = time[1].strip()
                        if not (((int(bornDate) - 1) // 100 + 1) == int(timeCB) or (
                                (int(deathDate) - 1) // 100 + 1) == int(timeCB)):
                            filteredLst.remove(p)
            if styleCB != "":
                for p in self.dataLst:
                    if p in filteredLst:
                        if not (styleCB in p.getStyle()):
                            filteredLst.remove(p)

            self.table.setRowCount(0)
            self.table = self.creatingTable(filteredLst)
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.table)
            container = QWidget()
            container.setLayout(self.layout)
            self.setCentralWidget(container)
        else:
            self.table.setRowCount(0)
            self.table = self.creatingTable(self.dataLst)
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.table)
            container = QWidget()
            container.setLayout(self.layout)
            self.setCentralWidget(container)
            self.CustomDialog.country_field.setCurrentIndex(-1)
            self.CustomDialog.time_field.setCurrentIndex(-1)
            self.CustomDialog.style_field.setCurrentIndex(-1)


app = QApplication([])
window = Window()
window.show()
app.exec()
