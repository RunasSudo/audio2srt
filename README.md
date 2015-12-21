# audio2srt
Generate automatic subtitles from an audio file using PocketSphinx

## Example usage
After installing [PocketSphinx](https://github.com/cmusphinx/pocketsphinx), download the US English Generic Language Model, e.g. [cmusphinx-5.0-en-us.lm.dmp](http://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/US%20English%20Generic%20Language%20Model/), and the US English Generic Acoustic Model, e.g. [cmusphinx-en-us-5.2.tar.gz](http://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/US%20English%20Generic%20Acoustic%20Model/), extracting the latter.

Save your audio as a 16-bit **16kHz mono** wav file.

To let audio2srt handle everything:

    ./audio2srt.py -i audio.wav -o audio.srt -- -lm cmusphinx-5.0-en-us.lm.dmp -hmm en-us

To process with PocketSphinx first then run audio2srt separately:

    pocketsphinx_continuous -infile audio.wav -lm cmusphinx-5.0-en-us.lm.dmp -hmm en-us -time yes > audio.txt
    ./audio2srt.py -t audio.txt -o audio.srt

To achieve better accuracy, you can (and probably should) [adapt](http://cmusphinx.sourceforge.net/wiki/tutorialadapt) the acoustic model to your situation. (I had a better experience with the MAP method than the MLLR method.)
