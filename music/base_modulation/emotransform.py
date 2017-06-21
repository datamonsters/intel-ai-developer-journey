'''
Emotion-based melody transformation script
Alexey Kalinin, 2017

Requirements: python3, music21

Using:
- call from console:
       python3 emotransform.py --emotion JOY input.mid
       output: transformed file JOY_input.mid

- from other python script
       from emotransform import transform
       transform('input.mid','JOY')
       output: transformed file JOY_input.mid
'''

import sys
import argparse
import music21

EMOTIONS = (
    'ANXIETY',
    'AWE',
    #'GRATITUDE',
    'JOY',
    'SADNESS',
    #'SERENITY',
    'DETERMINATION'
    )

def transform(filename, targetEmotion):
    ''' Perform emotion-based transformation. Output - transformed midi-file '''
    src_score = music21.converter.parse(filename)
    src_key = src_score.analyze('key')

    print("Source scale is", src_key.tonic.name, src_key.mode)
    print('Transforming {0} to {1}'.format(filename, targetEmotion))
    assert len(src_score) == 1, 'Not enough parts in score'

    part = src_score[0]

    currentScale = None
    if src_key.mode == 'major':
        currentScale = music21.scale.MajorScale(src_key.tonic.name)
    else:
        currentScale = music21.scale.MinorScale(src_key.tonic.name)

    # ANXIETY
    if targetEmotion == 'ANXIETY':
        notes = part.getElementsByClass(music21.note.Note)
        for currNote in notes:
            currDegree = currentScale.getScaleDegreeFromPitch(currNote)
            #print(currNote, ' * ', currDegree)
            minorsDegrees = (3, 6)
            if currDegree in minorsDegrees:  # change to minor (almost) - halftone lower III and VI degree, VII - leave untouched
                currNote.transpose(-1, inPlace=True)
                #TODO: add syncope
                #print('Beats ', currNote.offset, currNote.beat) 
                #currNote.offset = currNote.offset - 0.3 
                #print('Updated ', currNote)

    # SADNESS
    if targetEmotion == 'SADNESS':
        part.scaleOffsets(2.0).scaleDurations(2.0)

        notes = part.getElementsByClass(music21.note.Note)
        for currNote in notes:
            currNote.quarterLength = 4.00
            currDegree = currentScale.getScaleDegreeFromPitch(currNote)
            #print(currNote, ' * ', currDegree)
            minorsDegrees = (3, 6, 7)
            if currDegree in minorsDegrees:  # completely change to minor - halftone lower III, VI and VII degree
                currNote.transpose(-1, inPlace=True)
                #print('Updated ', currNote)

    # AWE
    if targetEmotion == 'AWE':
        part.scaleOffsets(1.8).scaleDurations(1.8)
        notes = part.getElementsByClass(music21.note.Note)
        for currNote in notes:
            currNote.quarterLength = 4.00
            currDegree = currentScale.getScaleDegreeFromPitch(currNote)
            #print(currNote, ' * ', currDegree)

            # Transitions, which should be changed
            # curr   next
            #   1 -> 5
            #   1 -> 4
            #   4 -> 1
            #   5 -> 1
            transition_degrees = {
                1:[4, 5],
                4:[1],
                5:[1]
            }

            if currDegree in transition_degrees:
                #lookup for next note
                nextNote = part.getElementAfterElement(currNote, [music21.note.Note])
                if nextNote == None: break

                nextNoteDegree = currentScale.getScaleDegreeFromPitch(nextNote)
                nextCheckDegrees = transition_degrees[currDegree]

                if nextNoteDegree in nextCheckDegrees:
                    #print('Updated ', nextNote)
                    #note change - connected with prev degree
                    if (currDegree == 1) and (nextNoteDegree in (4, 5)):
                        shiftInterval = music21.interval.Interval(nextNote, music21.note.Note(currentScale.pitchFromDegree(6)))
                        nextNote.transpose(shiftInterval, inPlace=True)

                    if (currDegree in (4, 5)) and (nextNoteDegree == 1):
                        shiftInterval = music21.interval.Interval(currNote, music21.note.Note(currentScale.pitchFromDegree(3)))
                        currNote.transpose(shiftInterval, inPlace=True)

    # JOY
    if targetEmotion == 'JOY':
        # pentatonic, replace 4 и 7 degree
        notes = part.getElementsByClass(music21.note.Note)
        for currNote in notes:
            currDegree = currentScale.getScaleDegreeFromPitch(currNote)
            #print(currNote, ' * ', currDegree)
            notPentaDegrees = (4, 7)
            if currDegree in notPentaDegrees:
                #print('Uppdated ', currNote)
                if currDegree == 4:
                    shiftInterval = music21.interval.Interval(currNote, music21.note.Note(currentScale.pitchFromDegree(5)))
                    currNote.transpose(shiftInterval, inPlace=True)
                if currDegree == 7:
                    shiftInterval = music21.interval.Interval(currNote, music21.note.Note(currentScale.pitchFromDegree(1)))
                    currNote.transpose(shiftInterval, inPlace=True)

    # DETERMINATION
    if targetEmotion == 'DETERMINATION':
        #TODO: translate to major if needed
        #TODO: rhythm: add syncops
        part.scaleOffsets(0.8).scaleDurations(0.8)
        notes = part.getElementsByClass(music21.note.Note)
        for currNote in notes:
            # shorten note duration, except last in each phrase
            if currNote.quarterLength <= 1:
                currNote.quarterLength = 0.25

    # TRANQUILITY/SERENITY
    if targetEmotion == 'SERENITY':
        assert False, 'SERENITY under construction!'

    # GRATITUDE
    if targetEmotion == 'GRATITUDE':
        assert False, 'GRATITUDE is under construction!'

    # transpose key signature
    #for ks in src_score.flat.getKeySignatures():
    #    ks.transpose(halfSteps, inPlace=True)

    newFileName = targetEmotion + '_' + filename
    src_score.write('midi', newFileName)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('''2 parameters needed!\nUsage: emo-transform.py filename --emotion EMOTION  ''')
        quit()

    parser = argparse.ArgumentParser()
    parser.add_argument('--emotion', dest='emotion')
    parser.add_argument('filename', type=str)
    args = parser.parse_args()

    if (args.emotion in EMOTIONS) == False:
        print('Please, specify one of possible emotions: ', EMOTIONS)
        quit()

    transform(filename=args.filename, targetEmotion=args.emotion)

