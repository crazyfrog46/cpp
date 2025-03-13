# irene2/utils/weather_icons.py

def get_weather_icon_and_bg(weather_description):
    """
    Returns the corresponding weather icon and background color based on the weather description.
    
    Args:
    weather_description (str): The description of the weather condition (e.g., "clear", "rainy", etc.).
    
    Returns:
    tuple: A tuple containing the weather icon and background color.
    """
    # Map weather descriptions to icons and background colors
    mapping = {
        "clear": ("☀️", "#87CEEB"),  # Sun icon and sky blue background
        "rainy": ("🌧️", "#5F9EA0"),  # Rain icon and light sea green background
        "snowy": ("❄️", "#ADD8E6"),   # Snowflake icon and light blue background
        "cloudy": ("☁️", "#D3D3D3"),  # Cloud icon and light gray background
        "stormy": ("🌩️", "#B0C4DE"),  # Lightning icon and light steel blue background
        "foggy": ("🌫️", "#A9A9A9"),   # Fog icon and dark gray background
    }

    # Default icon and background for unknown conditions
    default = ("🌈", "#FFD700")  # Rainbow icon and gold background

    # Return the appropriate icon and background color or the default
    return mapping.get(weather_description.lower(), default)
