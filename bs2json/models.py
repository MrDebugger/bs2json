from dataclasses import dataclass


@dataclass
class ConversionConfig:
    """Configuration for HTML-to-JSON conversion.

    Controls label names used in the JSON output, and behavioral flags
    for how elements are processed.
    """
    attr_name: str = "attrs"
    text_name: str = "text"
    comment_name: str = "comment"
    include_comments: bool = True
    strip: bool = True
    keep_order: bool = False
