import numpy as np
import os
import random

def compute_euclidean_distance(point, centroid):
    return np.sqrt(np.sum((point - centroid)**2))

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
                distance[index_centroid] = compute_euclidean_distance(data_points[index_point], centroids[index_centroid])
            label = assign_label_cluster(distance, data_points[index_point], centroids)
            centroids[label[0]] = compute_new_centroids(label[1], centroids[label[0]])

            if iteration == (total_iteration - 1):
                cluster_label.append(label)

    return [cluster_label, centroids]

def create_centroids():
    centroids = []
    centroids.append([random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9),
                      random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9),
                      random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9),
                      random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9),
                      random.randint(1, 9), random.randint(1, 9)])
    centroids.append([random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9),
                      random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9),
                      random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9),
                      random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9),
                      random.randint(1, 9), random.randint(1, 9)])
    return np.array(centroids)

def recursively(data_points, centroids, total_iteration, anomaly, counter, temp):
    cluster0 = []
    cluster1 = []
    temp2 = []
    successNode = 7
    [cluster_label, new_centroids] = iterate_k_means(data_points, centroids, total_iteration)
        
    for data in [cluster_label, new_centroids][0]:
        if data[0] == 0:
            cluster0.append(data[1])
        else:
            cluster1.append(data[1])
    print(len(cluster0), len(cluster1))
    if(len(cluster0) <= successNode):
        if(len(cluster0) < successNode):
            print("Anomaly Detected !!!")
            anomaly.append(cluster0)
            temp = 1
        else:
            temp = 0
            counter = counter + 1
            print("cluster - counter ", len(cluster0), " - ", counter)
            print(successNode, " FINISHED")
    else:
        temp = 0
        print("Left Node Starting...", len(cluster0))
        temp2, temp, counter = recursively(cluster0, [cluster_label, new_centroids][1], total_iteration, anomaly, counter, temp)
        if( temp == 1):
            counter = counter + 1
            temp = 0
            print("cluster - counter ", len(cluster0), " - ", counter)
        print("Left Node Finished...")
    if(len(cluster1) <= successNode):
        if(len(cluster1) < successNode):
            print("Anomaly Detected !!!")
            anomaly.append(cluster1)
            temp = 1
        else:
            temp = 0
            counter = counter + 1
            print("cluster - counter ", len(cluster1), " - ", counter)
            print(successNode, " FINISHED")
    else:
        temp = 0
        print("Right Node Starting...", len(cluster1))
        temp2, temp, counter = recursively(cluster1, [cluster_label, new_centroids][1], total_iteration, anomaly, counter, temp)
        if (temp == 1):
            counter = counter + 1
            temp = 0
            print("cluster - counter ", len(cluster1), " - ", counter)
        print("Right Node Finished...")
        
    return anomaly, temp, counter


if __name__ == "__main__":
    filename = os.path.dirname(__file__) + "lymphoX.csv"
    data_points = np.genfromtxt(filename, delimiter=",")
    centroids = create_centroids()
    total_iteration = 100
    anomaly = []
    counter = 0
    temp = 0
    anomaly, temp, counter = recursively(data_points, centroids, total_iteration, anomaly, counter, temp)
    print(anomaly)
    print("Number of Anomaly Groups: ",len(anomaly))
    print("Number of Success Groups: ", counter)
