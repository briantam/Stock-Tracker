from app import Application
from tkinter import *

#Driver
def main():
	root = Tk()
	root.title("Stock Tracker")
	root.geometry("340x540")

	app = Application(root)
	root.mainloop()

main()
