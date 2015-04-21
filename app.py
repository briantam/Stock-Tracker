import urllib.request
from tkinter import *
from tkinter import messagebox
from stock import Stock

class Application(Frame):
	def __init__(self, root):
		super().__init__(root)
		self.grid()
		root.protocol("WM_DELETE_WINDOW", self.close)	#Use my callback for closing

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
		self.portFile = "portfolio.txt"	#input file
		
		#Try to initialize portfolio via input file if present
		try:
			f = open(self.portFile, "r")
			for ticker in f:
				self.myPortfolio.append(Stock(ticker.strip()))	#Use tickers only
			f.close()
			self.refresh()			#Refresh to update all stocks and the GUI
		except FileNotFoundError:
			pass

		#Enables automatic refreshes every 30 seconds
		self.after(30000, self.refreshWrapper)


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
				self.portfolio.see(END)
				if toDisplay[1] == "gain":
					self.portfolio.itemconfig(END, fg=self.money, selectbackground="green")
				elif toDisplay[1] == "loss":
					self.portfolio.itemconfig(END, fg="red", selectbackground="red")
				else:
					self.portfolio.itemconfig(END, fg="#B2B200", selectbackground="yellow")

		#Clear the entry field regardless
		self.resetEntry(None)


	#Deleting a stock from the portfolio
	def deleteStock(self):
		#Check if anything to delete
		if len(self.myPortfolio) == 0:
			return

		#Find the stock in portfolio and remove
		ticker = self.portfolio.get(ACTIVE).split()[0]
		for s in self.myPortfolio:
			if s.getTicker() == ticker:
				self.myPortfolio.remove(s)
		
		#Rehighlight the next stock
		self.portfolio.delete(ACTIVE)
		self.portfolio.selection_set(ACTIVE)


	#Used when user refreshes portfolio OR portfolio is initialized by text file
	def refresh(self):
		#Check if anything to refresh
		if len(self.myPortfolio) == 0:
			return
		#Delete all current entries	
		activeIndex = self.portfolio.index(ACTIVE)
		self.portfolio.delete(0, END)

		#Construct a chain of ticker symbols for the companies in the portfolio
		companies = ""
		for s in self.myPortfolio:
			companies += s.getTicker() + "+"
		companies = companies[:-1]

		#Make one large API request and save the response
		query1 = "http://finance.yahoo.com/d/quotes.csv?s="
		query2 = "&f=nl1c1p2"
		response = urllib.request.urlopen(query1 + companies + query2)
		data = response.read()
		text = data.decode()

		#Update all the stocks
		stockList = text.strip().split("\n")
		for i in range(len(stockList)):
			self.myPortfolio[i].update(stockList[i])

		#Add the updated stocks back to the portfolio
		for s in self.myPortfolio:
			toDisplay = s.stringify()
			self.portfolio.insert(END, toDisplay[0])
			if toDisplay[1] == "gain":
				self.portfolio.itemconfig(END, fg=self.money, selectbackground="green")
			elif toDisplay[1] == "loss":
				self.portfolio.itemconfig(END, fg="red", selectbackground="red")
			else:
				self.portfolio.itemconfig(END, fg="#B2B200", selectbackground="yellow")
		self.portfolio.activate(activeIndex)
		self.portfolio.selection_set(ACTIVE)
		self.portfolio.see(ACTIVE)


	#Used to enable automatic refresh
	def refreshWrapper(self):
		self.refresh()
		self.after(30000, self.refreshWrapper)


	#Event handler when user first clicks on the entry field
	def resetEntry(self, event):
		self.entry.delete(0,END)
		self.entry["fg"] = "black"


	#When user explicitly saves the file
	def save(self):
		#Open the portfolio text file and save all the tickers
		f = open(self.portFile, "w")
		for s in self.myPortfolio:
			print(s.getTicker(), file = f)
		f.close()
		
		#Display success message
		message = "Saved " + str(self.portfolio.size()) + " companies to your portfolio."
		messagebox.showinfo("Saved!", message)


	#When user explicitly presses my "close" button or [X] out of the window
	def close(self):
		if messagebox.askyesno("Quit", "Are you sure? Did you save first?"):
			self.quit()

