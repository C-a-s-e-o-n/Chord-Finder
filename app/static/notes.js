// Export class for use in other files
export class Note {
    constructor(noteName) {
        this.noteName = noteName;
        this.isSelected = false;
    }

    select() {
        this.isSelected = true;
    }

    deselect() {
        this.isSelected = false;
    }

    getDomElement() {
        return document.getElementById(this.noteName);
    }

}

export class Piano {
    constructor() {
        this.notes = [
            new Note('C3'),
            new Note('Db3'),
            new Note('D3'),
            new Note('Eb3'),
            new Note('E3'),
            new Note('F3'),
            new Note('Gb3'),
            new Note('G3'),
            new Note('Ab3'),
            new Note('A3'),
            new Note('Bb3'),
            new Note('B3'),
            new Note('C4'),
            new Note('Db4'),
            new Note('D4'),
            new Note('Eb4'),
            new Note('E4'),
            new Note('F4'),
            new Note('Gb4'),
            new Note('G4'),
            new Note('Ab4'),
            new Note('A4'),
            new Note('Bb4'),
            new Note('B4')
        ]
    }

    findNoteByName(noteName) {
        return this.notes.find(Note => Note.noteName === noteName);
    }
}