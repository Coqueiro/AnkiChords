import pandas as pd

title = 'Barfuß am Klavier'
raw_df = pd.read_csv(title + '.txt', sep='\n',
                 names=['line'], comment='#')

music_df = pd.DataFrame(
    data=None, columns=['comment', 'chord', 'lyric'])

comment = chord = lyric = None
next_chord = next_lyric = True

for row in raw_df.iterrows():
    if next_chord:
        if row[1][0][0] == '-':
            comment = row[1][0]
        elif row[1][0][0] == '>':
            comment = row[1][0]
            next_lyric = False
        else:
            chord = row[1][0]
            next_chord = False
    elif next_lyric:
        lyric = row[1][0]
        next_lyric = False
    if not next_lyric and not next_chord:
        music_df = music_df.append(
            {'comment': comment, 'chord': chord, 'lyric': lyric}, ignore_index=True)
        comment = chord = lyric = None
        next_chord = next_lyric = True

music_df.index.name = 'order'
music_df.to_csv(title + '.tsv', sep='\t')