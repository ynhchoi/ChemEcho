import nistchempy as nist
from jcamp import jcamp_readfile
import tempfile
import os
from ir_spectra_conversion import normalize_to_transmittance


def _pick_best_spec(ir_specs):
    """Pick the best spectrum: prefer TRANSMITTANCE, then ABSORBANCE, then fallback to first."""
    for preferred in ['TRANSMITTANCE', 'ABSORBANCE']:
        for spec in ir_specs:
            if f'YUNITS={preferred}' in spec.jdx_text.upper():
                return spec
    return ir_specs[0]


def extract_spectrum_data(cas: str):
    """Fetch IR spectrum data from NIST for a given CAS number.
    Returns a jcamp dict with 'x' (wavenumbers) and 'y' (transmittance 0-100%).
    """
    X = nist.get_compound(cas)
    X.get_ir_spectra()
    X_IR = _pick_best_spec(X.ir_specs)
    jdx_content = X_IR.jdx_text

    # we need a tempfile because jcamp_readfile only reads from disk
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jdx', delete=False) as f:
        f.write(jdx_content)
        temp_path = f.name

    data = jcamp_readfile(temp_path)
    os.remove(temp_path)
    return normalize_to_transmittance(data)


def get_wavenumbers_and_intensities(cas: str):
    """Convenience wrapper that returns (wavenumbers, transmittance) directly."""
    data = extract_spectrum_data(cas)
    return data['x'], data['y']
