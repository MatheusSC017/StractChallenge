import io
import csv


def convert_csv(data):
    output = io.StringIO()
    writer = csv.writer(output)

    for row in data:
        writer.writerow(row)

    output.seek(0)
    return output.getvalue()
