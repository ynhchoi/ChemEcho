import nistchempy as nist
from jcamp import jcamp_readfile
import tempfile
import os

def extract_spectrum_data(cas:str):
    X = nist.get_compound(cas)
    X.get_ir_spectra()
    X.ir_specs
    X_IR = X.ir_specs[0]
    jdx_content = X_IR.jdx_text

    # here we need a tempfile bc the data is in a jdx that we need to go through to extract the data
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jdx', delete=False) as f:
        f.write(jdx_content)
        temp_path = f.name

    data = jcamp_readfile(temp_path)
    os.remove(temp_path)

    data_x = data['x']
    data_y = data['y']

    if data.get('yunits') == "Absorbance" or data.get('yunits') == "ABSORBANCE" :
        for i in range(0, len(data_y)):
            data_y[i] = 10**(-data_y[i])
    elif data.get('yunits') == "Transmittance" or data.get('yunits') == "TRANSMITTANCE" :
        pass
    else :    
        raise ValueError(f"{X.name} has an IR spectrum with y units not convertible in Transmittance")

    return data_x, data_y
"""
print(extract_spectrum_data('74-85-1').get('yunits'))
X = nist.get_compound('74-85-1')
X.get_ir_spectra()
X.ir_specs
X_IR = X.ir_specs[0]
jdx_content = X_IR.jdx_text
print(type(X.ir_specs))
print(type(jdx_content))
print(len(X.ir_specs))
"""