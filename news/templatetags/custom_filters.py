from django import template


register = template.Library()



@register.filter()
def censorship(text):
   """
   value: значение, к которому нужно применить фильтр
   code: код валюты
   """
   STOP_LIST = [
       'мат',
       'редиска',
       'сук',
   ]


   for word in STOP_LIST:
      if word in text:
          text = text.lower().replace(word.lower(), word[0]+'***')


   return f'{text}'