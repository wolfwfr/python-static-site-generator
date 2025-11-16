def extract_title(markdown):
    top_line = markdown.split("\n", 1)[0]
    if not top_line.startswith("# "):
        raise Exception("markdown document must start with an 'h1' heading")
    return top_line.removeprefix("# ")
