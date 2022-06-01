# viseme-to-video
This Python module creates video from viseme images and TTS audio output. I created this for testing the sync accuracy between synthesised audio and duration predictions extracted from FastSpeech2 hidden states.

The tool can be run from the command line using the command:

`python viseme_to_video.py`


This repo contains the following resources

**image/**
Two image sets
-- **speaker1/** from [Occulus developer doc 'Viseme reference'](https://developer.oculus.com/documentation/unity/audio-ovrlipsync-viseme-reference/ )
-- **mouth1/** adapted from icSpeech guide ['Mouth positions for English pronunciation'](https://icspeech.com/mouth-positions.html)

A different viseme image directory can be specified on the command line using the flag `--im_dir`.

**metadata/**
'24.json': A viseme metadata JSON file we produced during FastSpeech2 inference by:

- extracting the phoneme sequence produced by the text normalisation frontend module
- mapping this to a sequence of visemes
- extracting hidden state durations (in n frames) from FS2
- converting durations from frames to milliseconds using the formula
- writing this information (phoneme, viseme, duration, offset)

The tool will automatically generate video for all JSON metadata files stored in the `metadata/` folder.


**map/**
'viseme_map.json': A JSON file containing mappings between the visemes in viseme metadata files and the image filenames. Mapping visemes was necessary since the viseme set we use to generate our metadata files contained upper/lower-case distinctions, which file naming doesn't support. (I.e. you can't have two files named 't.jpeg' and 'T.jpeg' stored in the same folder.)

A different mapping file can be specified on the command line using the flag `--map`.


**audio/**
'24.wav' -  An audio sample generated from FastSpeech2 ([using kan-bayashi's ESPnet framework](https://github.com/espnet/espnet). This sample uses a [Harvard sentence](https://harvardsentences.com/) as text input (list 3, sentence 5: 'The beauty of the view stunned the young boy') .

A different mapping file can be specified on the command line using the flag `--map`
Video can be generated without adding audio, by adding the argument `--add_audio False` on the command line.

- insert gif here