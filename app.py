import urllib.request
from tkinter import *
from tkinter import messagebox
from stock import Stock

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
		self.entry.bind("<Return>", self.addStock)
		self.entry.grid(row=1, column=1, columnspan=3)
		self.addButton.grid(row=1, column=4)

		#Add the frame that will display the portfolio widget
		self.pFrame	= LabelFrame(self, text="Your Portfolio", font="Consolas 18 bold", labelanchor=N)
		self.pFrame.grid(columnspan=10, sticky=E+W)
		self.pFrame.columnconfigure(0, weight=1)
		
		self.portfolio 	= Listbox(self.pFrame, height=15, font="Consolas 16 bold")
		self.portfolio["bg"] = "#D4E9FF"	#"#b8dfd8"
		self.portfolio["cursor"] = "hand2"
		self.portfolio["bd"] = 2
		self.portfolio["selectborderwidth"] = 5
		self.portfolio["activestyle"] = "none"
		self.portfolio.grid(sticky=E+W, columnspan=10)

		#Some less GUI related variables that I will need
		self.money = "#008B00"		#color for stocks that are positive
		self.myPortfolio = []		#stores all the Stock objects in portfolio widget


	#Handles all actions related to adding a new stock to portfolio
	def addStock(self, event = None):
		#Check for nothing or spaces
		if self.entry.get().strip() == "":
			messagebox.showwarning("No Entry", "Enter a valid stock ticker symbol")
			self.entry.delete(0, END)
		else:
			#Make the API request and save the response
			company = self.entry.get().strip().upper()
			query1 = "http://finance.yahoo.com/d/quotes.csv?s="
			query2 = "&f=nl1c1p2"
			response = urllib.request.urlopen(query1 + company + query2)
			data = response.read()
			text = data.decode()

			#Invalid case
			if "N/A" in text:
				messagebox.showerror("Invalid Entry", "This stock does not exist" \
					+ " or data could not be pulled for it.")
			#Valid case
			else:	
				#Create a new stock object with the raw parameters for processing
				newStock = Stock(company, text)
				
				#Check if stock is already in portfolio, else --> add it
				for s in self.myPortfolio:
					if s.getTicker() == newStock.getTicker():
						messagebox.showwarning("Repeated Entry", "This stock is" \
							+ " already in your portfolio")
						self.resetEntry(None)
						return

				self.myPortfolio.append(newStock)
				toDisplay = newStock.stringify()
				
				#Add to portfolio and determine color (gain/loss)
				self.portfolio.insert(END, toDisplay[0])
				if toDisplay[1] == "gain":
					self.portfolio.itemconfig(END, fg=self.money, selectbackground="green")
				elif toDisplay[1] == "loss":
					self.portfolio.itemconfig(END, fg="red", selectbackground="red")
				else:
					self.portfolio.itemconfig(END, fg="#B2B200", selectbackground="yellow")

		#Clear the entry field regardless
		self.resetEntry(None)


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

		print(self.portfolio.size())


	def close(self):
		print("Quitting")
		self.quit()


def main():
	root = Tk()
	root.title("Stock Widget")
	root.geometry("340x540")

	app = Application(root)
	root.mainloop()

main()
