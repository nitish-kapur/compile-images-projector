# Projector Screen Image Arranger

A Python script that arranges multiple images into a grid layout scaled to fit a projector screen of a specified diagonal size, and saves the result as a single composite image.

---

## Author

**Nitish Kapur**<br>
GitHub: [github.com/nitish-kapur](https://github.com/nitish-kapur)

---

## Requirements
```bash
pip install pillow
```

---

## Usage

1. Place all images to be arranged in the same directory as the script
2. Run:
```bash
python compile-images-projector.py
```

The composite image will be saved to the `output/` subfolder automatically.

---

## Configuration

All key parameters are defined as constants at the top of the script:

| Constant | Default Value | Description |
|---|---|---|
| `PROJECTOR_DIAGONAL` | `201` | Diagonal size of the projector screen in inches |
| `ASPECT_RATIO_WIDTH` | `16` | Width component of the aspect ratio |
| `ASPECT_RATIO_HEIGHT` | `9` | Height component of the aspect ratio |
| `IMAGE_WIDTH_INCHES` | `14` | Width of each individual image in inches |
| `IMAGE_HEIGHT_INCHES` | `10` | Height of each individual image in inches |
| `NUM_IMAGES` | `110` | Maximum number of images to arrange |

Edit these values directly in the script to match your projector and image specifications.

---

## Output

| Location | File | Description |
|---|---|---|
| `output/` | `projector_screen.png` | Composite image of all arranged images |

---

## Supported Input File Types

`.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`

---

## Notes

- Images are arranged in a grid layout; the number of rows and columns is calculated automatically based on the screen and image dimensions.
- Images are scaled using the **Lanczos** resampling filter to maintain quality.
- The composite canvas is rendered at **100 DPI** for image placement.
- If fewer images are found than `NUM_IMAGES`, only the available images are placed.
- Original files are not modified.
