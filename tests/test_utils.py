import io
from pathlib import Path

import pytest
from fastapi import UploadFile
from starlette.datastructures import Headers

from app.utils.loaders import load_pdf

DATA_DIR = Path(__file__).parent / "data"


# Helper to create UploadFile from file bytes
def create_upload_file(
    file_path: Path,
    content_type="application/pdf",
):
    with open(file_path, "rb") as f:
        return UploadFile(
            filename=file_path.name,
            file=io.BytesIO(f.read()),
            headers=Headers({"content-type": content_type}),
        )


# Normal text PDF
# -----------------------------
def test_load_pdf_text_file():
    file_path = DATA_DIR / "sample_text.pdf"
    upload_file = create_upload_file(file_path)

    pages = load_pdf(upload_file)

    assert len(pages) > 0, "Text PDF should return pages"
    assert any(
        "Lorem" in page or "Sample" in page for page in pages
    ), "Expected text content missing"


def test_load_pdf_empty_file():
    file_path = DATA_DIR / "sample_empty.pdf"
    upload_file = create_upload_file(file_path)

    pages = load_pdf(upload_file)

    assert all(not page.strip() for page in pages), "Empty PDF should return empty page content"


def test_load_pdf_image_pdf():
    file_path = DATA_DIR / "sample_image.pdf"
    upload_file = create_upload_file(file_path)
    page_texts = load_pdf(upload_file)
    assert all(
        not page.strip() for page in page_texts
    ), "Image-based PDF detected. OCR not supported."


def test_load_pdf_corrupt_file():
    file_path = DATA_DIR / "sample_corrupt.pdf"
    upload_file = create_upload_file(file_path)

    with pytest.raises(ValueError):
        load_pdf(upload_file)


def test_load_pdf_non_pdf():
    fake_file = UploadFile(
        filename="sample.txt",
        file=io.BytesIO(b"hello world"),
        headers=Headers({"content-type": "text/plain"}),
    )

    with pytest.raises(ValueError):
        load_pdf(fake_file)
