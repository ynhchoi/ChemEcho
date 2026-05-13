import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "chemecho_epfl_main_code"))

from get_spectrum import extract_spectrum_data, ir_graph
#from ..chemecho_epfl_main_code.musification import 

def test_extract_spectrum_data():
    #test with a CAS number that 
    assert pytest.approx(extract_spectrum_data('74-85-1')[1][0,10],abs=0.01) == [92.9, 92.9, 92.9, 92.9, 92.9, 92.9, 93.0, 93.0, 93.0, 93.22]
    #test with a CAS number that raise a ValueError
    assert extract_spectrum_data('118-96-7') == "Could not find a spectrum for Trinitrotoluene or Trinitrotoluene has an IR spectrum with y units not convertible in Transmittance"
    #test with a CAS number that use the recursive call of the function
    assert pytest.approx(extract_spectrum_data('')[1][0,10],abs=0.01) == []

def test_ir_graph():
    with open(ir_graph(extract_spectrum_data('58-08-2')), "r") as file1, open("caffeine_ir.svg", "r") as file2:
        assert file1.read() == file2.read()