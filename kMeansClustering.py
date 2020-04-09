import numpy as np
import random
import csv
from sklearn import preprocessing


def compute_euclidean_distance(point, centroid):
    return np.sqrt(np.sum((point - centroid) ** 2))


def assign_label_cluster(distance, data_point, centroids):
    index_of_minimum = min(distance, key=distance.get)
    return [index_of_minimum, data_point, centroids[index_of_minimum]]


def compute_new_centroids(cluster_label, centroids):
    return np.array(cluster_label + centroids)


def iterate_k_means(data_points, centroids, total_iteration):
    cluster_label = []
    total_points = len(data_points)
    k = len(centroids)

    for iteration in range(0, total_iteration):
        for index_point in range(0, total_points):
            distance = {}
            for index_centroid in range(0, k):
                distance[index_centroid] = compute_euclidean_distance(data_points[index_point],
                                                                      centroids[index_centroid])
            label = assign_label_cluster(distance, data_points[index_point], centroids)
            centroids[label[0]] = compute_new_centroids(label[1], centroids[label[0]])

            if iteration == (total_iteration - 1):
                cluster_label.append(label)

    return [cluster_label, centroids]


def create_centroids(length):

    centroids = []
    x = []
    y = []

    for i in range(0, length):
        x.append(random.uniform(1, 9))
        y.append(random.uniform(1, 9))

    centroids.append(x)
    centroids.append(y)

    return np.array(centroids)


def recursively(data_points, centroids, total_iteration, anomaly, counter, temp):
    cluster0 = []
    cluster1 = []
    temp2 = []
    limit = 5
    numberOfCluster = 16
    [cluster_label, new_centroids] = iterate_k_means(data_points, centroids, total_iteration)

    for data in [cluster_label, new_centroids][0]:
        if data[0] == 0:
            cluster0.append(data[1])
        else:
            cluster1.append(data[1])
    print(len(cluster0), len(cluster1))
    if len(cluster0) <= limit * 2:
        if len(cluster0) <= limit * 2:
            print("Anomaly Detected !!!")
            anomaly.append(cluster0)
            temp = 1
        else:
            temp = 0
            if counter < numberOfCluster:
                counter = counter + 1
                succesGroups.append(cluster0)
            print("cluster - counter ", len(cluster0), " - ", counter)
            print(limit, " FINISHED")
    else:
        temp = 0
        print("Left Node Starting...", len(cluster0))
        if counter == numberOfCluster:
            return anomaly, temp, counter

        if counter == numberOfCluster - 1:
            return anomaly, temp, counter

        if counter <= numberOfCluster - 2:
            temp2, temp, counter = recursively(cluster0, [cluster_label, new_centroids][1], total_iteration, anomaly,
                                               counter, temp)

        if temp == 1:
            counter = counter + 1
            succesGroups.append(cluster1)
            temp = 0
            print("cluster - counter ", len(cluster0), " - ", counter)
        print("Left Node Finished...")
    if len(cluster1) <= limit * 2:
        if len(cluster1) <= limit * 2:
            print("Anomaly Detected !!!")
            anomaly.append(cluster1)
            temp = 1
        else:
            temp = 0
            if counter < numberOfCluster:
                counter = counter + 1
                succesGroups.append(cluster1)
            print("cluster - counter ", len(cluster1), " - ", counter)
            print(limit, " FINISHED")
    else:
        temp = 0
        print("Right Node Starting...", len(cluster1))
        if (counter == numberOfCluster):
            return anomaly, temp, counter

        if counter == numberOfCluster - 1:
            return anomaly, temp, counter

        if counter <= numberOfCluster - 2:
            temp2, temp, counter = recursively(cluster1, [cluster_label, new_centroids][1], total_iteration, anomaly,
                                               counter, temp)

        if temp == 1:
            counter = counter + 1
            succesGroups.append(cluster1)
            temp = 0
            print("cluster - counter ", len(cluster1), " - ", counter)
        print("Right Node Finished...")

    return anomaly, temp, counter


if __name__ == "__main__":

    fileName = 'breast-cancer-unsupervised-ad.csv'
    data_points = np.genfromtxt(fileName, delimiter=',')

    df = []
    normalized_data = []
    i = 0
    for i in range(0, len(data_points)):
        for j in range(0, len(data_points[i])):
            if np.isnan(data_points[i][j]):
                data_points[i][j] = np.nan_to_num(data_points[i][j])

    normalized_data = preprocessing.normalize(data_points)

    centroids = create_centroids(len(data_points[0]))
    total_iteration = 1
    anomaly = []
    succesGroups = []  # yeni eklendi
    counter = 0
    temp = 0
    anomaly, temp, counter = recursively(normalized_data, centroids, total_iteration, anomaly, counter, temp)

    #DOSYAYA YAZDIRMA

    i = -1
    j = -1
    anomalyIndexes = []
    extraordinary = 0

    for z in range(0, len(anomaly)):
        i = i + 1
        for x in range(0, len(anomaly[i])):
            for y in range(0, len(normalized_data)):
                flag = True
                for t in range(0, len(normalized_data[0])):
                    if flag:
                        if anomaly[z][x][t] == normalized_data[y][t]:
                            if t == len(normalized_data[0]) - 1:
                                anomalyIndexes.append(y)
                        else:
                            flag = False

                    else:
                        continue

    with open(fileName, 'r') as csvinput:
        with open('kMeansClusteringOutput.csv', 'w',newline='') as csvoutput:
            writer = csv.writer(csvoutput)
            indexNumber = 0
            for row in csv.reader(csvinput):
                if anomalyIndexes.__contains__(indexNumber):
                    writer.writerow(row + ['99'])
                else:
                    writer.writerow(row + ['cluster_label'])
                for value in row:
                    if value == 'o':
                        extraordinary = extraordinary + 1
                indexNumber = indexNumber + 1

    # DOSYAYA YAZDIRMA

    print("Number of Anomaly Groups: ", len(anomaly))
    print("Number of Success Groups: ", len(succesGroups))
    accuracy = (len(anomalyIndexes) + extraordinary) / len(normalized_data)
    print("Accuracy : ",accuracy)
