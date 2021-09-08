# app/templatetags/getattribute.py

import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if len(value) >= int(arg)-1:
        return value[int(arg)-1]
    else:
        return None
    # elif hasattr(value, str(arg)):
    #     return getattr(value, arg)
    # elif hasattr(value, 'has_key') and value.has_key(arg):
    #     return value[arg]
    # elif numeric_test.match(str(arg)) and len(value) > int(arg):
    #     return value[int(arg)]
    # else:
    #     return settings.TEMPLATE_STRING_IF_INVALID

register.filter('getattribute', getattribute)