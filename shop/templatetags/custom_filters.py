from django import template

register = template.Library()

@register.filter
def star_rating(value):
    """ Converts an integer rating (1-5) into star symbols """
    full_stars = '★' * value
    empty_stars = '☆' * (5 - value)
    return full_stars + empty_stars

@register.filter
def stars(value):
    """Converts a numerical rating to stars (⭐)."""
    try:
        value = float(value)  # Ensure it's a float
        return '⭐' * int(round(value))  # Generate stars based on rating
    except (ValueError, TypeError):
        return ''  # Return empty if invalid input