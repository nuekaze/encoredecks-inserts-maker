import sys
import re

import requests
from bs4 import BeautifulSoup

try:
    cards_file = open(sys.argv[1], 'r').read().split('\n')[:-1]
    cards = []

    for c in cards_file:
        # Card path is always "Set/WSxx-CARD" so we can just look for a slash.
        if "/" in c:
            cards.append(c)

except FileNotFoundError:
    print("Could not find file: " + sys.argv[1])
    exit(1)

except:
    print("Usage: " + sys.argv[0] + "card_list.txt")
    exit(1)

# Print the HTML
print("""<html>
<head>
<style type="text/css">
body {
        display: flex;
        flex-wrap: wrap;
}
@media print{
        @page {
          size: auto;
        }
}
h1 {
        font-size: 1.5em;
    text-align: center;
}
div.card {
        width: 60mm;
        font-size: 0.4em;
        border: solid black 1px;
        padding: 0.5em;
        break-inside: avoid;
}
img {
        height: 0.8em;
        width: 0.8em;
}
</style>
</head>
<body>""")

for c in cards:
    c = c.split('\t')

    resp = requests.get("https://en.ws-tcg.com/cardlist/?cardno=" + c[0])
    soup = BeautifulSoup(resp.content, "html.parser")

    if not soup:
        continue

    card = {
        "name": c[2],
        "text": str(soup.find_all(class_="p-cards__detail u-mt-22 u-mt-40-sp")[0].contents[1]),
        "amount": int(c[1])
    }

    # Fix images
    card["text"] = card["text"].replace("/wp/", "https://en.ws-tcg.com/wp/")

    # Print card
    for i in range(card["amount"]):
        print("<div class=\"card\">")
        print(card["text"])
        print("<h1>" + card["name"] + "</h1>")
        print("</div>")

# Close the HTML
print("</body>\n</html>")
