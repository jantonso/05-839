#filew = open("training.txt","a")
    #filew.write(user_name + ":" + session_number)
    #filew.write("\n")
    #for wm in window_movements:
#       filew.write("%f " % wm)
#   filew.write("\n")
#   filew.close()

new_file = open("data/new_immigration_cleaned.csv","w")

with open("data/new_immigration.csv","r") as training:
	for line in training:
		ls = line.split('\t')
		for i in xrange(0,10):
			print ls[i]
		if i == 0:
			i += 1
			continue
		break	
