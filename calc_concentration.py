def calculate_concentration(num_molecules):
    avogadro_number = 6.023e23  # molecules/mol
    volume_micrometer_cubed = 0.017  # μm³
    micrometer_cubed_to_liters = 1e-15  # μm³ to L

    moles = num_molecules / avogadro_number
    volume_liters = volume_micrometer_cubed * micrometer_cubed_to_liters
    concentration_M = moles / volume_liters
    concentration_uM = concentration_M * 1e6 

    return concentration_uM

num_molecules = 55

concentration = calculate_concentration(num_molecules)
print(f"Concentration: {concentration:.3e} μM")