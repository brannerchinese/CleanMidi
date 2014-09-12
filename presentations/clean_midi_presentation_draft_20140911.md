# Transcribing a Solo Voice Recording

# to Western Musical Notation

---

## This talk describes a failed attempt

---

Goal: transcribe melody automatically.

---

Recording is of Taiwanese cantillation: read classical poem in "reading pronunciation" (different from spoken language), elaborate the tones of the words into a melody

---

Recording, 1-8.

![Lines 1-8 of Bái Jūyì 白居易, "Pípá xíng" 琵琶行, sung by Hsü Yi-t'ing 許禕娗](../recordings/白居易、琵琶行並序_lines_01-08_n_1024.mp3)

---

After many experiments, settled on WaoN  to convert audio into MIDI. Heard here converted to MP3 by FluidSynth.

---

Play 1.

---

Terrible. Tremolo in the voice and reverb in the recording lead to chords or trills in MIDI transcription.

---

Idea: can we clean MIDI with Python?

---

There are MIDI modules for Python, but I felt a purer approach would be to convert MIDI to text and discard all but the notes with highest "velocity" (qqq define)

---

Play 1-2.

---

Also terrible. It was shown by Georg Cantor a century ago that there is no natural upper bound on the number of terrible things that can exist in the universe.

---

Panicked solution: hire a professional transcriber to transcribe it for me.

---

Play 1-2.

---

Further evidence of Cantor's conclusion.

---

Finally, used MuseScore to transcribe manually.

---

Much easier than I thought it would be.


---

# 劇終

----

## Background Images

### If you put text on top of an image, the image is _**filtered**_ so the text is always readable. 

---

# Isn’t that **great?**

![](http://deckset-assets.s3-website-us-east-1.amazonaws.com/colnago2.jpg)

---

# You can also turn the filter off.

![original](http://deckset-assets.s3-website-us-east-1.amazonaws.com/colnago2.jpg)


---


---

