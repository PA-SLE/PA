import ctypes
from datetime import datetime
import time


def message(title, text, style):
    """
    Styles:
    0 : OK
    1 : OK | Cancel
    2 : Abort | Retry | Ignore
    3 : Yes | No | Cancel
    4 : Yes | No
    5 : Retry | Cancel 
    6 : Cancel | Try Again | Continue

    Return will be the button that was clicked
    count starts at 1 and not zero
    """
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def check_time(item, config, current_time):
    """
    Check whether the passed in item is due
    """
    hour = current_time.hour
    minute = current_time.minute
    if hour == config['hour'] and minute == config['minute']:
        text = config.get('text', '')
        message(
            title=TITLE,
            text=f'{item}\n{text}',
            style=0
        )
        reminder_issued = True
    elif hour > config['hour'] and minute > config['minute']:
        print(item, 'has already occured, skipping reminder')
        reminder_issued = True
    else:
        reminder_issued = False
        print(item, 'Condition not met')
    return reminder_issued


if __name__ == '__main__':
    TITLE = 'Sunday Service Setup Reminders'
    times = {
        'Start streaming for first service': {
            'hour': 8,
            'minute': 40,
            'text': ''
        },
        'Setup overflow room': {
            'hour': 10,
            'minute': 18,
            'text': 'Sunday school should be all packed up at 10:20'
        },
        'Ring bell': {
            'hour': 10,
            'minute': 20,
            'text': 'Ring bell for longer at 10:25 as well'
        },
        'Start streaming for second service': {
            'hour': 11,
            'minute': 10,
            'text': ''
        }
    }
    response = message(
        title=TITLE,
        text='''Make sure there are some batteries in the charger or charged
Click cancel if not Sunday''',
        style=1
    )

    if response == 2:
        # User clicked Cancel
        # Stop reminders
        message(
            title=TITLE,
            text='Reminders stopped',
            style=0
        )
    else:
        # Continue 

        # Get current time
        date_time = datetime.now()
        print(date_time)
        for item, config in times.items():
            print('Waiting for the time to', item)
            reminder_issued = False
            while reminder_issued is False:
                date_time = datetime.now()
                reminder_issued = check_time(item, config, date_time)
                time.sleep(30)
            print('Moving on to next item')

