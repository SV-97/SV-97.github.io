import argparse
from pathlib import Path
import re

parser = argparse.ArgumentParser(description="Translate a html file to a markdown file")
parser.add_argument("-p", "--path", dest="path", default="./index.html", help="Paht of source file")
args = parser.parse_args()
path = Path(args.path)

with open(path, "r") as f:
    source = f.read()


def bold(match):
    return f"**{match.group(1)}**"


def italics(match):
    return f"*{match.group(1)}*"


def paragraph(match):
    return match.group(1)


def heading(match):
    heading_thingy = "#" * int(match.group(1))
    return f"{heading_thingy} {match.group(2)}"


def unordered_list(match):
    def list_item(match):
        return f"* {match.group(1)}"
    return re.sub(r"<li>([\w\W]*?)<\/li>", list_item, match.group(1))


def ordered_list(match):
    def list_item(match):
        return f"1. {match.group(1)}"
    return re.sub(r"<li>([\w\W]*?)<\/li>", list_item, match.group(1))


def hyperlink(match):
    return f"[{match.group('text')}]({match.group('url')})"


def image(match):
    return f"![YOURIMAGETEXT]({match.group('url')})"


def table(match):
    return f"# TABLE {match.group(1)}"


source = re.sub(r"<b>([\w\W]*?)<\/b>", bold, source)
source = re.sub(r"<i>([\w\W]*?)<\/i>", italics, source)
source = re.sub(r"<p>([\w\W]*?)<\/p>", paragraph, source)
source = re.sub(r"<br>", " \n\n", source)
source = re.sub(r"<h(\d)>([\w\W]*?)<\/h\d>", heading, source)
source = re.sub(r"<ul>([\w\W]*?)<\/ul>", unordered_list, source)
source = re.sub(r"<ol>([\w\W]*?)<\/ol>", ordered_list, source)
source = re.sub(r"<code>([\w\W]*?)<\/code>", "```\nCode here\n```", source)
source = re.sub(r"<a href=\"(?P<url>.*)\">(?P<text>[\w\W]*?)<\/a>", hyperlink, source)
source = re.sub(r"<img src=\"(?P<url>.*)\"[\w\W]*?/>", image, source)
source = re.sub(r"<table>([\w\W]*?)<\/table>", table, source)
# source = re.sub(r"<(?P<tag1>.*)>(?P<text>[\w\W]*?)<\/(?P=tag1)>", lambda m: m.group("text"), source)
old_source = source
while True:
    source = re.sub(r"\n\n", "\n", old_source)
    if old_source != source:
        old_source = source
    else:
        break

with open(f"{path.stem}.md", "w") as f:
    f.write(source)