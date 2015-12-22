files = ['studies09-10.txt', 'studies10-11.txt', 'studies11-12.txt', 'studies12-13.txt', 'studies13-14.txt']

nf = 'data/studies_cleaned.txt'

f2 = open(nf, 'a+')

for i in xrange(0,len(files)):
	f = open('data/' + files[i])
	for line in f:
		words = line.split("\t")
		# the order of the data changes each year, so fix it
		if i == 2 or i == 3:		
			f2.write(words[0].strip() + ",")
			words = words[1:len(words)-1]
		elif i == 1:
			f2.write(words[1].strip() + ",")
			words = words[2:len(words)-1]
			words = words[:10] + [words[11]] + [words[10]]
		elif i == 0:
			f2.write(words[1].strip() + ",")
			words = words[2:len(words)-1]
			words = [words[0]] + [words[8]] + [words[1]] + [words[6]] + [words[7]] + [words[9]] + [words[5]] + [words[3]] + [words[2]] + [words[4]] + [words[11]] + [words[10]]
		else:
			f2.write(words[0].strip() + ",")
			words = words[3:]
			words = [words[4]] + [words[5]] + [words[0]] + [words[6]] + [words[1]] + [words[7]] + [words[8]] + [words[2]] + [words[3]] + [words[9]] + [words[10]] + [words[11]] 
		new_line = ""
		for j in xrange(0,len(words)):
			new_word = words[j].strip()
			if (i == 0):
				new_word = new_word.strip("%")
			new_line += new_word
			if (j != len(words) - 1):
				new_line += ","
		new_line += "\n"
		f2.write(new_line)
	f.close()

f2.close()
