with open("C:/Users/Rohit/Documents/IPython Notebooks/Wiki Parser/all data files/"+file, 'rb') as csvfile:

    datareader = csv.reader(csvfile, delimiter=',')
    foundEdit=None
    country = datareader.next()[0][8:-9]
            
    for row in datareader:
        
            #row[:1] gives a one element list ['Geeta Menon, Dean of the Undergraduate College at New York University Stern School of Business'] 
            #row[:1][0].split(',')[0] extracts Geeta Menon out of the first element
        if not row:
            continue
        temp=row[:1][0].split(',')[0]
        
                #start printing when you find [edit] in the last six characters
                #store the area of expertise
        
        if temp[-6:] =='[edit]':
            foundEdit=True
            areaOfExpertise=temp[:-6]
            
        
            
        if foundEdit and temp and not "[edit]" in temp:
            
            temp=handleExceptions(temp)
            if temp is '':
                continue
                
            try:
                wikipage = urllib2.urlopen('http://en.wikipedia.org/wiki/'+string.replace(temp, ' ', '_'))
                html = wikipage.read()
                influence=len(html)
            except urllib2.HTTPError:
                influence=0
                        
                    #print all_data
            with open('output.csv', 'ab') as csvfile:
                fieldnames = ['country', 'name','area','influence']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)                        
                        #writer.writeheader()
                writer.writerow({'country':country,'name':temp,'area':areaOfExpertise,'influence':str(influence)})
