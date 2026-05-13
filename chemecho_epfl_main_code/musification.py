import numpy as np
from midiutil import MIDIFile
import get_spectrum as spect
from translation_ir_to_music import wavenumber_to_midi, molecular_weight_to_sound_code


def find_peaks(wavenumbers, intensities, threshold=80, max_peaks=20):
    """Find absorption dips in a transmittance spectrum (local minima below threshold).

    In transmittance, absorption bands appear as dips (low T = strong absorption).
    threshold is in % transmittance — only dips below it are considered peaks.
    Returns (wavenumber, absorption_strength) where absorption_strength is in [0, 1].
    """
    peaks = []
    for i in range(1, len(intensities) - 1):
        if intensities[i] < threshold and intensities[i] < intensities[i-1] and intensities[i] < intensities[i+1]:
            absorption_strength = (100 - intensities[i]) / 100  # deeper dip = stronger
            peaks.append((wavenumbers[i], absorption_strength))

    # keep only the strongest absorptions
    peaks.sort(key=lambda p: p[1], reverse=True)
    peaks = peaks[:max_peaks]
    # play from high wavenumber to low (same order as reading an IR spectrum)
    peaks.sort(key=lambda p: p[0], reverse=True)
    return peaks


def spectrum_to_midi(cas: str, output_file: str = "output.mid", bpm: int = 120):
    """Convert the IR spectrum of a compound (by CAS) into a MIDI file.

    Each peak in the spectrum becomes one note:
      - wavenumber  -> pitch (higher wavenumber = higher note)
      - intensity   -> velocity (stronger peak = louder)
      - instrument  -> chosen by molecular weight
    """
    wavenumbers, intensities = spect.get_wavenumbers_and_intensities(cas)
    peaks = find_peaks(wavenumbers, intensities)

    instrument = molecular_weight_to_sound_code(cas) - 1  # midiutil is 0-indexed

    midi = MIDIFile(1)
    midi.addTempo(0, 0, bpm)
    midi.addProgramChange(0, 0, 0, instrument)

    beat = 0.0
    for wn, intensity in peaks:
        pitch = wavenumber_to_midi(wn)
        velocity = int(40 + intensity * 70)  # map 0-1 to velocity 40-110
        duration = 0.25 + intensity * 0.5   # stronger peaks held longer
        midi.addNote(0, 0, pitch, beat, duration, velocity)
        beat += duration

    with open(output_file, "wb") as f:
        midi.writeFile(f)

    return output_file
