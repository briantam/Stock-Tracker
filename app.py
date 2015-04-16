from tkinter import *
from tkinter import messagebox

class Application(Frame):
	def __init__(self, root):
		super().__init__(root)
		self.grid()

		#First row of widgets
		self.commandLabel	= Label(self, text="Commands:")
		self.refreshButton 	= Button(self, text="Refresh", command=self.refresh)
		self.saveButton 	= Button(self, text="Save", command=self.save)
		self.quitButton		= Button(self, text="Quit", command=self.close)
		self.deleteButton	= Button(self, text="Delete", command=self.deleteStock)

		#Grid the first row of widgets
		self.commandLabel.grid(row=0, column=0, sticky=E)
		self.refreshButton.grid(row=0, column=1)
		self.saveButton.grid(row=0, column=2)
		self.quitButton.grid(row=0, column=3)
		self.deleteButton.grid(row=0, column=4)

		#Second row of widgets
		self.newLabel	= Label(self, text="New Stock:")
		self.entry		= Entry(self, width=22, fg="gray")
		self.addButton	= Button(self, text="Add", command=self.addStock)

		#Grid the second row of widgets
		self.newLabel.grid(row=1, column=0, sticky=E)
		self.entry.insert(0, "Enter a stock ticker symbol")
		self.entry.bind("<Button-1>", self.resetEntry)
		self.entry.grid(row=1, column=1, columnspan=3)
		self.addButton.grid(row=1, column=4)

		#Add the frame that will display the portfolio
		self.pFrame		= LabelFrame(self, text="Portfolio")
		self.pFrame.grid(columnspan=10, sticky=E+W)
		self.pFrame.columnconfigure(0, weight=1)
		self.portfolio 	= Listbox(self.pFrame)
		self.portfolio.grid(sticky=E+W)


	def addStock(self):
		print("Adding new stock")

		#Check for nothing or spaces
		if self.entry.get().strip() == "":
			messagebox.showwarning("Invalid Entry", "Enter a ticker symbol with no spaces")
			self.entry.delete(0, END)
		else:
			print("Adding " + self.entry.get())


	def deleteStock(self):
		print("Deleting stock")


	#Event handler when user first clicks on the entry field
	def resetEntry(self, event):
		self.entry.delete(0,END)
		self.entry["fg"] = "black"


	def refresh(self):
		print("Refresh!")


	def save(self):
		print("Saved!")


	def close(self):
		print("Quitting")
		self.quit()


def main():
	root = Tk()
	root.title("Stock Widget")
	root.geometry("350x500")

	app = Application(root)
	root.mainloop()

main()