

"""
Module of task number 00
"""
from flask import Flask
from typing import List



attendees = [
    {"name": "Alice", "event_title": "Python Conference", "event_date": "2023-07-15", "event_location": "New York"},
    {"name": "Bob", "event_title": "Data Science Workshop", "event_date": "2023-08-20", "event_location": "San Francisco"},
    {"name": "Charlie", "event_title": "AI Summit", "event_date": None, "event_location": "Boston"}
]

campos = ['name', 'event_title', 'event_date', 'event_location']

def generate_invitations(template:str, attendees: List):
    """
    Generate invitations based on a template and the attendees
    """
    if not isinstance(template, str):
        print('Template is empty, no output files generated')
        return

    elif len(template) == 0:
        print('Template is empty, no output files generated')
        return

    if not isinstance(attendees, List):
        print('No data provided, no output files generated.')
        return

    elif len(attendees) == 0:
        print('No data provided, no output files generated.')
        return

    dics = [isinstance(dic, dict) for dic in attendees]
    if all(dics) == False:
        print('No data provided, no output files generated.')
        return

    for index, dic in enumerate(attendees, start=1):
        text = template
        for campo in campos:
            value = dic.get(campo)
            if value == None:
                value = 'N/A'
            text = text.replace(f"{{{campo}}}", str(value))

        with open(f"output_{index}.txt", "w") as f:
            f.write(text)


if __name__ == '__main__':
    generate_invitations()
