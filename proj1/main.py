import webapp2
import logging
import urllib
from webapp2_extras import jinja2

# this library is for decoding json responses
from webapp2_extras import json

# BaseHandler subclasses RequestHandler so that we can use jinja
class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

        # This will call self.response.write using the specified template and context.
        # The first argument should be a string naming the template file to be used. 
        # The second argument should be a pointer to an array of context variables
        #  that can be used for substitutions within the template
    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)

class Viz3(BaseHandler):
	def get(self):
		# logic for map vizualizaiton
		try:
			mapyear = int(self.request.get('mapyear'))
		except ValueError:
			mapyear = 0

		if not mapyear:
			mapyear = 0
		
		logging.info(mapyear)
		state_num = []
		try:
			fp = open("data/state_numbers.txt")
			lines = fp.readlines()
			line = lines[mapyear]	
			line = line.split(":")
			line = line[:len(line)-1]
			state_nums = line
		except IOError:
			logging.info("failed to load file")

		if mapyear == 0:
			mapyear = '2014'
		elif mapyear == 1:
			mapyear = '2013'
		elif mapyear == 2:
			mapyear = '2012'
		elif mapyear == 3:
			mapyear = '2011'
		else:
			mapyear = '2010'

		variables = {'state_nums': state_nums,
        			 'map_year': mapyear}
	
		self.render_response('viz3.html', **variables)

class MainPage(BaseHandler):
    
	def get(self):
		#logging.info(results)
		# add it to the context being passed to jinja
		try:
			year = int(self.request.get('year'))
		except ValueError:
			year = 0

		if not year:
			year = 0

		data = []
		countries = []		
		should_read = False
		try: 
			fp = open("data/studies_cleaned.txt")
			for line in fp:
				if (line[0] == str(year)):
					should_read = True
					continue
				elif (len(line) == 2):
					should_read = False
				if (should_read):
					data += [line.split(",")]
			fp.close()
		except IOError:
			logging.info("failed to load file")

		for i in xrange(0,len(data)):
			countries += [data[i][0]]
			data[i] = data[i][1:len(data[i])]
			for j in xrange(0,len(data[i])):
				data[i][j] = float(data[i][j].strip("\n"))

		majors = ['Business/Mgmt.', 'Education', 'Engineering', 'Fine/Applied Arts', 'Health Professions', 'Humanities', 'Intensive English', 'Math/Computer Science', 'Physical/Life Sciences', 'Social Sciences', 'Other', 'Undeclared']
		variables = {'countries': countries,
					 'majors': majors,
				     'percentages': data,
					 'current_year': year}

		self.render_response('viz2.html', **variables)

application = webapp2.WSGIApplication([
    ('/visualization2/', MainPage),
	('/visualization3/', Viz3),
], debug=True)

