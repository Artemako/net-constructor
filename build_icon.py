"""One-off script: render resources/app-icon.svg to resources/app-icon.ico using PySide6 and Pillow."""

import io
import sys
from pathlib import Path

from PIL import Image
from PySide6.QtCore import QByteArray, QBuffer, QIODevice
from PySide6.QtGui import QImage, QPainter
from PySide6.QtSvg import QSvgRenderer

ROOT = Path(__file__).resolve().parent
SVG_PATH = ROOT / "resources" / "app-icon.svg"
ICO_PATH = ROOT / "resources" / "app-icon.ico"
SIZES = (256, 48, 32, 16)


def main() -> None:
    if not SVG_PATH.exists():
        print(f"SVG not found: {SVG_PATH}", file=sys.stderr)
        sys.exit(1)
    renderer = QSvgRenderer(str(SVG_PATH))
    if not renderer.isValid():
        print("QSvgRenderer: invalid SVG", file=sys.stderr)
        sys.exit(1)
    images = []
    for size in SIZES:
        image = QImage(size, size, QImage.Format_ARGB32)
        image.fill(0)
        painter = QPainter(image)
        renderer.render(painter)
        painter.end()
        buf = QBuffer()
        buf.open(QIODevice.WriteOnly)
        image.save(buf, "PNG")
        buf.close()
        data = buf.data().data()
        pil_img = Image.open(io.BytesIO(data))
        pil_img = pil_img.convert("RGBA")
        images.append(pil_img)
    images[0].save(
        str(ICO_PATH),
        format="ICO",
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:] if len(images) > 1 else [],
    )
    print(f"Written {ICO_PATH}")


if __name__ == "__main__":
    main()
