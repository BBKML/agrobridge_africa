from django import template
from django.utils.html import format_html
from django.conf import settings
import os

register = template.Library()


@register.simple_tag
def responsive_image(image_field, alt='', sizes='100vw', class_attr=''):
    """Render a responsive <picture> element for an ImageField.

    Expects variant files named like original_400.jpg and original_400.webp
    """
    if not image_field:
        # fallback to a static placeholder
        placeholder = settings.STATIC_URL + 'images/image1.jpg'
        return format_html('<img src="{}" alt="{}" class="{}" loading="lazy">', placeholder, alt, class_attr)

    url = image_field.url
    # define widths
    widths = [400, 800, 1200]

    # build webp srcset
    webp_parts = []
    jpg_parts = []
    base, ext = os.path.splitext(url)
    for w in widths:
        webp_parts.append(f"{base}_{w}.webp {w}w")
        jpg_parts.append(f"{base}_{w}{ext} {w}w")

    webp_srcset = ', '.join(webp_parts)
    jpg_srcset = ', '.join(jpg_parts)

    # choose a default src (mid size jpg)
    default_src = f"{base}_800{ext}"

    html = (
        '<picture>'
        f'<source type="image/webp" srcset="{webp_srcset}" sizes="{sizes}">'
        f'<img src="{default_src}" srcset="{jpg_srcset}" sizes="{sizes}" alt="{alt}" class="{class_attr}" loading="lazy">'
        '</picture>'
    )

    return format_html(html)


@register.filter
def splitlines(value):
    if value is None:
        return []
    try:
        return str(value).splitlines()
    except Exception:
        return []
