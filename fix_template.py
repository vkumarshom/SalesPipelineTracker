#!/usr/bin/env python3

with open('templates/booking/calendar.html', 'r') as file:
    content = file.read()

# Replace notes field
content = content.replace(
    '{{ form.notes(class="form-control" + (" is-invalid" if form.notes.errors else ""), rows="3", placeholder="Any specific topics or questions you\'d like to address in your reading?") }}',
    '{{ form.notes }}'
)

with open('templates/booking/calendar.html', 'w') as file:
    file.write(content)

print("Template fixed successfully.")