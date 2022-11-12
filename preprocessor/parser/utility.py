def is_single_break(line, tag):
    # True if the text is not a single break tag or space
    return not len(line) > len(tag) + 1