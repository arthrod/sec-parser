#!/usr/bin/env python3
"""Test confidential metadata merging functionality."""

from complete_parser import UniversalEDGARParser

# Test HTML with confidential metadata pattern
test_html = """
<html>
<body>
<p>Some regular content</p>
<p>Confidential Treatment Requested Under</p>
<p>17 C.F.R. Sections 200.80(b)(4) and 240.24b-2</p>
<p>More content after</p>
<p>Another Confidential treatment under</p>
<p>Section 123.45</p>
<p>Regular paragraph</p>
</body>
</html>
"""


parser = UniversalEDGARParser()
result = parser.parse(test_html, "test_confidential.html")

if result.success:

    for _i, element in enumerate(result.elements):
        element_info = f"[{element.type.value.upper()}]"
        if hasattr(element, "metadata") and element.metadata.get("merged_count"):
            element_info += f" (merged {element.metadata['merged_count']} elements)"

    # Check for merged elements
    merged_elements = [elem for elem in result.elements if
                      hasattr(elem, "metadata") and elem.metadata.get("merged_count")]

    for _elem in merged_elements:
        pass

else:
    pass
