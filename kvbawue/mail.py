import re
from pprint import pprint

def reverseEmails(hrefsearch, href, textsearch, text):
    # // Only if htef is obfuscated.
    if hrefsearch.group():
        # // That"s the reversing part right here.
        # element.setAttribute("href", href.split("").reverse().join("") );
        foo = "".join(href.split("").reverse())
        print(foo)
        return foo
    # // Only if text is obfuscated.
    if textsearch.group():
        # // Reverse the text of the element and    //    return the    direction    to    normal(left    to    right).
        foo = "".join(text.split("").reverse())
        print(foo)
        return foo


def deObfuscateEmail(text, href):
    textsearch = re.search('@.+@', text)
    hrefsearch = re.search('@.+@', href)

    if hrefsearch.group():
        href = changeLetters(href)
        print(href)
        return href
    if textsearch.group():
        text = changeLetters(text)
        print(text)


def changeLetters(string):
    stringLength = len(string)
    currentString = ""
    characters = tuple(list("123456789qwertzuiopasdfghjklyxcvbnmMNBVCXYLKJHGFDSAPOIUZTREWQ"))
    charactersLength = len(characters)
    for i in range(0, stringLength-1):
        currentLetter = string[i]
        try:
            currentPos = characters.index(currentLetter)
            currentPos -= int((charactersLength - 1) // 2)
            if currentPos < 0:
                currentPos += charactersLength
            currentString += characters[currentPos]
        except ValueError:
            currentString += currentLetter
    return currentString

def deText(text):
    return changeLetters(text)[::-1]


