import nistchempy as nist


def wavenumber_to_midi(wavenumber: float) -> int:
    """Map an IR wavenumber (cm-1) to a MIDI note number.

    IR spectra range from ~400 to 4000 cm-1. We map this linearly
    to MIDI pitches 40-90 (E2 to D6), which fits comfortably within
    the audible range and most instrument timbres.
    Higher wavenumber = higher pitch (faster vibration = higher note).
    """
    midi = int((wavenumber - 400) / (4000 - 400) * (90 - 40) + 40)
    return max(40, min(90, midi))


def molecular_weight_to_sound_code(compound_cas: str) -> int:
    """Assign a General MIDI instrument number based on molecular weight.

    Lighter molecules tend to vibrate faster, so we assign
    higher-pitched instruments to smaller compounds.
    Instrument codes follow General MIDI standard (1-indexed).
    """
    compound = nist.get_compound(compound_cas)
    mw = compound.mol_weight

    if mw < 50:
        return 74   # flute
    elif mw < 100:
        return 72   # clarinet
    elif mw < 200:
        return 43   # cello
    elif mw < 300:
        return 67   # tenor sax
    else:
        return 44   # contrabass
