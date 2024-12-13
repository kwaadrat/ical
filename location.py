import re
from icalendar import Calendar, Event

def add_location(ical_file):
    """
    Dodaje parametr LOCATION do wydarzeń w pliku iCalendar,
    wyciągając wartość z pola "Sala". Używa wyrażenia regularnego
    dla bardziej elastycznego parsowania.

    Args:
        ical_file (str): Ścieżka do pliku wejściowego.

    Returns:
        str: Ścieżka do pliku wyjściowego.
    """

    with open(ical_file, 'rb') as f:
        cal = Calendar.from_ical(f.read())

    for component in cal.walk():
        if component.name == "VEVENT":
            description = component.get('DESCRIPTION')
            match = re.search(r"Sala:\s*(.*)", description, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                component.add('location', location)

    # Zapisujemy plik wyjściowy w tym samym katalogu co plik wejściowy
    output_file = ical_file.replace(".ics", "_with_location.ics")
    with open(output_file, 'wb') as f:
        f.write(cal.to_ical())

    return output_file