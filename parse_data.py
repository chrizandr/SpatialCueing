from lxml import etree
import matplotlib.pyplot as plt
import os
import numpy as np
import pdb
from sklearn.cluster import KMeans


def parse_file(filepath, gender):
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
            try:
                raw_data[columns[i]].append(float(value))
            except ValueError:
                raw_data[columns[i]].append(value)

    max_val = max(raw_data[columns[2]])
    min_val = min(raw_data[columns[2]])
    raw_data[columns[2]] = [100*(x-min_val)/(max_val - min_val) for x in raw_data[columns[2]]]

    trial, time = raw_data[columns[1]], raw_data[columns[2]]
    data = {}
    for l, t in zip(trial, time):
        if l not in data:
            data[l] = [float(t)]
        else:
            data[l].append(float(t))
    raw_data["Gender"] = gender[filepath]
    return data, raw_data


def gender_file(filepath, data_path):
    gender = {}
    f = open(filepath)
    for r in f:
        data = r.strip().split(',')
        gender[os.path.join(data_path, data[0])] = data[1]
    return gender


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
    gender = gender_file("gender.txt", data_path)
    files = get_files(data_path)
    output = [parse_file(x, gender) for x in files]
    data = [x[0] for x in output]
    raw_data = [x[1] for x in output]

    means = [find_means(x) for x in data]

    means_m = []
    means_f = []

    order = ['Invalid Left', 'Invalid Right', 'Neutral Left', 'Neutral Right', 'Valid Left', 'Valid Right']
    for i, x in enumerate(raw_data):
        if x["Gender"] == "M":
            means_m.append([means[i][x] for x in order])
        else:
            means_f.append([means[i][x] for x in order])

    means_f = np.array(means_f)
    means_m = np.array(means_m)

    means_m_mean = np.mean(means_m, axis=0)
    means_f_mean = np.mean(means_f, axis=0)

    means = np.vstack((means_f, means_m))

    model = KMeans(n_clusters=2)
    model.fit(means)

    labels = model.labels_

    data_1 = [means[i] for i, x in enumerate(labels) if x > 0]
    data_2 = [means[i] for i, x in enumerate(labels) if x == 0]

    cluster_1 = [raw_data[i] for i, x in enumerate(labels) if x > 0]
    cluster_2 = [raw_data[i] for i, x in enumerate(labels) if x == 0]

    pdb.set_trace()
    cov = np.cov(means.T)
    plt.imshow(cov)
    plt.title("Correlation between features")
    plt.xticks(range(len(order)), order)
    plt.yticks(range(len(order)), order)
    plt.show()
    pdb.set_trace()
    # total_mean = {}
    # for key in means[0].keys():
    #     mean_data = [x[key] for x in means]
    #     mean = sum(mean_data) / len(mean_data)
    #     total_mean[key] = mean
    # pdb.set_trace()
