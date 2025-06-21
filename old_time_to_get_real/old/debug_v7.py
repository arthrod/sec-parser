#!/usr/bin/env python3
"""Debug V7 processing steps to understand why HTML comments aren't being removed."""

from pathlib import Path

from bs4 import BeautifulSoup, Comment

from agreement_parser_v7 import AgreementParserV7, HtmlCommentRemoverStep


def debug_html_comments():
    """Debug HTML comment processing."""
    # Load agreement 041 HTML
    html_file = Path("html_files/agreement_041.html")
    html_content = html_file.read_text(encoding="utf-8")

    # Parse with BeautifulSoup to find comments
    soup = BeautifulSoup(html_content, "html.parser")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    for i, _comment in enumerate(comments[:5], 1):
        pass

    # Test V7 parser
    parser = AgreementParserV7()
    elements = parser.parse(html_content)

    # Look for TextElements that might be comments
    text_elements = [e for e in elements if hasattr(e, "html_tag") and e.html_tag]

    # Check if any contain image filenames
    image_patterns = [
        "a123123-exhibit109001.jpg",
        "a123123-exhibit109002.jpg",
        "exhibit109001.jpg",
        ".jpg",
    ]

    found_images = []
    for elem in text_elements:
        if elem.html_tag.text:
            text = elem.html_tag.text.strip()
            for pattern in image_patterns:
                if pattern in text:
                    found_images.append((elem.__class__.__name__, text[:100]))
                    break

    for _cls_name, text in found_images:
        pass

    # Test HtmlCommentRemoverStep directly
    comment_remover = HtmlCommentRemoverStep()

    # Get elements before comment removal
    parser_before = AgreementParserV7()
    steps_before = parser_before.get_default_steps()

    # Find the comment remover step
    comment_step_index = -1
    for i, step in enumerate(steps_before):
        if isinstance(step, HtmlCommentRemoverStep):
            comment_step_index = i
            break

    if comment_step_index >= 0:

        # Run steps up to but not including comment remover
        elements = parser_before.parse(html_content)

        # Manually run comment remover
        comment_remover.get_stats()

    return elements


def debug_consecutive_pages() -> None:
    """Debug consecutive page number processing."""
    # Create test HTML with consecutive page numbers
    test_html = """
    <html><body>
    <p>Some content</p>
    <p>1</p>
    <p>2</p>
    <p>3</p>
    <p>More content</p>
    </body></html>
    """

    parser = AgreementParserV7()
    elements = parser.parse(test_html)

    for elem in elements:
        if hasattr(elem, "html_tag") and elem.html_tag and elem.html_tag.text:
            elem.html_tag.text.strip()


def debug_redaction_patterns() -> None:
    """Debug redaction pattern processing."""
    # Create test HTML with redaction patterns
    test_html = """
    <html><body>
    <p>Some content</p>
    <p>[***]</p>
    <p>***</p>
    <p>[****]</p>
    <p>More content</p>
    </body></html>
    """

    parser = AgreementParserV7()
    elements = parser.parse(test_html)

    for elem in elements:
        if hasattr(elem, "html_tag") and elem.html_tag and elem.html_tag.text:
            elem.html_tag.text.strip()


if __name__ == "__main__":
    debug_html_comments()
    debug_consecutive_pages()
    debug_redaction_patterns()
