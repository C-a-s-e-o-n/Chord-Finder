from flask import Flask, send_from_directory, jsonify, request, render_template, Response
from chord_db import find_user_chord, get_conn_c
from export_audio import overlay_block_chord

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename) 


@app.route('/get_note', methods=['POST'])
def get_note():
    print(request.method)
    print(request.json)
    keys_pressed = request.json.get('notes') # Extracting the keys pressed into a list


    # Iterate through the list and remove numbers from each note
    for i in range(len(keys_pressed)):
        keys_pressed[i] = ''.join(char for char in keys_pressed[i] if not char.isdigit())
    print(keys_pressed)

    conn, c = get_conn_c()
    
    matched_chord, other_matched_chords = find_user_chord(keys_pressed, conn, c) # returns a single chord, and a list of chords

    response_data = {
        "matchedChord": matched_chord,
        "otherMatchedChords": other_matched_chords
    }

    print(response_data)
        # print(jsonify({'audioFilePath':audio_file_path}))

    return jsonify(response_data)


@app.route('/play_chord', methods=['POST', 'GET'])
def play_chord():
    print(request.method)
    print(request.json)
    keys_pressed = request.json.get('notes')

    note_paths = []

    for key in keys_pressed:
        note_paths.append(f'app/static/notes/{key}.wav')

    chord_audio = overlay_block_chord(note_paths)

    # Export the combined audio as bytes
    audio_bytes = chord_audio.export(format="wav").read()

    # Set appropriate headers for the response
    response = Response(audio_bytes, mimetype="audio/wav")
    response.headers['Content-Disposition'] = 'inline; filename=combined_audio.wav'

    return response

if __name__ == "__main__":
    app.run(debug=True)
