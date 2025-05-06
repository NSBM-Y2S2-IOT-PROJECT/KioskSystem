# from PyQt5 import QtWidgets, QtGui, QtCore
# import sys
# import json
# import threading
# import time

# # Global variables
# acceleration_l = False
# acceleration_r = False
# blur = False
# unblur = False
# button_pressed = False  # To track the button press state

# # Initialize counters for left and right scrolling, and blur states
# countL, count_r, b, ub = 0, 0, 0, 0
# lthresh = 10  # Threshold for slow down (adjust as needed)
# centroid_data = None

# def read_centroid_data():
#     global centroid_data
#     while True:
#         try:
#             # Open and read the JSON file
#             with open('../centroid_data.json', 'r') as file:
#                 centroid_data = json.load(file)
#         except Exception as e:
#             print(f"Error reading centroid data: {e}")
#         time.sleep(0)  # Read data every 100ms

# # Start the centroid data reading thread
# input_thread = threading.Thread(target=read_centroid_data, daemon=True)
# input_thread.start()

# class DemoUi(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)

#     def setupUi(self, MainWindow):
#         MainWindow.setWindowTitle("Demo UI with QGraphicsEffect")
#         MainWindow.resize(640, 480)

#         # Central widget
#         self.centralWidget = QtWidgets.QWidget(MainWindow)
#         MainWindow.setCentralWidget(self.centralWidget)

#         # Button
#         self.button = QtWidgets.QPushButton("Click Me", self.centralWidget)
#         self.button.setGeometry(0, 0, 500, 500)

#         # Apply QGraphicsBlurEffect to the button
#         self.graphicsEffect = QtWidgets.QGraphicsBlurEffect()
#         self.graphicsEffect.setBlurRadius(1)  # Adjust the blur radius as needed
#         self.button.setGraphicsEffect(self.graphicsEffect)

#         # Timer for controlling automation
#         self.qtimer = QtCore.QTimer()
#         self.qtimer.setInterval(10)  # Refresh interval for continuous effect
#         self.qtimer.timeout.connect(self.acceleratorThread)
#         self.qtimer.start()

#         # Show the main window
#         MainWindow.show()

#     def acceleratorThread(self):
#         global centroid_data, blur, unblur, button_pressed, countL, count_r, lthresh
#         position = self.button.pos()
#         # Read the centroid data (x, y)
#         print(centroid_data)
#         if centroid_data is not None:
#             x = centroid_data.get('centroid', {}).get('x', 0)
#             y = centroid_data.get('centroid', {}).get('y', 0)
#             self.button.move(x-int(640/2),position.y())

#         # Handling blur effect (based on conditions, you can change logic here)
#         if blur:
#             self.graphicsEffect.setBlurRadius(10)  # Increase the blur intensity
#         if unblur:
#             self.graphicsEffect.setBlurRadius(1)  # Reduce blur effect

#         # Handle button press/unpress
#         if button_pressed:
#             self.button.setText("Pressed")
#         else:
#             self.button.setText("Click Me")

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = DemoUi()
#     sys.exit(app.exec_())
