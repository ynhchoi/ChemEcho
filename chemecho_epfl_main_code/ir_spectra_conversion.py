import pandas as pd
import numpy as np
from io import StringIO


def normalize_to_transmittance(spectrum_data: dict) -> dict:
    """Convert any NIST IR spectrum to transmittance (0-100%).

    NIST spectra come in three formats:
      - TRANSMITTANCE: already correct, just clip to 0-100
      - ABSORBANCE: convert with T = 100 * 10^(-A)
      - anything else (molar absorptivity, etc.): normalize to [0,1]
        as relative absorbance then apply the same conversion.
        Peak positions are preserved; absolute intensities are meaningless
        anyway for sonification purposes.

    Returns a copy of the dict with 'y' in transmittance (0-100)
    and 'yunits' updated.
    """
    y = spectrum_data['y'].copy().astype(float)
    yunits = str(spectrum_data.get('yunits', '')).upper()

    if 'TRANSMITTANCE' in yunits:
        # some entries use 0-1 instead of 0-100
        if y.max() <= 1.0:
            y = y * 100
        y = np.clip(y, 0, 100)

    elif 'ABSORBANCE' in yunits:
        y = np.clip(y, 0, None)          # absorbance can't be negative
        y = 100 * np.power(10.0, -y)

    else:
        # molar absorptivity or unknown unit: normalize to [0,1] first
        ymax = y.max()
        if ymax > 0:
            y = y / ymax
        y = 100 * np.power(10.0, -y)

    result = dict(spectrum_data)
    result['y'] = y
    result['yunits'] = 'TRANSMITTANCE'
    return result


def spectrum_to_dataframe(spectrum_data: dict) -> pd.DataFrame:
    """Convert a jcamp spectrum dict to a DataFrame with Wavenumber and Transmittance columns."""
    return pd.DataFrame({
        "Wavenumber": spectrum_data['x'],
        "Transmittance": spectrum_data['y']
    })


def from_df_to_csv(df_spectrum: pd.DataFrame) -> str:
    """Export a spectrum DataFrame to a CSV string."""
    buffer_csv = StringIO()
    df_spectrum.to_csv(buffer_csv, index=False)
    return buffer_csv.getvalue()
