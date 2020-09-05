import re

ligatures = {
    # chr(0x10): 'ff',
    # chr(0x06): 'fi',
    # chr(0x02): 'fi',
    # chr(0x05): 'ff',
    # chr(0x03): 'ff',
    # chr(0x19): 'fl',
    # chr(0x0c): 'fi',
    # chr(0x0b): 'ff',
    # chr(0x1a):' ',
    #   unichr(0xA732):'AA',
    #   unichr(0xA733):'aa',
    #   unichr(0x00C6):'AE',
    #   unichr(0x00E6):'ae',
    #   unichr(0xA734):'AO',
    #   unichr(0xA735):'ao',
    #   unichr(0xA736):'AU',
    #   unichr(0xA737):'au',
    #   unichr(0xA738):'AV',
    #   unichr(0xA739):'av',
    #   unichr(0xA73A):'AV',
    #   unichr(0xA73B):'av',
    #   unichr(0xA73C):'AY',
    #   unichr(0xA73D):'ay',
    #   unichr(0x1F670):'et',
    #   unichr(0xFB00):'ff',
    #   unichr(0xFB03):'ffi',
    #   unichr(0xFB04):'ffl',
    #   unichr(0xFB01):'fi',
    #   unichr(0xFB02):'fl',
    #   unichr(0x0152):'OE',
    #   unichr(0x0153):'OE',
    #   unichr(0xA74E):'OO',
    #   unichr(0xA74F):'oo',
    #   unichr(0x1E9E):'fs',
    #   unichr(0x00DF):'fz',
    #   unichr(0xFB06):'st',
    #   unichr(0xFB05):'ft',
    #   unichr(0xA728):'TZ',
    #   unichr(0xA729):'tz',
    #   unichr(0x1D6B):'ue',
    #   unichr(0xA760):'VY',
    #   unichr(0xA761):'vy'
}


def clean_text(rawtxt):
    '''

    '''
    f = open(rawtxt, 'r')
    content = f.readlines()
    f.close()

    # if line starts with lowercase letter, join in with previous line

    pattern_trash_string = r"^[+-,:;)%(/|. 0-9]+$"
    len_content = len(content)
    for i in range(1, len_content + 1):
        j = len_content - i

        # remove trash strings
        if re.match(pattern_trash_string, content[j]):
            content[j] = ""
            continue

        if content[j][0].islower():
            c = content[j - 1].strip()
            if len(c) > 0 and c[-1] == '-':
                # print(c)
                content[j - 1] = c[:-1].strip() + content[j]
                content[j] = ""
            # elif len(c)>0 and c[-1]=='-':
            #    content[j-1]=c[:-1].strip()+content[j]
            #    content[j]=""
            else:
                content[j - 1] = c + " " + content[j]
                content[j] = ""
        else:
            c = content[j - 1].strip()
            if len(c) > 0 and c[-1] == ',':
                content[j - 1] = c + " " + content[j]
                content[j] = ""
    for j in range(0, len_content):
        content[j] = content[j].strip()
    content_filtered = [s for s in content if len(s) > 0]

    content_filtered = replace_ligatures(content_filtered)

    content = "\n".join(content_filtered)

    content = re.sub(r'\s*-\s*\n', '', content)
    content = re.sub(r'\n[ ,0-9]+\]', ' ', content)
    content = re.sub(r'\s*,\s*\n', ', ', content)
    content = re.sub(r'\n([a-z]+)', r'\1', content)
    content = re.sub(r'\n\s*\(', r'(', content)
    content = re.sub(r'\s+\.', r'.', content)
    content = re.sub(r'\n\d+\]', ' ', content)
    content = re.sub(r'\[[0-9, ]+\]', ' ', content)
    content = re.sub(r'\s+\.', r'.', content)
    content = re.sub(r'\s+,', r',', content)
    content = re.sub(r'( and| or| if| of| to | over| a| the| in| between| when| where| is| The)\s*\n', r'\1 ', content)
    content = re.sub(r' +', r' ', content)
    # content=re.sub(r'\s*,\s*\n',', ',
    #    re.sub(r'\s*-\s*\n', '',
    #        "\n".join(content_filtered)))

    return content


def replace_ligatures(content_filtered):
    # replace ligatures here
    len_content = len(content_filtered)
    for c in ligatures:
        f = c
        t = ligatures[c]
        for j in range(0, len_content):
            content_filtered[j] = content_filtered[j].replace(f, t)

    return content_filtered
