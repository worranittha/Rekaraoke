# Rekaraoke
Thai to English Transliteration

The propose of this project is to search a song's name from a Thai transliteration lyric.

There are 2 model for transforming a Thai transliteration to a English lyric:

    1. IPA-based integration model
        This model consists of 4 stages:
        
            - Tokenization
            - Thai transliteration to IPA
            - IPA to English sentence
            - Spelling correction
            
    2. End-to-End model

Then, we search a song's name using Genius API.

**The demo website for searching song is available in the demo folder ^_^.**
