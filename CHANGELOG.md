# CHANGELOG

All notable changes to this project will be documented in this file.

## [Unreleased] - 2025-11-17
### Added
- `tools/blur_faces.py`: script to blur faces in videos using OpenCV.
- `website/templatetags/responsive_images.py`: template tag and `splitlines` filter for responsive images.

### Changed
- LinkedIn footer link updated to `https://www.linkedin.com/company/agrobridge-africa`.
- Added global CSS to render content images as circular by default. Logos are preserved square using the `no-round` class.
- Image variants generation (JPG/WebP) added to image upload handlers (best-effort).

### Notes
- Run `pip install -r requirements.txt` after pulling changes.
- To blur a video: `python tools/blur_faces.py input.mp4 output_blurred.mp4 --blur 25`.
- Review generated media variants in `MEDIA_ROOT` after uploading images.

