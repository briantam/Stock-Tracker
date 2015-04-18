class Stock(object):
	def __init__(self, ticker, rawInfo):
		#Parse out the company name by finding the quotation marks
		rawInfo = rawInfo.strip()
		quoteNum = 0;
		for i in range(len(rawInfo)):
			if rawInfo[i] == "\"":
				quoteNum += 1
				if quoteNum == 2:
					break
		name = rawInfo[:i+2]		#Store the raw company name here

		#Further process the string and turn into a list
		rawInfo = rawInfo.replace(name, "")
		rawInfo = rawInfo.replace("\"", "")
		rawInfo = rawInfo.replace("%", "")
		rawInfoList = rawInfo.split(",")

		#Store all the object attributes and round numbers to 2 decimal places
		self.__name = name.strip("\",")
		self.__ticker = ticker
		self.__price = "{0:.2f}".format(float(rawInfoList[0]))
		self.__changeNum = "{0:.2f}".format(float(rawInfoList[1]))
		self.__changePer = "{0:.2f}".format(float(rawInfoList[2])) + "%"

		#Figure out the status (gain/loss/neutral)
		if float(self.__changeNum) > 0:
			self.__status = "gain"
		elif float(self.__changeNum) < 0:
			self.__status = "loss"
		else:
			self.__status = "neutral"

	#For convenient printing/debugging
	def __str__(self):
		ret = "Name: " + self.__name + " | Ticker: " + self.__ticker + " | Price: " \
			 + self.__price + " | ∆: " + self.__changeNum + " | %: " \
			 + self.__changePer + " | Status: " + self.__status
		return ret

	#For constructing the string that will be displayed in the portfolio
	#Returns a tuple. First element = display string, second element = status
	def stringify(self):
		display = self.__ticker.ljust(9) + self.__price.ljust(10) \
					+ self.__changeNum.ljust(9) + self.__changePer
		
		ret = (display, self.__status)		
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
