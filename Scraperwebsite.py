from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys

root = "https://aflcio.org/paywatch/company-pay-ratios"

issp500 = "0"
order = "median"
sort = "desc"

#Gets top company for each state 
# Returns array of 50 states 

def get_by_state():
	industry = "All"
	states = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC",  
	"DE", "FL", "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA",  
	"MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE",  
	"NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC",  
	"SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]
	print (states)

	results = []

	for i in range(len(states)):
		#f' means expect variables. It's telling the string to expect variables. 
#url filters for top company for each state
		url = f'{root}?combine=&industry={industry}&state={states[i]}&sp500={issp500}&order={order}&sort={sort}'
		#make get erquest for that url
		response = requests.get(url)
		#tell beautiful soup to parse html string
		soup = BeautifulSoup(response.text, 'html.parser')
		table = soup.find("table", class_="cols-4")
		if table:
			top_company = table.find("tbody").find("tr") #.find_all("tr")[0]
			#strip removes white space in the text
			cells = [cell.text.strip() for cell in top_company.find_all("td")]
			#append state name to row
			cells.append(states[i])
			#append state with top company to results arrray
			results.append(cells)

	#print(results)

	# df = pd.DataFrame(results, columns=['ticker', 'company', 'median worker pay', 'pay ratio', 'state'])
	# df.to_csv('top_company_by_state.xls', index=False)
	return results


#Returns dictionary mapping from company ticker to industry
def get_by_industry():
	# did not hard code industry because what if they add another industry
	#industries = ["Communication Services", '']
	response = requests.get(root)
	soup = BeautifulSoup(response.text, 'html.parser')
	#find the dropdown in html
	form = soup.find("select", class_="form-select form-control custom-select")

	#form = soup.find('select',{'class':'form-select form-control custom-select'})
	#getting all dropdown values 
	options = form.find_all("option")
	#we ddint want the first industries option
	industries = [option.text.strip() for option in options][1:]
	#print (industries)
	state = "All"
	#Making a dictionary instead of an array 
	industry_dict = {}
	for i in range(len(industries)): #go through industries
		page = 0
		while True:
			url = f'{root}?combine=&industry={industries[i]}&state={state}&sp500={issp500}&order={order}&sort={sort}&page={page}'
			response = requests.get(url)
			soup = BeautifulSoup(response.text, 'html.parser')
			table = soup.find("table", class_="cols-4")
			#checking if table because what if it reaches the final page with no table  
			if table:
				#companies goes through all companies gives me all 
				companies = table.find("tbody").find_all("tr")
				for company in companies:
					
					#company will give me the first row of all industries
					#getting the ticker for the company
					ticker = company.find("td").text.strip()
					#or
					#ticker = company.find_all("td")[1].text.strip() 

					industry_dict[ticker] = industries [i]
					#whatever you map in the dictionary has to be unique
					#company_cells = []
					# for cell in company.find_all("td"):
					# 	company_cells.append(cell.text.strip())
					# industry_dict[company_cells[0]] = industries[i]
				# cells.append(industries[i])
				# results.append(cells)
			else:
				print(page)
				break

			page += 1
	print(industry_dict)
	return industry_dict

def find_industry(state_results, industry_dict):
	for i in range (len (state_results)): 
		#for i in state_results 
		#top_company returns all 4 coloumns 
		top_company = state_results[i]
		#we get the ticker or the first element
		ticker = top_company[0]
		#look up the ticker symbol in the industry
		#takes aapl and returns communications or associated industry name for aapl
		industry = industry_dict[ticker]
		top_company.append(industry)
		#returns top company name with the associated industry name
		return state_results
		#we are returning to pass

	

state_results = get_by_state()
print (state_results)
industry_dict = get_by_industry()
print (industry_dict)
results = find_industry(state_results, industry_dict)
print (results)
df = pd.DataFrame(results, columns= ['ticker', 'company', 'median worker pay', 'pay ratio']) 
df.to_csv('top_company')













