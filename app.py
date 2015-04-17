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
		self.entry		= Entry(self, width=22, fg="#757575")
		self.addButton	= Button(self, text="Add", command=self.addStock)

		#Grid the second row of widgets
		self.newLabel.grid(row=1, column=0, sticky=E)
		self.entry.insert(0, "Enter a stock ticker symbol")
		self.entry.bind("<Button-1>", self.resetEntry)
		self.entry.grid(row=1, column=1, columnspan=3)
		self.addButton.grid(row=1, column=4)

		#Add the frame that will display the portfolio widget
		self.pFrame	= LabelFrame(self, text="Your Portfolio", font="Verdana 18", labelanchor=N)
		self.pFrame.grid(columnspan=10, sticky=E+W)
		self.pFrame.columnconfigure(0, weight=1)
		
		self.portfolio 	= Listbox(self.pFrame, height=15, font="Verdana 14")
		self.portfolio["bg"] = "#b8dfd8"
		self.portfolio["cursor"] = "hand2"
		self.portfolio["bd"] = 2
		self.portfolio["selectborderwidth"] = 5
		self.portfolio["activestyle"] = "none"
		self.portfolio.grid(sticky=E+W, columnspan=10)


		self.money = "#1ca64a"
		for i in range(10):
			self.portfolio.insert(END, "Item " + str(i))
			if i%2 == 0:
				self.portfolio.itemconfig(i, fg=self.money, selectbackground="green")
			else:
				self.portfolio.itemconfig(i, fg="red", selectbackground="red")


	def addStock(self):
		print("Adding new stock")

		#Check for nothing or spaces
		if self.entry.get().strip() == "":
			messagebox.showwarning("Invalid Entry", "Enter a ticker symbol with no spaces")
			self.entry.delete(0, END)
		else:
			print("Adding " + self.entry.get().strip())


	def deleteStock(self):
		print("Deleting stock")
		print(self.portfolio.get(ACTIVE))
		
		self.portfolio.delete(ACTIVE)
		self.portfolio.selection_set(ACTIVE)


	#Event handler when user first clicks on the entry field
	def resetEntry(self, event):
		self.entry.delete(0,END)
		self.entry["fg"] = "black"


	def refresh(self):
		print("Refresh!")

		self.portfolio.delete(0, END)
		for i in range(20):
			self.portfolio.insert(END, "Item " + str(i))
			if i%2 == 0:
				self.portfolio.itemconfig(i, fg=self.money, selectbackground="green")
			else:
				self.portfolio.itemconfig(i, fg="red", selectbackground="red")


	def save(self):
		print("Saved!")


	def close(self):
		print("Quitting")
		self.quit()


def main():
	root = Tk()
	root.title("Stock Widget")
	root.geometry("340x510")

	app = Application(root)
	root.mainloop()

main()