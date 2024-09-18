import math
import sys
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog, QAction, QMenu, QMessageBox, QDialog, \
    QVBoxLayout, QLineEdit, QPushButton
from PySide2.QtGui import QPixmap, QContextMenuEvent
from PySide2.QtCore import Qt


class AnimalDialog(QDialog):
    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle("Введите название животного")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.label = QLabel("Название животного:")
        layout.addWidget(self.label)

        self.animal_name_input = QLineEdit()
        layout.addWidget(self.animal_name_input)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_animal)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_animal(self):
        animal_name = self.animal_name_input.text()
        self.parent().dict_of_animal[animal_name] = self.parent().coords
        if animal_name:
            # Здесь можно обработать сохранение, например, вывести сообщение
            QMessageBox.information(self, "Информация", f"Животное '{animal_name}' сохранено!")
            self.accept()  # Закрывает диалог
        else:
            QMessageBox.warning(self, "Предупреждение", "Введите название животного.")


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")

        # Создаем виджет для отображения изображения
        self.label = QLabel(self)
        self.setCentralWidget(self.label)

        # Загружаем изображение
        self.load_image()

        # Устанавливаем размер окна
        self.resize(800, 600)

        self.dict_of_animal = dict()

        self.coords = None

        self.add_animal = QAction(self)
        self.add_animal.setText('Добавить животное')
        self.add_animal.triggered.connect(self.add_animal_func)

        self.show_animal = QAction(self)
        self.show_animal.setText('Показать всех животных')
        self.show_animal.triggered.connect(self.show_animal_func)

        self.show_animal_close = QAction(self)
        self.show_animal_close.setText('Показать животных рядом')
        self.show_animal_close.triggered.connect(self.show_animal_close_func)

        self.menu = QMenu(self)
        self.menu.addAction(self.add_animal)
        self.menu.addAction(self.show_animal)
        self.menu.addAction(self.show_animal_close)

    def is_close1(self, coords1, coords2):
        if ((coords1[0] - coords2[0]) ** 2 + (coords1[1] - coords2[1]) ** 2) ** (1/2) < 20:
            return True
        else:
            return False

    def is_close(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2

        # Вычисление расстояния
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # Проверка условия
        return distance < 100

    def show_animal_close_func(self):
        new_dict = dict()
        for key, value in self.dict_of_animal.items():
            if self.is_close(self.coords, value):
                new_dict[key] = value
        mess = 'соседей нет'
        if len(new_dict) != 0:
            mess = str(new_dict)
        msg = QMessageBox()
        msg.setText(mess)
        if msg.exec_() == QDialog.Accepted:
            pass

    def show_animal_func(self):
        msg = QMessageBox()
        msg.setText(str(self.dict_of_animal))
        if msg.exec_() == QDialog.Accepted:
            pass

    def add_animal_func(self):
        msg = AnimalDialog(self)
        if msg.exec_() == QDialog.Accepted:
            pass

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        self.coords = (event.globalPos().x(), event.globalPos().y())
        self.menu.exec_(event.globalPos())

    def load_image(self):
        # Открываем диалог выбора файла
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)",
                                                   options=options)

        if file_path:
            # Загружаем выбранное изображение
            self.pixmap = QPixmap(file_path)
            self.label.setPixmap(self.pixmap)
            self.label.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Получаем координаты клика мыши
            x = event.x()
            y = event.y()
            print(f"Координаты клика: ({x}, {y})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())
