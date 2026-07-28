import numpy as np

# =========================
# R_D 相關函數定義
# =========================

def diffusion_coefficient(D0, P0, P, T, T0):
    """
    Calculate diffusion coefficient:
    D = D0 * (P0 / P) * (T / T0)^(3/2)

    Units:
    D0: cm^2/s
    P0, P: same pressure unit, e.g. torr
    T0, T: K
    return D: cm^2/s
    """
    return D0 * (P0 / P) * (T / T0) ** 1.5


def diffusion_rate(D, a, geometry):
    """
    Calculate diffusion collision rate.

    Units:
    D: cm^2/s
    a: cm
    return R_D: s^-1
    
    """
    if geometry == "cube":
        return 3 * D * (np.pi / a) ** 2
    elif geometry == "sphere":
        return D * (np.pi / a) ** 2
    else:
        raise ValueError("geometry must be 'cube' or 'sphere'")
    
# =========================
# R_sd 相關函數定義
# =========================

k_B = 1.380649e-23
u = 1.66053906660e-27


def gas_density(P, T):
    """
    Ideal gas density:
    n = P / (k_B T)

    Units:
    P: Pa
    T: K
    return n: m^-3
    """
    return P / (k_B * T)


def reduced_mass(m1, m2):
    """
    Reduced mass:
    mu = m1 m2 / (m1 + m2)

    Units:
    m1, m2: kg
    return mu: kg
    """
    return (m1 * m2) / (m1 + m2)


def thermal_relative_velocity(T, mu):
    """
    Mean relative thermal velocity:
    v = sqrt(8 k_B T / (pi mu))

    Units:
    T: K
    mu: kg
    return v: m/s
    """
    return np.sqrt(8 * k_B * T / (np.pi * mu))


def spin_destruction_rate(n_bg, sigma_sd, v):
    """
    R_sd = n_bg * sigma_sd * v

    Units:
    n_bg: m^-3
    sigma_sd: m^2
    v: m/s
    return R_sd: s^-1
    """
    return n_bg * sigma_sd * v

# =========================
# R_se 相關函數定義
# =========================

def spin_exchange_rate(n_Rb, sigma_se, v_rel):
    """
    Spin-exchange collision rate:

    R_se = n_Rb * sigma_se * v_rel

    Units:
    n_Rb: m^-3
    sigma_se: m^2
    v_rel: m/s

    return:
    R_se: s^-1
    """
    return n_Rb * sigma_se * v_rel

# =========================
# R_pr & R_pr 相關函數定義
# =========================

h = 6.62607015e-34
c = 2.99792458e8


def optical_frequency(wavelength):
    """
    Optical frequency:
    nu = c / lambda

    wavelength: m
    return nu: Hz
    """
    return c / wavelength


def resonant_cross_section(wavelength, gamma_nat, delta_nu_total):
    """
    sigma_0 = lambda^2 / (2 pi) * Gamma_nat / Delta_nu_total

    wavelength: m
    gamma_nat: Hz
    delta_nu_total: Hz
    return sigma_0: m^2
    """
    return wavelength**2 / (2 * np.pi) * gamma_nat / delta_nu_total


def detuned_cross_section(sigma_0, delta_nu_total, detuning):
    """
    sigma(Delta) = sigma_0 * (Delta_nu_total / 2)^2 / Delta^2

    sigma_0: m^2
    delta_nu_total: Hz
    detuning: Hz
    return sigma_delta: m^2
    """
    return sigma_0 * (delta_nu_total / 2) ** 2 / detuning**2


def probing_rate(sigma_delta, intensity, frequency):
    """
    R_pr = sigma(Delta) I / (h nu)

    sigma_delta: m^2
    intensity: W/m^2
    frequency: Hz
    return R_pr: s^-1
    """
    return sigma_delta * intensity / (h * frequency)
