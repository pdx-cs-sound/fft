import argparse, scipy
import numpy as np
import scipy.io.wavfile as wav

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--volume", help="volume 0..10", type=float, default=8)
ap.add_argument("-o", "--output", help="output file")
ap.add_argument("-f", "--frequency", type=float, default=1000)
ap.add_argument("signal", help="signal type", choices=["sine", "saw-rise", "saw-fall"])
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

if args.signal == "sine":
    s = np.sin(2 * np.pi * frequency * t)
elif args.signal == "saw-rise":
    nseg = int(sample_rate / frequency)
    seg = np.linspace(-1, 1, nseg)
    s = np.tile(seg, int(nsamples / nseg))
elif args.signal == "saw-fall":
    nseg = int(sample_rate / frequency)
    seg = np.linspace(1, -1, nseg)
    s = np.tile(seg, int(nsamples / nseg))
else:
    assert False

a = min(0.1 * args.volume, 1)
a = 0.1 * np.power(10, a)
wav.write(args.output, sample_rate, (a * s * (1 << 15)).astype(np.int16))
