from icalendar import Calendar, Event
import re

def add_location_to_ical(ical_file, output_file):
    """
    Dodaje parametr LOCATION do wydarzeń w pliku iCalendar,
    wyciągając wartość z pola "Sala". Używa wyrażenia regularnego
    dla bardziej elastycznego parsowania.

    Args:
        ical_file (str): Ścieżka do pliku wejściowego.
        output_file (str): Ścieżka do pliku wyjściowego.
    """

    with open(ical_file, 'rb') as f:
        cal = Calendar.from_ical(f.read())

    for component in cal.walk():
        if component.name == "VEVENT":
            description = component.get('DESCRIPTION')
            # Wyrażenie regularne: dopasuj "Sala:" z dowolną liczbą spacji i dowolną wartością
            match = re.search(r"Sala:\s*(.*)", description, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                component.add('location', location)

    with open(output_file, 'wb') as f:
        f.write(cal.to_ical())

# Przykład użycia
ical_file = "Plany.ics"
output_file = "moj_plan_z_lokalizacja.ics"
add_location_to_ical(ical_file, output_file)