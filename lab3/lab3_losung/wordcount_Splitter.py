import Splitter as sp
import Mapper as mp
import Reducer as rd

import constPipe as const

splitter = sp.Splitter()

with open("wordcount.txt") as txt:
    text = txt.read()

splitter.initWordCount(text)

splitter.start()
