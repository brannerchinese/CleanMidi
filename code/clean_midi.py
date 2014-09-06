#! /usr/bin/env python
# clean_midi.py
# David Prager Branner
# 20140905, works.

"""Clean MIDI-CSV file: retain the note with highest velocity at any time."""

import sys
if sys.version_info.major < 3:
    print('Python 3 is required. You are using {}.{}.'.
            format(sys.version_info.major, sys.version_info.minor))
    sys.exit()
import os
import heapq as H
import pprint

def main(filename='output.csv'):
    with open(os.path.join('midi', filename), 'r') as f:
        content = f.read()
    # Extract only lines containing "Note_" and store in "received_events".
    received_events = [tuple(item.split(', '))
            for item in content.split('\n')
            if 'Note_' in item]
    received_events = [tuple(item) for item in received_events]
    # Redefine "received_events" as list of lists of tuples w/ same element 0.
    same_time_events = []
    for event in received_events:
        if same_time_events and (same_time_events[-1][0][1] == event[1]):
            same_time_events[-1].extend([event])
        else:
            same_time_events.append([event])
    #
    # Main loop.
    current_events = []
    final_melody = []
    current_note = None
    note_lookup = {}
    # Step through times
    for events in same_time_events:
        for event in events:
            # If an off-item, remove from "current_events".
            if event[2] == 'Note_off_c':
                current_events.remove(note_lookup.pop(event[4]))
            # If an on-item, add to "current_events".
            # Use "elif" rather than "else" because there may be other things.
            elif event[2] == 'Note_on_c':
                H.heappush(current_events, event)
                note_lookup[event[4]] = event
        # If highest-velocity item in "events" is not "current":
        # What if two simultaneous events are equally loud?
        if current_events:
            largest = H.nlargest(1, current_events, key=lambda i: i[1])[0]
            if largest != current_note:
                # Add "on" event for new "largest".
                final_melody.append(largest)
                # Create "off" event for "current_note"; add to final_melody.
                # But at index = 0, there is no "current_note" yet.
                if current_note:
                    off_event = (
                            '1', largest[1], 'Note_off_c', '0',
                            current_note[4], '64')
                    final_melody.append(off_event)
                # Assign new highest-velocity value to "current_note".
                current_note = largest
    # Finally, last "off" event must occur at actual time in original.
    final_time = events[-1][1]
    off_event = ('1', final_time, 'Note_off_c', '0', current_note[4], '64')
    final_melody.append(off_event)
    # Create string for saving to file.
    head = ('''0, 0, Header, 0, 1, 10\n'''
            '''1, 0, Start_track\n'''
            '''1, 0, Tempo, 500000\n'''
            '''1, 0, Program_c, 0, 0\n''')
    tail = ('1, ' + final_time + ''', End_track\n'''
            '''0, 0, End_of_file\n''')
    body = '\n'.join([', '.join(event) for event in final_melody])
    content = head + body + '\n' + tail
    filename = filename.split('.')[0] + '_edited.csv'
    try:
        with open(os.path.join('midi', filename), 'w') as f:
            f.write(content)
#        pprint.pprint(content) # debug
        print('\nContent cleaned and saved to file\n\n    midi/{}\n'.
                format(filename))
    except Exception as e:
        print('Content cleaned but failed to save; error "{}"'.format(e))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = 'output.csv'
    else:
        filename = sys.argv[1]
        if filename.split('.')[-1] == 'csv':
            main(filename)
        else:
            print('Input filename must end in .csv')
