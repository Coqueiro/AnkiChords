import pandas as pd
import re

def convert_music(title):
    raw_df = pd.read_csv('music/' + title + '.txt', sep='\n',
                         names=['line'], comment='#')

    music_df = pd.DataFrame(
        data=None, columns=['title',
                            'last_comment', 'last_chord', 'last_lyric',
                            'comment', 'chord', 'lyric'])

    comment = chord = lyric = None
    has_chord = has_lyric = True
    music_line = {'comment': '[First Line]', 'chord': None, 'lyric': None}

    for row in raw_df.iterrows():
        if has_chord:
            if row[1][0][0] == '-':
                comment = row[1][0]
            elif row[1][0][0] == '>':
                comment = row[1][0]
                has_lyric = False
            else:
                chord = add_image(row[1][0])
                has_chord = False
        elif has_lyric:
            lyric = row[1][0]
            has_lyric = False
        if not has_lyric and not has_chord:
            music_df = music_df.append(
                {'title': title,
                 'last_comment': music_line['comment'],
                 'last_chord': music_line['chord'],
                 'last_lyric': music_line['lyric'],
                 'comment': comment, 'chord': chord, 'lyric': lyric}, ignore_index=True)
            music_line = {'comment': comment, 'chord': chord, 'lyric': lyric}
            comment = chord = lyric = None
            has_chord = has_lyric = True

    music_df.index.name = 'order'
    music_df.to_csv('music_tsv/' + title + '.tsv', 
                    header=False, sep='\t', encoding='utf-8')

def generate_spans(chord):
    chord_span = '<span_class=chord>{}</span>'.format(chord)
    image_span = '<span_class=image><img_src={}.png></span>'.format(chord)
    return chord_span + image_span

def add_image(chord_text):
    spans = re.sub(r'\w+', lambda x: generate_spans(x.group()), chord_text)
    spans = spans.replace(' ', '&nbsp;')
    spans = spans.replace('_', ' ')
    return spans
    