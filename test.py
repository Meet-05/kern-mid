import music21 as m21
import os
# from melodygenerator import MelodyGenerator
# from test import Preprocess


class Preprocess:

    def load_songs_in_kern(dataset_path):
        """Loads all kern pieces in dataset using music21.
        :param dataset_path (str): Path to dataset
        :return songs (list of m21 streams): List containing all pieces
        """
        songs = []
        print(dataset_path)
        # go through all the files in dataset and load them with music21
        for path, subdirs, files in os.walk(dataset_path):
            for file in files:
                print(file)
                # consider only kern files
                if file[-3:] == "krn":
                    print(os.path.join(path, file))
                    song = m21.converter.parse(os.path.join(path, file))
                    songs.append(song)
        return songs

    def encode_song(self, song, time_step=0.25):
        """Converts a score into a time-series-like music representation. Each item in the encoded list represents 'min_duration'
        quarter lengths. The symbols used at each step are: integers for MIDI notes, 'r' for representing a rest, and '_'
        for representing notes/rests that are carried over into a new time step. Here's a sample encoding:
            ["r", "_", "60", "_", "_", "_", "72" "_"]
        :param song (m21 stream): Piece to encode
        :param time_step (float): Duration of each time step in quarter length
        :return:
        """

        encoded_song = []

        for event in song.flat.notesAndRests:

            # handle notes
            if isinstance(event, m21.note.Note):
                symbol = event.pitch.midi  # 60
            # handle rests
            elif isinstance(event, m21.note.Rest):
                symbol = "r"

            # convert the note/rest into time series notation
            steps = int(event.duration.quarterLength / time_step)
            for step in range(steps):

                # if it's the first time we see a note/rest, let's encode it. Otherwise, it means we're carrying the same
                # symbol in a new time step
                if step == 0:
                    encoded_song.append(symbol)
                else:
                    encoded_song.append("_")

        # cast encoded song to str
        encoded_song = " ".join(map(str, encoded_song))

        return encoded_song

    def transpose(self, song):
        """Transposes song to C maj/A min
        :param piece (m21 stream): Piece to transpose
        :return transposed_song (m21 stream):
        """

        # get key from the song
        parts = song.getElementsByClass(m21.stream.Part)
        measures_part0 = parts[0].getElementsByClass(m21.stream.Measure)
        key = measures_part0[0][4]

        # estimate key using music21
        if not isinstance(key, m21.key.Key):
            key = song.analyze("key")

        # get interval for transposition. E.g., Bmaj -> Cmaj
        if key.mode == "major":
            interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("C"))
        elif key.mode == "minor":
            interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("A"))

        # transpose song by calculated interval
        tranposed_song = song.transpose(interval)
        return tranposed_song

    def preprocessor(self, filename):
        # load folk songs
        print("Loading songs...")
        # song = load_songs_in_kern('deutschl/erk')
        song = [m21.converter.parse(filename)]
        print(len(song))
        # transpose songs to Cmaj/Amin
        song = self.transpose(song[0])
        # encode songs with music time series representation
        encoded_song = self.encode_song(song)
        print(f'encoded song -->{encoded_song}')
        return encoded_song

        # mg = MelodyGenerator()
        # melody = mg.generate_melody(encoded_song, 500, 64, 0.3)
        # print(melody)
        # mg.save_melody(melody)
        # save songs to text file
        # save_path = os.path.join(SAVE_DIR, str(i))
        # with open(save_path, "w") as fp:
        #     fp.write(encoded_song)

    def getString(self, filename):
        # deut0569.krn
        x = self.preprocessor(filename)
        print(x)
        return x


# if __name__ == '__main__':
#     Preprocess().getString('deut0569.krn')
