# walfie-gif-dl
Download GIFs on https://walfiegif.wordpress.com/.

All credit goes to [Walfie](https://social.aikats.us/) for drawing the GIFs.

View GIFs by category [here](categories.md).

<img src="gifs/ameJAM.gif" height="360">

## Usage
Requirements
- Python 3.7+
- [geckodriver](https://github.com/mozilla/geckodriver/releases) 0.30+ (add it to PATH)

Install dependencies
```bash
pip install -Ur requirements.txt
```

Fetch GIF data
```bash
python fetch.py
```

Download GIFs
```bash
python download.py
```

Generate [categories.md](categories.md)
```bash
python categorize.py
```
