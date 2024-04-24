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


def convert_file_to_raw_bytes(path: GPaths, dest_path):
    with open(path.value, mode="rb") as f:
        unit = [str(line) for line in f.readlines()]
        with open(dest_path, "w") as wf:
            wf.writelines(unit)
