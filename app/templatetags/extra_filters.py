from django import template

register=template.Library()

@register.simple_tag()
def multiply(value,arg):
    return value*arg

@register.filter('convert')
def convert(value):
    val= {'M':'Mobile' ,'L':'Laptob', 'TW':'Top Wear', 'BW':'Bottom Wear'}  
    return val.get(value)

@register.filter('slice')
def slice(value):
    try:
        return int(value[13:])
    except:
        return ''
    
@register.filter('adding')
def slice(value,arg):
    return value + int(arg)   
    