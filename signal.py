import argparse, scipy
import numpy as np
import scipy.io.wavfile as wav

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--volume", help="volume 0..10", type=float, default=8)
ap.add_argument("-o", "--output", help="output file")
ap.add_argument("-f", "--frequency", help="fundamental frequency", type=float, default=1000)
ap.add_argument("-p", "--phase", help="initially rise or fall", choices=["rise", "fall"], default="rise")
ap.add_argument("-a", "--algorithm", help="saw algorithm", choices=["segments", "mod", "floor"], default="floor")
ap.add_argument("signal", help="signal type", choices=["sine", "saw"])
ap.add_argument("duration", help="seconds to play", type=float)
args = ap.parse_args()

sample_rate = 48_000
nsamples = int(sample_rate * args.duration)
t = np.linspace(
    0,
    args.duration,
    nsamples,
    dtype=np.float64,
)
frequency = args.frequency

def saw(t, f, algorithm):
    if algorithm == "segments":
        nseg = int(sample_rate / f)
        seg = np.linspace(-1, 1, nseg)
        s = np.tile(seg, int(nsamples / nseg))
    elif algorithm == "mod":
        s = (t * 2.0 * frequency) % 2.0 - 1.0
    elif algorithm == "floor":
        # https://en.wikipedia.org/wiki/Sawtooth_wave
        p = 1.0 / f
        s = 2.0 * (t / p - np.floor(0.5 + t / p))
    else:
        assert False
    return s

if args.signal == "sine":
    s = np.sin(2 * np.pi * frequency * t)
elif args.signal == "saw":
    s = saw(t, frequency, args.algorithm)
else:
    assert False

if args.phase == "rise":
    pass
elif args.phase == "fall":
    s = -s
else:
    assert False

a = min(0.1 * args.volume, 1)
a = 0.1 * np.power(10, a)
wav.write(args.output, sample_rate, (a * s * (1 << 15)).astype(np.int16))
