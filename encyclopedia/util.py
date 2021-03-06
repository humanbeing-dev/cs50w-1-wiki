import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def markdown_to_HTML(content):
    """
    To implement:
    - headings
    - boldface
    - unordered list
    - links
    - paragraphs
    """
    print(content)

    head_pattern = "(#+) ([\w* ]+)"
    bold_pattern = "\*{2}([\w]+)+\*{2}"
    italic_pattern = "\*{1}([\w]+)+\*{1}"
    list_pattern = "- ([\w]+)"
    link_pattern = "\[(\w+)\]\(([/\w]+)\)"

    # <a href='2'>1</a>

    def find_heading(regex_object):
        # Check how many hashes in md
        hash_counter = len(regex_object.group(1))
        heading_type = min(hash_counter, 6)
        tag_content = regex_object.group(2)
        return f"<h{heading_type}>{'#' * (hash_counter % 6) + ' ' if hash_counter > 6 else ''}{tag_content}</h{heading_type}>"


    def find_bold(regex_object):
        # Check how many hashes in md
        tag_content = regex_object.group(1)
        return f"<strong>{tag_content}</strong>"

    
    def find_italic(regex_object):
        # Check how many hashes in md
        tag_content = regex_object.group(1)
        return f"<em>{tag_content}</em>"

        
    def find_list(regex_object):
        # Check how many hashes in md
        tag_content = regex_object.group(1)
        return f"<li>{tag_content}</li>"


    def find_link(regex_object):
        # Check how many hashes in md
        tag_content = regex_object.group(1)
        link = regex_object.group(2)
        return f"<a href='{link}'>{tag_content}</a>"


    new_content = re.sub(head_pattern, find_heading, content)
    new_content = re.sub(bold_pattern, find_bold, new_content)
    new_content = re.sub(italic_pattern, find_italic, new_content)
    new_content = re.sub(list_pattern, find_list, new_content)
    new_content = re.sub(link_pattern, find_link, new_content)

    print(new_content)
