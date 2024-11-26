

def extract_title(markdown):
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block.startswith("# "):
            return block.lstrip("#").strip()
    raise ValueError("No h1 provided in markdown")

md = """# This is my h1

This is random para
"""
extract_title(md)
