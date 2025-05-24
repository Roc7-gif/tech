# myapp/templatetags/html_filters.py
from django import template
from bs4 import BeautifulSoup

register = template.Library()

@register.filter(name='safe_html')
def safe_html(value):
    """
    Nettoie et ferme correctement les balises HTML dans une chaîne.
    """
    soup = BeautifulSoup(value, 'html.parser')  # ou 'html5lib' pour plus de robustesse
    return str(soup)
