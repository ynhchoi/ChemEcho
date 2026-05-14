import matplotlib.pyplot as plt
import pandas as pd
import nistchempy as nist


def ir_graph(dict_spectrum, cas_number):
    """Plot an IR spectrum. dict_spectrum is the jcamp dict from extract_spectrum_data."""
    df_spectrum = pd.DataFrame({
        "Wavenumber": dict_spectrum['x'].tolist(),
        "Transmittance": dict_spectrum['y'].tolist()
    })

    compound = nist.get_compound(cas_number)

    fig, ax = plt.subplots()
    ax.plot(df_spectrum["Wavenumber"], df_spectrum["Transmittance"], color="black")
    ax.set_xlabel("Wavenumber (cm⁻¹)")
    ax.set_ylabel("Transmittance (%)")
    ax.set_title(f"IR spectrum of {compound.name}")
    ax.grid(visible=False)
    ax.set_xlim(4000, 400)
    ax.set_ylim(0, 100)

    return fig, ax
