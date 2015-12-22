from pyPdf import PdfFileWriter, PdfFileReader
import urllib2
from StringIO import StringIO
import re

states = ["Hawaii", "Alaska", "Florida", "South-Carolina", "Georgia", "Alabama", "North-Carolina", "Tennessee", "Rhode-Island", "Connecticut", "Massachusetts", "Maine", "New-Hampshire", "Vermont", "New-York", "New-Jersey", "Pennsylvania", "Delaware", "Maryland", "West-Virginia", "Kentucky", "Ohio", "Michigan", "Wyoming", "Montana", "Idaho", "Washington", "DC", "Texas", "California", "Arizona", "Nevada", "Utah", "Colorado", "New-Mexico", "Oregon", "North-Dakota", "South-Dakota", "Nebraska", "Iowa", "Mississippi", "Indiana", "Illinois", "Minnesota", "Wisconsin", "Missouri", "Arkansas", "Oklahoma", "Kansas", "Louisiana", "Virginia"]

years = ['2014', '2013', '2012', '2011', '2010']

# Create a new file to write all the data to
nf = 'data/state_numbers.txt'
f2 = open(nf, 'a+')

for year in years:
	print "Year = %s" % year
	for state in states:
		url = ""
		if year == '2014':
			if state != "DC" and state != "Minnesota":
				url = "http://www.iie.org/~/media/Files/Corporate/Open-Doors/Fact-Sheets-" + year + "/States/" + state + "-State-Sheet-" + year + ".ashx"
			elif state == "Minnesota":
				url = "http://www.iie.org/~/media/Files/Corporate/Open-Doors/Fact-Sheets-" + year + "/States/Minnesota-State-Sheet.ashx"
			elif state == "DC":
				url = "http://www.iie.org/~/media/Files/Corporate/Open-Doors/Fact-Sheets-" + year + "/States/Washington-DC-Sheet-" + year + ".ashx"
		elif year == '2013':
			if (len(state.split("-")) > 1) and (state != "Rhode-Island") and (state != "North-Dakota"):
				state = state.split("-")[0] + "%20" + state.split("-")[1]
			elif state == "DC":
				state = "WashingtonDC"
			url = "http://www.iie.org/~/media/Files/Corporate/Open-Doors/Fact-Sheets-" + year + "/States/" + state + "-Open-Doors-" + year + ".ashx"
		elif year == '2012':
			url = "http://www.iie.org/~/media/Files/Corporate/Open-Doors/Fact-Sheets-" + year + "/State/" + state + "-Open-Doors-" + year + ".ashx"			
		elif year == '2011':
			if (len(state.split("-")) > 1):
				state = state.split("-")[0] + "%20" + state.split("-")[1]

			if (state == 'Delaware'):
				state = 'Delware'

			if (state == "Alabama"):
				url = "http://www.iie.org/~/media/Files/Corporate/Open-Doors/Fact-Sheets-2011/State/Alabama%20Fact%20Sheet-%20Open%20Doors%202011.ashx"
			else:
				url = "http://www.iie.org/~/media/Files/Corporate/Open-Doors/Fact-Sheets-2011/State/" + state + "%20Fact%20Sheet%20-%20Open%20Doors%202011.ashx"
		elif year == '2010':
			if (len(state.split("-")) > 1):
				state = state.split("-")[0] + state.split("-")[1]
			if (state == 'Oregon'):
				url = "http://www.iie.org/~/media/Files/Corporate/Open-Doors/Fact-Sheets-2010/State/Oregon%20Fact%20Sheet%202010.ashx"
			else:
				url = "http://www.iie.org/~/media/Files/Corporate/Open-Doors/Fact-Sheets-2010/State/" + state + "2010.ashx"

		url_pdf = urllib2.urlopen(url).read()
		memory_pdf = StringIO(url_pdf)
		pdf_file = PdfFileReader(memory_pdf)

		content = pdf_file.getPage(0).extractText()

		if (state == 'Iowa') and (year == '2011'):
			f2.write("10,404:")
			continue

		if (state == 'Illinois') and (year == '2010'):
			f2.write("31,093:")
			continue

		results = []
		if (state == 'Arkansas') and (year == '2012'):
			results = re.findall(r'FOREIGN STUDENTS IN THE STATE  #\d*\* \d*,\d*', content)
		elif (state == 'Alaska') and (year == '2012'):
			results = re.findall(r'FOREIGN STUDENTS IN THE STATE  #\d*\* \d*', content)
		elif (state != 'Alaska') or (year == '2013'):
			results = re.findall(r'FOREIGN STUDENTS IN THE STATE #\d*\* \d*,\d*', content)
		else:
			results = re.findall(r'FOREIGN STUDENTS IN THE STATE #\d*\* \d*', content)
		
		if len(results) > 0:
			results = results[0].split(" ")
			num_foreign_students = results[len(results)-1]
			f2.write(num_foreign_students + ":")
			print "%s: %s" % (state,num_foreign_students)
		else:
			print "%s: no match" % state
	f2.write("\n")
