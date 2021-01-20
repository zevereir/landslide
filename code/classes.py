#RA classes
class Powerpoint:
    def __init__(self,pages):
        self.pages=pages

class Page:
    def __init__(self,elements, RA, index, n):
        self.elements=elements
        self.RA=RA
        self.index=index
        self.n=n


class Element:
    def __init__(self, index, bbox):
        self.index=index
        self.bbox=bbox

class Title(Element):
    pass

class Content(Element):
    pass
class Background(Element):
    pass


#archetypes classes
class TitleSlide:
    internal_id=0
    def __init__(self, title, subscript):
        self.title=title
        self.subscript=subscript
class TitleDoubleContent:
    internal_id = 1
    def __init__(self,title,left_content,right_content):
        self.title=title
        self.left_content=left_content
        self.right_content=right_content

class TitleSingleContent:
    internal_id = 2
    def __init__(self, title, content):
        self.title = title
        self.content = content

class TitleTripleContent:
    internal_id = 3
    def __init__(self, title, left_content, middle_content,right_content):
        self.title = title
        self.left_content = left_content
        self.middle_content=middle_content
        self.right_content = right_content

class BackgroundQuote:
    internal_id = 4
    def __init__(self, title, background):
        self.title = title
        self.background=background
class Comparison:
    internal_id = 5
    def __init__(self, title, left_content, right_content, left_subtitle, right_subtitle):
        self.title = title
        self.left_content = left_content
        self.right_content = right_content
        self.left_subtitle=left_subtitle
        self.right_subtitle=right_subtitle

class TitleOnly:
    internal_id = 6
    def __init__(self, title):
        self.title = title
class CaptionedContent:
    internal_id = 7
    def __init__(self, top_content, left_content, right_content):
        self.top_content = top_content
        self.left_content = left_content
        self.right_content = right_content

class ContentOnly:
    internal_id = 8
    def __init__(self, content):
        self.content=content

class SectionHeader:
    internal_id = 9
    def __init__(self, title, subscript):
        self.title = title
        self.subscript=subscript

class BackgroundOnly:
    internal_id = 10
    def __init__(self, background):
        self.background=background