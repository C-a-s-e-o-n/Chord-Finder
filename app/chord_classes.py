import pandas as pd

# SCALES
class Scale:
    def __init__(self, name, tonic, supertonic, mediant, subdom, dom, submediant, leading):
        self.name = name
        self.tonic = tonic
        self.supertonic = supertonic
        self.mediant = mediant
        self.subdom = subdom
        self.dom = dom
        self.submediant = submediant
        self.leading = leading

    chromatic = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    list_6th_7th_chords = []
    list_triads = []
    list_extended_chords = []

    @staticmethod
    def flatten_note(note, chromatic):
        if note in chromatic:
            index = chromatic.index(note)
            flat_note_index = (index - 1) % len(chromatic) # wrap around in case of C
            return chromatic[flat_note_index]
        

    @staticmethod
    def get_triads(maj_scale, chromatic, list_triads):
        flat_mediant = Scale.flatten_note(maj_scale.mediant, chromatic) # minor third
        flat_dom = Scale.flatten_note(maj_scale.dom, chromatic) # b5
        flat_submediant = Scale.flatten_note(maj_scale.submediant, chromatic) # augmented fifth

        maj_triad = [f'{maj_scale.tonic}_maj_triad', maj_scale.tonic, maj_scale.mediant, maj_scale.dom]
        min_triad = [f'{maj_scale.tonic}_min_triad', maj_scale.tonic, flat_mediant, maj_scale.dom]
        aug_triad = [f'{maj_scale.tonic}_aug_triad', maj_scale.tonic, maj_scale.mediant, flat_submediant]
        dim_triad = [f'{maj_scale.tonic}_dim_triad', maj_scale.tonic, flat_mediant, flat_dom]
        sus2 = [f'{maj_scale.tonic}_sus2_triad', maj_scale.tonic, maj_scale.supertonic, maj_scale.dom]
        sus4 = [f'{maj_scale.tonic}_sus4_triad', maj_scale.tonic, maj_scale.subdom, maj_scale.dom]

        list_triads.append(maj_triad)
        list_triads.append(min_triad)
        list_triads.append(aug_triad)
        list_triads.append(dim_triad)
        list_triads.append(sus2)
        list_triads.append(sus4)

        return list_triads

    @staticmethod
    def get_6th_7th_chords(maj_scale, chromatic, list_6th_7th_chords):
        flat_mediant = Scale.flatten_note(maj_scale.mediant, chromatic) # minor third
        flat_dom = Scale.flatten_note(maj_scale.dom, chromatic) # b5
        flat_submediant = Scale.flatten_note(maj_scale.submediant, chromatic) # augmented fifth
        flat_leading = Scale.flatten_note(maj_scale.leading, chromatic) # 7th note from minor scale

        # 6th chords
        maj_6 = [f'{maj_scale.tonic}_maj_6', maj_scale.tonic, maj_scale.mediant, maj_scale.dom, maj_scale.submediant] 
        min_6 = [f'{maj_scale.tonic}_min_6', maj_scale.tonic, flat_mediant, maj_scale.dom, maj_scale.submediant]
        list_6th_7th_chords.append(maj_6)
        list_6th_7th_chords.append(min_6)

        # clean up later
        maj_7 = [f'{maj_scale.tonic}_maj_7', maj_scale.tonic, maj_scale.mediant, maj_scale.dom, maj_scale.leading]
        list_6th_7th_chords.append(maj_7)

        min_7 = [f'{maj_scale.tonic}_min_7', maj_scale.tonic, flat_mediant, maj_scale.dom, flat_leading]
        list_6th_7th_chords.append(min_7)

        min_maj_7 = [f'{maj_scale.tonic}_min_maj_7', maj_scale.tonic, flat_mediant, maj_scale.dom, maj_scale.leading]
        list_6th_7th_chords.append(min_maj_7)

        dom_7 = [f'{maj_scale.tonic}_dom_7', maj_scale.tonic, maj_scale.mediant, maj_scale.dom, flat_leading]
        list_6th_7th_chords.append(dom_7)

        aug_7 = [f'{maj_scale.tonic}_aug_7', maj_scale.tonic, maj_scale.mediant, flat_submediant, flat_leading]
        list_6th_7th_chords.append(aug_7)

        maj_7_sharp5 = [f'{maj_scale.tonic}_maj_7_sharp5', maj_scale.tonic, maj_scale.mediant, flat_submediant, maj_scale.leading] # weird name because # = comment
        list_6th_7th_chords.append(maj_7_sharp5)

        min_7_b5 = [f'{maj_scale.tonic}_min_7_b5', maj_scale.tonic, flat_mediant, flat_dom, flat_leading]
        list_6th_7th_chords.append(min_7_b5)

        dim_7 = [f'{maj_scale.tonic}_dim_7', maj_scale.tonic, flat_mediant, flat_dom, maj_scale.submediant]
        list_6th_7th_chords.append(dim_7)

        dom_7_sus4 = [f'{maj_scale.tonic}_dom_7_sus4', maj_scale.tonic, maj_scale.subdom, maj_scale.dom, flat_leading]
        list_6th_7th_chords.append(dom_7_sus4)

        dom_7_sus2 = [f'{maj_scale.tonic}_dom_7_sus2', maj_scale.tonic, maj_scale.supertonic, maj_scale.dom, flat_leading]
        list_6th_7th_chords.append(dom_7_sus2)

        return list_6th_7th_chords

    @staticmethod
    def get_extended_chords(maj_scale, chromatic, list_extended_chords):

        flat_mediant = Scale.flatten_note(maj_scale.mediant, chromatic) # minor third
        flat_dom = Scale.flatten_note(maj_scale.dom, chromatic) # b5
        flat_leading = Scale.flatten_note(maj_scale.leading, chromatic) # 7th note from minor scale


        ninth = maj_scale.supertonic # ninth degree of scale
        eleventh = maj_scale.subdom # 11th degree of scale
        thirteenth = maj_scale.submediant # 13th degree of scale

        # 9 chords
        maj_9 = [f'{maj_scale.tonic}_maj_9', maj_scale.tonic, maj_scale.mediant, maj_scale.dom, maj_scale.leading, ninth, None, None]
        min_9 = [f'{maj_scale.tonic}_min_9', maj_scale.tonic, flat_mediant, maj_scale.dom, flat_leading, ninth, None, None]
        min_maj_9 = [f'{maj_scale.tonic}_min_maj_9', maj_scale.tonic, flat_mediant, maj_scale.dom, maj_scale.leading, ninth, None, None]
        dom_9 = [f'{maj_scale.tonic}_dom_9', maj_scale.tonic, maj_scale.mediant, maj_scale.dom, flat_leading, ninth, None, None]

        list_extended_chords.append(maj_9)
        list_extended_chords.append(min_9)
        list_extended_chords.append(min_maj_9)
        list_extended_chords.append(dom_9)

        # 11 chords
        maj_11 = [f'{maj_scale.tonic}_maj_11', maj_scale.tonic, maj_scale.mediant, maj_scale.dom, maj_scale.leading, ninth, eleventh, None]
        min_11 = [f'{maj_scale.tonic}_min_11', maj_scale.tonic, flat_mediant, maj_scale.dom, flat_leading, ninth, eleventh, None]
        min_maj_11 = [f'{maj_scale.tonic}_min_maj_11', maj_scale.tonic, flat_mediant, maj_scale.dom, maj_scale.leading, ninth, eleventh, None]
        dom_11 = [f'{maj_scale.tonic}_dom_11', maj_scale.tonic, maj_scale.mediant, maj_scale.dom, flat_leading, ninth, eleventh, None]

        list_extended_chords.append(maj_11)
        list_extended_chords.append(min_11)
        list_extended_chords.append(min_maj_11)
        list_extended_chords.append(dom_11)

        # 13 chords
        maj_13 = [f'{maj_scale.tonic}_maj_13', maj_scale.tonic, maj_scale.mediant, maj_scale.dom, maj_scale.leading, ninth, eleventh, thirteenth]
        min_13 = [f'{maj_scale.tonic}_min_13', maj_scale.tonic, flat_mediant, maj_scale.dom, flat_leading, ninth, eleventh, thirteenth]
        min_maj_13 = [f'{maj_scale.tonic}_min_maj_13', maj_scale.tonic, flat_mediant, maj_scale.dom, maj_scale.leading, ninth, eleventh, thirteenth]
        dom_13 = [f'{maj_scale.tonic}_dom_13', maj_scale.tonic, maj_scale.mediant, maj_scale.dom, flat_leading, ninth, eleventh, thirteenth]

        list_extended_chords.append(maj_13)
        list_extended_chords.append(min_13)
        list_extended_chords.append(min_maj_13)
        list_extended_chords.append(dom_13)
        return list_extended_chords



def get_chords_for_scale():
    scales = [
    Scale('C Major', 'C', 'D', 'E', 'F', 'G', 'A', 'B'),
    Scale('Db Major', 'Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'),
    Scale('D Major', 'D', 'E', 'Gb', 'G', 'A', 'B', 'Db'),
    Scale('Eb Major', 'Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'),
    Scale('E Major', 'E', 'Gb', 'Ab', 'A', 'B', 'Db', 'Eb'),
    Scale('F Major', 'F', 'G', 'A', 'Bb', 'C', 'D', 'E'),
    Scale('Gb Major', 'G', 'A', 'B', 'C', 'D', 'E', 'Gb'),
    Scale('G Major', 'Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F'),
    Scale('Ab Major', 'Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'),
    Scale('A Major', 'A', 'B', 'Db', 'D', 'E', 'Gb', 'Ab'),
    Scale('Bb Major', 'Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'),
    Scale('B Major', 'B', 'Db', 'Eb', 'E', 'Gb', 'Ab', 'Bb')
    ]

    for scale in scales:
        list_6th_7th_chords = Scale.get_6th_7th_chords(scale, Scale.chromatic, Scale.list_6th_7th_chords)
        list_triads = Scale.get_triads(scale, Scale.chromatic, Scale.list_triads)
        list_extended_chords = Scale.get_extended_chords(scale, Scale.chromatic, Scale.list_extended_chords)

    return list_triads, list_6th_7th_chords, list_extended_chords

    # df1 = pd.DataFrame({'Triads': list_triads})
    # df2 = pd.DataFrame({'6ths and 7ths': list_6th_7th_chords})
    # df3 = pd.DataFrame({'Extended': list_extended_chords})
    
    # print(df1)
    # print(df2)
    # print(df3)
