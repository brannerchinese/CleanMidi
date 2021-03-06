## Produce and clean a MIDI file from an audio recording

**Problem**: Given a recording of solo voice singing, produce a clean MIDI version of it, from which transcription in traditional musical notation can be produced.

**Summary**: Tremolo in the singer's voice and slight reverberation in the recordings make this a hard, hard business. A base MIDI file is produced with WaoN and then processed with a Python script. There are Python modules for manipulating MIDI directly, but I didn't know about those at the time I did this little project.

The script must be counted a failure, but I learned quite a lot by writing it. The results are actually somewhat better using WaoN output directly. I suspect I will have better results transcribing manually — computer-aided transcription seems the best way to proceed.

### Non-Python requirements

 1. [WaoN](https://github.com/kichiki/WaoN) for converting `.wav` to `.mid` (MIDI). (Available through HomeBrew.) Note that SoX does not currently support conversion to MIDI. WaoN renders 和音 'chord' or 'melodious sounds' in Japanese (also 'Japanese sounds').
 1. [MIDICSV](http://www.fourmilab.ch/webtools/midicsv/) (includes CSVMIDI) for conversion between `.mid` MIDI files and text-editable `.csv` files. (Available through HomeBrew.)
 1. [FluidSynth](https://sourceforge.net/apps/trac/fluidsynth/): generate raw soundfile from a MIDI. Requires a SoundFont; to prepare that:
     1. Download [`GeneralUser` SoundFont](http://www.schristiancollins.com/generaluser.php).
     1. Rename file `GeneralUser GS FluidSynth v1.44.sf2` to `GeneralUser_GS_FluidSynth_v1.44.sf2` and move it to location of `fluidsynth` install (which is a symlink, so follow that link to the directory's true location).
 1. [SoX (Sound eXchange](http://sox.sourceforge.net/): convert raw sound file to `.wav`, `.mp3`, etc.

### Background on MIDI format

 1. http://www.midi.org/techspecs/midimessages.php
 1. http://www.sonicspot.com/guide/midifiles.html

### Steps

 1. Convert `.wav` to `.mid`:

        waon -i recording.wav -o output.mid

   Note that there are many options for WaoN. I have used `-n` to select note-length and `-t` and `-b` to restrict the transcribed range to what appears to be the actual range used by the singer in this recording:

        waon -n 8192 -t 67 -b 52 \
        -i recordings/16_白居易、琵琶行並序、許禕娗_chanting_lines_01-08.wav \
        -o midi/16_白居易、琵琶行並序、許禕娗_chanting_lines_01-08_n_8196_t_67_b_52.mid

   But bear in mind that when restricting the transcribed range I have had segmentation faults with lower values of `-n`, which otherwise give more interesting results.

   Output looks like this:

        $ waon -n 1024 \
        -i recordings/16_白居易、琵琶行並序、許禕娗_chanting_lines_01-08.wav \
        -o midi/16_白居易、琵琶行並序、許禕娗_chanting_lines_01-08_n_1024.mid
        Format: Microsoft WAV format (little endian default).
        Subtype: Signed 16 bit data
        Endian type: Default file endian-ness.
        frames     : 2161441
        samplerate : 44100
        channels   : 2
        sections   : 1
        seekable   : 1
        WaoN : end of file.
        division = 86
        WaoN : # of events = 2120
        WAON_notes : n = 2120
        filename : midi/16_白居易、琵琶行並序、許禕娗_chanting_lines_01-08_n_1024.mid
        $ 

 1. Convert `.mid` to editable `.csv`:

        midicsv output.mid > output.mid.csv

 1. Run `clean_midi.py`, to isolate only the highest-velocity note at any time-tick:

        python code/clean_midi.py <filename.csv>

   or

        python code/clean_midi.py

   for default input filename `output.csv` and output `output_edited.csv`. Program looks in directory `midi` for these files, so don't include the directory name in your input.

 1. Convert `.csv` to `.mid`:
 
        csvmidi midi/output_edited.csv > midi/output.csv.mid

   Some errors may be generated here of the form "Events out of order; this event is before the previous..". I have not yet looked at what is causing this.

 1. Play MIDI file:

        fluidsynth -i <soundfont> <MIDI file>

 1. Optionally, to convert the MIDI file to `.wav` etc.:

        fluidsynth -i <soundfont> <MIDI file> -F <raw_file.raw>
        sox -t raw -r 44100 -e signed -b 16 -c 1 <raw_file.raw> <sound_file.wav>

   or

        sox -t raw -r 44100 -e signed -b 16 -c 1 <raw_file.raw> <sound_file.mp3>

   But `sox` with these settings seems to change the pitch and speed of files, so they may need revision. 
   
   On my system (Mac OS 10.9.4) I always specify the `soundfont` as `/usr/local/Cellar/fluid-synth/1.1.6/include/fluidsynth/GeneralUser_GS_FluidSynth_v1.44.sf2`. FluidSynth plus this long option-input can be saved to an alias or written into a script.

### Last reflections

What I have heard so far is poor, but actually better than hand-transcribed material I paid for for comparison. (Possibly the transcriber was also using automated processes.) I frankly think the WaoN output without Python processing is less bad than it — see for instance

 * `midi/16_白居易、琵琶行並序、許禕娗_chanting_lines_01-08_n_1024_s_512.mid`
 * `midi/16_白居易、琵琶行並序、許禕娗_chanting_lines_01-08_n_1024.mid`
 * `midi/16_白居易、琵琶行並序、許禕娗_chanting_lines_01-08_n_8196_t_67_b_52.mid`. 

[end]
