import { Piano } from './notes.js';

const piano = new Piano(); // Array of Note objects
let selectedNotes = []; // Array of currently selected notes

piano.notes.forEach((note) => {
    const domNote = note.getDomElement(); // Returns text content of each note
    domNote.addEventListener('click', receiveNote);
});

document.getElementById('find-chord-btn').addEventListener('click', fetchChord)
document.getElementById('play-chord-btn').addEventListener('click', playChord)

function receiveNote(e) {
    const nameOfClickedNote = e.target.textContent;
    const clickedNote = piano.findNoteByName(nameOfClickedNote);

    if (clickedNote.isSelected === false) {
        colorSelectedNote(clickedNote);
        clickedNote.select();
        selectedNotes.push(clickedNote);
        playNote(clickedNote);
    }

    else if (clickedNote.isSelected === true) {
        colorSelectedNote(clickedNote);
        clickedNote.deselect();
        
        const index = selectedNotes.indexOf(clickedNote);
        selectedNotes.splice(index, 1);
    }

    console.log(selectedNotes);
} 

function colorSelectedNote(clickedNote) {
    const domNote = clickedNote.getDomElement();

    if (clickedNote.isSelected === false) {
        if (domNote.classList.contains('white-key')) {
            document.getElementById(`${domNote.textContent}-span`).style.backgroundColor = 'black';
            document.getElementById(`${domNote.textContent}-span`).style.color = 'white';
        }
        else {
            document.getElementById(`${domNote.textContent}-span`).style.backgroundColor = 'white';
            document.getElementById(`${domNote.textContent}-span`).style.color = 'black';
        }
    }

    if (clickedNote.isSelected === true) {
        if (domNote.classList.contains('white-key')) {
            document.getElementById(`${domNote.textContent}-span`).style.backgroundColor = 'white';
            document.getElementById(`${domNote.textContent}-span`).style.color = 'black';
        }
        else {
            document.getElementById(`${domNote.textContent}-span`).style.backgroundColor = 'black';
            document.getElementById(`${domNote.textContent}-span`).style.color = 'white';
        }
    }
} 

function playNote(clickedNote) {
    const audioFilePath = `static/notes/${clickedNote.noteName}.wav`;
    const audio = new Audio(audioFilePath);
    audio.play();
}


let audioContext;
function playChord() {
    fetch('/play_chord', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
        },
        body: JSON.stringify({ notes: selectedNotes.map(note => note.noteName) }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('No notes are selected');
        }
        return response.arrayBuffer();
    })
    .then(audioData => {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }

        audioContext.decodeAudioData(audioData, buffer => {
            const source = audioContext.createBufferSource();
            source.buffer = buffer;
            source.connect(audioContext.destination);
            source.start();
        });
    });
}

function fetchChord() {
    fetch('/get_note', {
        method: 'POST', 
        headers: {
            'Content-type': 'application/json',
        },
        body: JSON.stringify( {notes: selectedNotes.map(note => note.noteName)} ),
    })
        .then(response => response.json()) // Metadata about the response object
        .then(responseData => {
            // responseData is the python variable containing the JSON audio data
            const matchedChord = responseData.matchedChord;
            const otherMatchedChords = responseData.otherMatchedChords;
            const chordDiv = document.getElementById('chord-text');
            const otherChordsDiv = document.getElementById('other-chords-text')
            chordDiv.textContent = matchedChord;
            chordDiv.style.fontWeight = 'bold';
            chordDiv.style.color = 'white';
            otherChordsDiv.textContent = 'Notes also found in: ' + otherMatchedChords;
            otherChordsDiv.style.color = 'white';  // displays every matched chord

    })
    .catch(error => console.error('Error fetching data:', error));
}
