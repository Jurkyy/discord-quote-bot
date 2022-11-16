import random


def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == 'hello' or p_message == 'hi':
        return 'Hey there!'

    if message == 'roll':
        return str(random.randint(1, 6))

    if p_message == 'help':
        return 'Probeer wat leuks te zeggen, misschien beledig ik Luc :smiling_imp:\nMet `?` maak je een command of bericht privé.\n\nCommands:\n\t`!quote`\n\t`!knapste`\n\t`!hello` OF `!hi`\n\t`!roll`\n\nEn natuurlijk ook paar hidden commands :wink:'

    if p_message == 'knapste':
        return 'Abdellos'

    if p_message == 'lellijkste':
        return 'Luc'

    if p_message == 'keyphrase is not in quotes':
        return 'Gast, er is helemaal geen quote met dit woord... :pensive:'
