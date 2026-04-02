# Decklog ripper for bushinavi decks

Decklog ripper for https://decklog-en.bushiroad.com 
Works for english weiss decks. Probably others too but didnt test.

Add a txt file with all decklog codes in the target folder, one decklog code per line.
Will output txt files for each deck with card quantity, card code and card name per line.

Python dependencies are playwright and beautifulsoup4

```
python decklog_ripper.py
```

# Deck Aggregator 

Takes multiple lists created by decklog ripper and averages them

```
python deck_aggregator.py <folder path> <desired name>
```
