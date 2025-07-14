import wave

with wave.open('audio_recordings/server/a.wav', 'rb') as w:
    if w.getnchannels() == 1:
        print("mono")
    else:
        print("stereo / multichannel")
    print(w.getframerate())
    print(w.getnchannels())
    print(w.getsampwidth())
    print(w.getnframes())
    print(w.getcomptype())
    print(w.getcompname())
    print(w.getparams())
    print(w.getnframes())

with wave.open('audio_recordings/server/b.wav', 'rb') as w:
    if w.getnchannels() == 1:
        print("mono")
    else:
        print("stereo / multichannel")
    print(w.getframerate())
    print(w.getnchannels())
    print(w.getsampwidth())
    print(w.getnframes())
    print(w.getcomptype())
    print(w.getcompname())
    print(w.getparams())
    print(w.getnframes())

with wave.open('audio_recordings/server/c.wav', 'rb') as w:
    if w.getnchannels() == 1:
        print("mono")
    else:
        print("stereo / multichannel")
    print(w.getframerate())
    print(w.getnchannels())
    print(w.getsampwidth())
    print(w.getnframes())
    print(w.getcomptype())
    print(w.getcompname())
    print(w.getparams())
    print(w.getnframes())

with wave.open('audio_recordings/server/d.wav', 'rb') as w:
    if w.getnchannels() == 1:
        print("mono")
    else:
        print("stereo / multichannel")
    print(w.getframerate())
    print(w.getnchannels())
    print(w.getsampwidth())
    print(w.getnframes())
    print(w.getcomptype())
    print(w.getcompname())
    print(w.getparams())
    print(w.getnframes())