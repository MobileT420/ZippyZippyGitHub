from pathlib import Path

current_file = None


def start_file(path):

    global current_file

    Path(path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    current_file = open(
        path,
        "wb"
    )


def write_chunk(data):

    global current_file

    if current_file:
        current_file.write(data)


def finish_file():

    global current_file

    if current_file:

        current_file.close()

        current_file = None

        print("Saved")