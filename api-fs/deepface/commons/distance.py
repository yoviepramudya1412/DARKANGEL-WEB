import numpy as np
from deepface import DeepFace
from scipy.spatial.distance import cityblock


def findCosineDistance(source_representation, test_representation):
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))


def findEuclideanDistance(source_representation, test_representation):
    if type(source_representation) == list:
        source_representation = np.array(source_representation)

    if type(test_representation) == list:
        test_representation = np.array(test_representation)

    euclidean_distance = source_representation - test_representation
    euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
    euclidean_distance = np.sqrt(euclidean_distance)
    return euclidean_distance


def l2_normalize(x):
    return x / np.sqrt(np.sum(np.multiply(x, x)))


def findManhattanDistance(source_representation, test_representation):
    distance = cityblock(source_representation, test_representation)
    return distance


def l1_normalize(x):
    abs_sum = np.sum(np.abs(x))
    return x / abs_sum


def findThreshold(model_name, distance_metric):
    base_threshold = {
        "cosine": 0.40,
        "euclidean": 0.55,
        "euclidean_l2": 0.75,
        "mahalanobisCosine": 0.50,
        "manhattan": 0.50,
    }

    thresholds = {
        "VGG-Face": {"cosine": 0.41, "euclidean": 0.60, "euclidean_l2": 0.86},
        "Facenet": {"cosine": 0.67, "euclidean": 10, "euclidean_l2": 0.80},
        "Facenet512": {"cosine": 0.30, "euclidean": 23.56, "euclidean_l2": 1.04},
        "ArcFace": {"cosine": 0.68, "euclidean": 4.15, "euclidean_l2": 1.13},
        # TODO: find the best threshold values
        "SFace": {
            "cosine": 0.5932763306134152,
            "euclidean": 10.734038121282206,
            "euclidean_l2": 1.055836701022614,
        },
        "OpenFace": {"cosine": 0.10, "euclidean": 0.55, "euclidean_l2": 0.55},
        # use new best threshold
        "DeepFace": {"cosine": 0.23, "euclidean_l2": 0.67, "manhattan_l1": 0.74},
        "DeepID": {"cosine": 0.02, "euclidean_l2": 0.21, "manhattan_l1": 0.22},
        "Dlib": {"cosine": 0.08, "euclidean_l2": 0.41, "manhattan_l1": 0.42},
        "Seresnet18": {"cosine": 0.99, "euclidean_l2": 1.41, "manhattan_l1": 1.99},
    }

    threshold = thresholds.get(model_name, base_threshold).get(distance_metric, 0.4)

    return threshold
