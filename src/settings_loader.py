

def load_settings(filename: str) -> dict:
    with open(filename, 'rt', encoding='utf8') as f:
        text = f.read()
    lines = text.splitlines(keepends=False)

    settings = {}
    for line in lines:
        if line.strip() == '':
            continue
        if line.startswith('#'):
            continue

        pair = line.split('=', 1)
        settings[pair[0].strip()] = pair[1].strip()
    return settings

if __name__ == '__main__':
    print(load_settings('settings.txt'))
