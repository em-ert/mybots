import sf2_loader as sf

def Create_Synth():
    loader = sf.sf2_loader("default-GM.sf2")
    loader.change(bank=128, preset=8)
    
    return loader