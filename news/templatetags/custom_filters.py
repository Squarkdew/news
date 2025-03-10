from django import template


register = template.Library()




BAD_WORDS = ['редиска']  

@register.filter()
def censor(value):
   
    if not isinstance(value, str):
        raise ValueError('Фильтр "censor" может быть применён только к строкам.')

    def replace(word):
        if word.lower() in BAD_WORDS:
            return word[0] + '*' * (len(word) - 1)
        return word

    censored_words = [replace(word) for word in value.split()]
    
    return ' '.join(censored_words)

