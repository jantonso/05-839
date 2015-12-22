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

class MainPage(BaseHandler):
    def get(self):
        countries = self.request.get('countries')
        bottom = self.request.get('bot')
        country = 3
        if countries == 'europe':
            country = 1
        elif countries == 'asia':
            country = 2

        bot = 1
        if bottom == 'description':
            bot = 2
        elif bottom == 'table':
            bot = 1

        variables = {'countries': country, 'bottom': bot}
        self.render_response('main.html', **variables)

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

