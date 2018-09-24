from lxml import etree
import matplotlib.pyplot as plt
import os
import pdb


def parse_file(filepath):
    """Parse the HTML file to get data."""
    html = open(filepath).read().replace("\n", "")
    data_table = etree.HTML(html).findall("body/table")[1]

    rows = data_table.getchildren()

    raw_data = {}
    columns = []

    for headers in rows[0].getchildren():
        label = headers.getchildren()[0].text
        raw_data[label] = list()
        columns.append(label)

    for r in rows[1::]:
        for i, entry in enumerate(r.getchildren()):
            value = entry.getchildren()[0].text
            raw_data[columns[i]].append(value)

    trial, time = raw_data[columns[1]], raw_data[columns[2]]
    data = {}
    for l, t in zip(trial, time):
        if l not in data:
            data[l] = [float(t)]
        else:
            data[l].append(float(t))

    return data, raw_data


def get_files(data_path):
    """Get all the file in the data path."""
    file_list = os.listdir(data_path)
    file_list = [x for x in file_list if x[-5:] == ".html"]
    file_list = [os.path.join(data_path, x) for x in file_list]
    return file_list


def find_means(data):
    means = {}
    for key in data.keys():
        means[key] = sum(data[key]) / len(data[key])
    return means


if __name__ == "__main__":
    data_path = "data/"
    files = get_files(data_path)
    output = [parse_file(x) for x in files]
    data = [x[0] for x in output]
    raw_data = [x[1] for x in output]
    means = [find_means(x) for x in data]

    for key in means[0].keys():
        mean_data = [x[key] for x in means]
        plt.plot(mean_data, label=key)
    plt.legend()
    plt.show()
    pdb.set_trace()
