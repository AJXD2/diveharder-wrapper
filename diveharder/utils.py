def hdml_to_md(text: str) -> str:
    """
    Converts a string in HDML (DiveHarder Markup Language) format to Markdown format.
    
    Args:
        text (str): The input string in HDML format.
        
    Returns:
        str: The input string converted to Markdown format.
    
    Example:
        >>> hdml_to_md("<i=3>Hello</i=3> <i=1>World</i=1>")
        "[b]Hello[/b] [yellow]World[/yellow]"
    """
    format_mapping = {
        "<i=3>": "[b]",  # Bold
        "</i=3>": "[b]",  # Thank you for doing bold twice devs :thumbsup:
        "<i=1>": "[yellow]",  # Yellow text
        "</i>": "[/]",  # Closing tag
    }
    for code, markup in format_mapping.items():
        text = text.replace(code, markup)
    return text


def url_join(*args):
    """Join combine URL parts to get the full endpoint address."""
    return "/".join(arg.strip("/") for arg in args)
