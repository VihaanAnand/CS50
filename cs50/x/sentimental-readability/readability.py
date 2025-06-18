text = input("Text: ")
characters = len(text)
letters = 0
for a in text:
    if a.isalpha():
        letters += 1
words = len(text.split())
sentences = 0
for b in text:
    if b == "." or b == "?" or b == "!":
        sentences += 1
lettersPer100 = letters / words * 100
sentencesPer100 = sentences / words * 100
colemanLiau = 0.0588 * lettersPer100 - 0.296 * sentencesPer100 - 15.8 + 0.5
if colemanLiau < 1:
    print("Before Grade 1")
elif colemanLiau >= 16:
    print("Grade 16+")
else:
    print(f"Grade {colemanLiau}")