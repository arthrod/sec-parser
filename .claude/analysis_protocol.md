# SEC Agreement Analysis Protocol

## File-by-File Review Instructions

### Step 1: Load File Data
```bash
# Load JSON parsed output
cat time_to_get_real/parsed_output/agreement_XXX_parsed_standard.json

# Load HTML source
cat time_to_get_real/html_files/agreement_XXX.html
```

### Step 2: Validation Analysis
```python
# Run validation on specific file
python time_to_get_real/validate.py agreement_XXX_parsed_standard.json
```

### Step 3: Systematic Review
For each file, analyze:

1. **Element Count & Distribution**
   - Total elements
   - Element types (EmptyElement, TitleElement, TextElement, etc.)
   - Size category (Small <20, Medium 20-200, Large >200)

2. **Structural Quality Assessment**
   - Orphan elements: Count and percentage
   - Parent-child relationships
   - Hierarchy depth and consistency

3. **Metadata Handling Evaluation**
   - Trash elements remaining
   - Types of metadata artifacts
   - Filtering effectiveness

4. **HTML Pattern Analysis**
   - Document structure complexity
   - Problematic markup patterns
   - Parser-friendly vs challenging structures

### Step 4: Evidence Documentation
Document with specific examples:
- JSON snippets showing structure
- HTML patterns causing issues
- Quantitative metrics (counts, percentages)
- Qualitative assessment (good/bad patterns)

### Step 5: Update Review Files
Update appropriate review_batch_XX.md with:
- Completed checkboxes
- Real data snippets
- Evidence-based findings
- Specific recommendations

### Analysis Standards
- **Be thorough**: Examine both JSON and HTML in detail
- **Be specific**: Provide exact counts, element IDs, text snippets
- **Be evidence-based**: Support all claims with concrete examples
- **Be systematic**: Follow same analysis depth for all files
- **Be actionable**: Provide specific improvement recommendations

### Continuous Process
- Process files 001-100 in order
- Do not skip any files
- Maintain consistent analysis quality
- Update cumulative statistics
- Track emerging patterns across batches

### Quality Gates
Before marking a file complete:
- [ ] JSON structure analyzed
- [ ] HTML patterns documented
- [ ] Validation metrics recorded
- [ ] Issues clearly identified
- [ ] Evidence provided for all claims
- [ ] Recommendations formulated