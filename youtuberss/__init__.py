#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

from inspect import getmembers, isfunction

from home import home_page
from converter import converter_page
import jinja_filters

from flask import Flask

app = Flask(__name__)

# add jinja filters
my_filters = {name: function
              for name, function in getmembers(jinja_filters)
              if isfunction(function)}
app.jinja_env.filters.update(my_filters)


# Remove unnecessary whitespace
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.register_blueprint(home_page)
app.register_blueprint(converter_page)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
