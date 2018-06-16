
def emotion_data_to_class(valence: int, arousal: int) -> str:
    if valence < 3.0:
        if arousal < 3.0:
            return "VL_AL"
        elif 3.0 <= arousal < 6.0:
            return "VL_AM"
        else:
            return "VL_AH"
    elif 3.0 <= valence < 6.0:
        if arousal < 3.0:
            return "VM_AL"
        elif 3.0 <= arousal < 6.0:
            return "VM_AM"
        else:
            return "VM_AH"
    else:
        if arousal < 3.0:
            return "VH_AL"
        elif 3.0 <= arousal < 6.0:
            return "VH_AM"
        else:
            return "VH_AH"