
from pypdf import PdfReader
from pypdf.errors import PdfReadError


def extract_text_from_pdf(pdf_file):
    """Extracts text from each PDF page while preserving its source."""

    try:
        reader = PdfReader(pdf_file)

        if reader.is_encrypted:
            raise ValueError(
                "This PDF is password-protected. "
                "Please upload an unlocked version."
            )

        extracted_pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text()

                if text and text.strip():
                    extracted_pages.append({
                        "page": page_number,
                        "text": text.strip()
                    })

                    print(
                        f"[EXTRACTION] Page {page_number}: "
                        f"{len(text)} characters"
                    )

                else:
                    print(
                        f"[EXTRACTION] Page {page_number}: "
                        "No text found."
                    )

            except Exception as error:
                raise ValueError(
                    f"Failed to extract text from page "
                    f"{page_number}: {error}"
                ) from error

        return extracted_pages

    except PdfReadError as error:
        raise ValueError(
            "Unable to read the PDF file. "
            "Please check whether the file is valid."
        ) from error
