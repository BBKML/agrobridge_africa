from PIL import Image, ImageOps
import os
from django.conf import settings

def _ensure_dir(path):
    d = os.path.dirname(path)
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def generate_variants(image_path, sizes=(400, 800, 1200), webp=True, quality=85):
    """Generate resized JPG and optionally WebP variants for a given image path.

    Variants are saved as: originalname_<width>.<ext> and <width>.webp
    Returns a dict of generated filepaths keyed by width and format.
    """
    results = {'jpg': {}, 'webp': {}} if webp else {'jpg': {}}

    if not os.path.exists(image_path):
        return results

    base, ext = os.path.splitext(image_path)
    ext = ext.lower().lstrip('.')

    try:
        with Image.open(image_path) as im:
            # convert to RGB to avoid issues with PNG transparency when saving JPEG
            if im.mode not in ('RGB', 'RGBA'):
                im = im.convert('RGB')

            for w in sizes:
                im_copy = im.copy()
                im_copy = ImageOps.exif_transpose(im_copy)
                im_copy.thumbnail((w, w * 10), Image.LANCZOS)
                jpg_path = f"{base}_{w}.{ext}"
                _ensure_dir(jpg_path)
                im_copy.save(jpg_path, format='JPEG' if ext in ['jpg','jpeg'] else im_copy.format or 'JPEG', quality=quality, optimize=True)
                results['jpg'][w] = jpg_path

                if webp:
                    webp_path = f"{base}_{w}.webp"
                    im_copy.save(webp_path, format='WEBP', quality=quality, optimize=True)
                    results['webp'][w] = webp_path

    except Exception:
        # keep silent — best effort
        return results

    return results

def url_for_variant(original_url, width, ext=None):
    """Given an original media URL and a width, return URL of variant.

    Example: /media/products/foo.jpg -> /media/products/foo_800.jpg
    If ext provided (e.g., 'webp'), it will use that extension.
    """
    if not original_url:
        return ''
    base, orig_ext = os.path.splitext(original_url)
    if ext:
        return f"{base}_{width}.{ext}"
    else:
        return f"{base}_{width}{orig_ext}"
