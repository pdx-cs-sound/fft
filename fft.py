import argparse, numpy, sounddevice, struct, sys, wave
from scipy import fft

ap = argparse.ArgumentParser()
ap.add_argument(
    "-b", "--blocksize",
    help="block size in frames",
    type=int,
    default = 4096,
)
ap.add_argument(
    "-o", "--outfile",
    help="output file",
)
ap.add_argument(
    "wavfile",
    help="wav input file",
)
args = ap.parse_args()

blocksize = args.blocksize

# Read a wave file.
def read(filename):
    with wave.open(filename, "rb") as w:
        assert w.getnchannels() == 1
        assert w.getsampwidth() == 2
        nframes = w.getnframes()
        frames = w.readframes(nframes)
        framedata = struct.unpack(f"<{nframes}h", frames)
        samples = [s / (1 << 15) for s in framedata]
        return w.getparams(), samples, w.getframerate()

# Collect the samples.
params, samples, sample_rate = read(args.wavfile)

# Write a data file.
def write(samples, params):
    nframes = len(samples)
    framedata = [int(numpy.abs(s) * (1 << 15)) for s in samples]
    with open(args.outfile, "w") as f:
        for fr in framedata:
            print(fr, file=f)

# Build the window.
lap = int(0.1 * blocksize)
trap1 = numpy.linspace(0, 1, lap, endpoint=False)
trap2 = numpy.ones(blocksize - 2 * lap)
trap3 = 1 - trap1
window = numpy.append(trap1, trap2)
window = numpy.append(window, trap3)

# Run the filter.
freqs = fft.rfft(samples, blocksize)
write(freqs, params)
