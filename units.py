# =========================
# R_D 相關函數定義
# =========================

def temperature_to_K(value, unit):
    if unit == "K":
        return value
    if unit == "°C":
        return value + 273.15
    raise ValueError(f"Unknown temperature unit: {unit}")


def pressure_to_torr(value, unit):
    if unit == "torr":
        return value
    if unit == "Pa":
        return value / 133.322
    if unit == "atm":
        return value * 760
    raise ValueError(f"Unknown pressure unit: {unit}")


def length_to_cm(value, unit):
    if unit == "cm":
        return value
    if unit == "mm":
        return value / 10
    if unit == "m":
        return value * 100
    raise ValueError(f"Unknown length unit: {unit}")


# =========================
# R_sd 相關函數定義
# =========================

def area_to_m2(value, unit):
    if unit == "m²":
        return value
    if unit == "cm²":
        return value * 1e-4
    raise ValueError(f"Unknown area unit: {unit}")


def mass_to_kg(value, unit):
    if unit == "kg":
        return value
    if unit == "u":
        return value * 1.66053906660e-27
    raise ValueError(f"Unknown mass unit: {unit}")


def pressure_to_pa(value, unit):
    if unit == "Pa":
        return value
    if unit == "torr":
        return value * 133.322
    if unit == "atm":
        return value * 101325
    raise ValueError(f"Unknown pressure unit: {unit}")

# =========================
# R_pr 相關函數定義
# =========================
def wavelength_to_m(value, unit):
    if unit == "m":
        return value
    if unit == "nm":
        return value * 1e-9
    if unit == "μm":
        return value * 1e-6
    raise ValueError(f"Unknown wavelength unit: {unit}")


def frequency_to_hz(value, unit):
    if unit == "Hz":
        return value
    if unit == "MHz":
        return value * 1e6
    if unit == "GHz":
        return value * 1e9
    raise ValueError(f"Unknown frequency unit: {unit}")


def intensity_to_w_per_m2(value, unit):
    if unit == "W/m²":
        return value
    if unit == "mW/cm²":
        return value * 10
    raise ValueError(f"Unknown intensity unit: {unit}")