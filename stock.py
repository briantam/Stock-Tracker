class Stock(object):
	def __init__(self, name, ticker, price, changeNum, changePer):
		self.__name = name
		self.__ticker = ticker
		self.__price = price
		self.__changeNum = changeNum
		self.__changePer = changePer

	def __str__(self):
		ret = "Name: " + self.__name + " | Ticker: " + self.__ticker + " | Price: " \
			 + str(self.__price) + " | ∆: " + str(self.__changeNum) + " | %: " + str(self.__changePer)
		return ret

	#Getters
	def getName(self):
		return self.__name	
	def getTicker(self):
		return self.__ticker
	def getPrice(self):
		return self.__price
	def getChangeNum(self):
		return self.__changeNum	
	def getChangePer(self):
		return self.__changePer

	#Setters
	def setName(self, name):
		self.__name = name
	def setTicker(self, ticker):
		self.__ticker = ticker
	def setPrice(self, price):
		self.__price = price
	def setChangeNum(self, changeNum):
		self.__changeNum = changeNum
	def setChangePer(self, changePer):
		self.__changePer = changePer


stock = Stock("Apple", "AAPL", 123, 1.32, 0.24)
print(stock)