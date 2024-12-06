def calculate_energy_usage(electricity, gas, fuel):
    """Calculates electricity, natural gas and fuel usage."""

    return (
        electricity * 12 * 0.0005 +
        gas * 12 * 0.0053 +
        fuel * 12 * 2.32
    )

def calculate_waste(waste, recycling_percentage):

    """Calculates the amount of waste and recycling."""
    return (
        waste * 12 * 0.57 -
        (waste * 12 * (recycling_percentage / 100) * 0.57)
    
    )

def calculate_business_travel(kilometers, fuel_efficiency):
    
    """ Calculates the carbon footprint from business travel. """
    
    return (
        kilometers * (1 / fuel_efficiency) *2.31
    )