from Code.Keys.GamePaths import GPaths


def get_chunks(chunks, rows_size):
    if chunks < 1 or chunks > rows_size:
        return
    chunk_size = int(rows_size / chunks)
    ranges = []
    start = 0
    end = chunk_size
    for i in range(chunks):
        ranges.append((start, end))
        start = end
        end += chunk_size
        if i == (chunks - 2):
            end = rows_size
    return ranges


def convert_file_to_raw_bytes_g_path(g_path: GPaths, dest_path):
    convert_file_to_raw_bytes(g_path.value, dest_path)


def convert_file_to_raw_bytes(path: str, dest_path):
    with open(path, mode="rb") as f:
        unit = [str(line) for line in f.readlines()]
        with open(dest_path, "w") as wf:
            wf.writelines(unit)


def get_file_as_lines(path: str):
    with open(path, mode="rb") as f:
        unit = [str(line) for line in f.readlines()]
    return unit


def get_file_as_lines2(path: str):
    with open(path, mode="rb") as f:
        unit = f.read().split(b"\n")
    return unit


def get_file(path: str):
    with open(path, mode='rb') as f:
        return f.read()
