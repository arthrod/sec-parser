#!/usr/bin/env python3
"""Debug V7 processing steps to understand why HTML comments aren't being removed"""

from bs4 import BeautifulSoup, Comment
from pathlib import Path
from agreement_parser_v7 import AgreementParserV7, HtmlCommentRemoverStep


def debug_html_comments():
    """Debug HTML comment processing."""
    print("🔍 Debugging HTML Comment Processing")
    print("=" * 50)
    
    # Load agreement 041 HTML
    html_file = Path("html_files/agreement_041.html")
    html_content = html_file.read_text(encoding='utf-8')
    
    print(f"📄 Loaded {html_file.name}")
    print(f"📊 HTML Size: {len(html_content):,} chars")
    
    # Parse with BeautifulSoup to find comments
    soup = BeautifulSoup(html_content, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    
    print(f"💬 Found {len(comments)} HTML comments:")
    for i, comment in enumerate(comments[:5], 1):
        print(f"   {i}. {comment.strip()}")
    
    print("\n🧪 Testing V7 Parser...")
    
    # Test V7 parser
    parser = AgreementParserV7()
    elements = parser.parse(html_content)
    
    print(f"📊 Parsed {len(elements)} elements")
    
    # Look for TextElements that might be comments
    text_elements = [e for e in elements if hasattr(e, 'html_tag') and e.html_tag]
    
    print(f"📝 Found {len(text_elements)} elements with HTML tags")
    
    # Check if any contain image filenames
    image_patterns = [
        "a123123-exhibit109001.jpg",
        "a123123-exhibit109002.jpg", 
        "exhibit109001.jpg",
        ".jpg"
    ]
    
    found_images = []
    for elem in text_elements:
        if elem.html_tag.text:
            text = elem.html_tag.text.strip()
            for pattern in image_patterns:
                if pattern in text:
                    found_images.append((elem.__class__.__name__, text[:100]))
                    break
    
    print(f"\n🖼️  Found {len(found_images)} elements with image references:")
    for cls_name, text in found_images:
        print(f"   {cls_name}: {text}")
    
    # Test HtmlCommentRemoverStep directly
    print(f"\n🧪 Testing HtmlCommentRemoverStep directly...")
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
        print(f"🔧 Found HtmlCommentRemoverStep at index {comment_step_index}")
        
        # Run steps up to but not including comment remover
        elements_before = elements = parser_before.parse(html_content)
        
        # Manually run comment remover
        stats = comment_remover.get_stats()
        print(f"📊 Comment remover stats: {stats}")
    else:
        print("❌ HtmlCommentRemoverStep not found in pipeline!")
    
    return elements


def debug_consecutive_pages():
    """Debug consecutive page number processing."""
    print(f"\n🔍 Debugging Consecutive Page Numbers")
    print("=" * 50)
    
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
    
    print("🧪 Testing with artificial consecutive page numbers...")
    
    parser = AgreementParserV7()
    elements = parser.parse(test_html)
    
    print(f"📊 Parsed {len(elements)} elements")
    
    for elem in elements:
        if hasattr(elem, 'html_tag') and elem.html_tag and elem.html_tag.text:
            text = elem.html_tag.text.strip()
            print(f"   {elem.__class__.__name__}: '{text}'")


def debug_redaction_patterns():
    """Debug redaction pattern processing."""
    print(f"\n🔍 Debugging Redaction Patterns")
    print("=" * 50)
    
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
    
    print("🧪 Testing with artificial redaction patterns...")
    
    parser = AgreementParserV7()
    elements = parser.parse(test_html)
    
    print(f"📊 Parsed {len(elements)} elements")
    
    for elem in elements:
        if hasattr(elem, 'html_tag') and elem.html_tag and elem.html_tag.text:
            text = elem.html_tag.text.strip()
            print(f"   {elem.__class__.__name__}: '{text}'")


if __name__ == "__main__":
    debug_html_comments()
    debug_consecutive_pages()
    debug_redaction_patterns()