import pandas as pd

title = 'Barfuß am Klavier'
raw_df = pd.read_csv(title + '.txt', sep='\n',
                     names=['line'], comment='#')

music_df = pd.DataFrame(
    data=None, columns=['comment', 'chord', 'lyric',
                        'last_comment', 'last_chord', 'last_lyric'])

comment = chord = lyric = None
has_chord = has_lyric = True
music_line = {'comment': None, 'chord': None, 'lyric': None}

for row in raw_df.iterrows():
    if has_chord:
        if row[1][0][0] == '-':
            comment = row[1][0]
        elif row[1][0][0] == '>':
            comment = row[1][0]
            has_lyric = False
        else:
            chord = row[1][0]
            has_chord = False
    elif has_lyric:
        lyric = row[1][0]
        has_lyric = False
    if not has_lyric and not has_chord:
        music_df = music_df.append(
            {'comment': comment, 'chord': chord, 'lyric': lyric,
             'last_comment': music_line['comment'], 'last_chord': music_line['chord'],
             'last_lyric': music_line['lyric']}, ignore_index=True)
        music_line = {'comment': comment, 'chord': chord, 'lyric': lyric}
        comment = chord = lyric = None
        has_chord = has_lyric = True

music_df.index.name = 'order'
music_df.to_csv(title + '.tsv', sep='\t')
