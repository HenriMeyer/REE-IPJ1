from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import time
import sys

def main():
    # param for window
    screen = app.primaryScreen()
    window_x = 0
    window_y = 0
    window_width = 500
    window_height = 500
    
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("Softwaretitel")
    label = QLabel('Hallo, PyQt!', parent=window)
    label.move(50, 50)
    window.setGeometry(window_x, window_y, window_width, window_height)
    window.show()
    app.exec_()
    time.sleep(1)
    window.close()
    

# Nur ausführen, wenn das Skript direkt aufgerufen wird
if __name__ == "__main__":
    main()
