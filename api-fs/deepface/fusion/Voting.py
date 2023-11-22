import numpy as np
import time


def vote(img1, img2, verified_list, distance_metric, voting_method):
    votings = [
        "if all true",
        "if any true",
        "based on threshold",
        "if tie = true",
        "if tie = false",
    ]
    distances = []
    thresholds = []
    verification = []
    model_names = []
    voting_result = {}

    # Simpan distances, thresholds, hasil verified untuk input di voting
    for item in verified_list:
        #         test = item.get('test')
        #         train = item.get('train')
        distances.append(item.get("distance"))
        thresholds.append(item.get("threshold"))
        verification.append(item.get("verified"))
        model_names.append(item.get("model"))

    if voting_method in votings:
        result = get_vote(distances, thresholds, verification, voting_method)

        voting_result = {
            "test": img1,
            "train": img2,
            "verified": result,
            "distances": distances,
            "model": model_names,
            "thresholds": thresholds,
            "distance_metric": distance_metric,
            "verified_by_model": verification,
            "voting_method": voting_method,
        }
        return voting_result
    else:
        raise ValueError(
            "Invalid voting method passed to vote function: {}".format(voting_method)
        )


#         def voting(verified_list, distance_metric, voting_method):
#     votings = ['if all true', 'if any true', 'based on threshold', 'if tie = true', 'if tie = false']
#     test = []
#     train = []
#     distances = []
#     thresholds = []
#     verification = []
#     model_names = []
#     durations = []
#     voting_result = {}

#     vote_tic = time.time()
#     # Simpan distances, thresholds, hasil verified untuk input di voting
#     for item in verified_list:
#         test = item.get('test')
#         train = item.get('train')
#         manual_ann = item.get('manual_annotation')
#         distances.append(item.get('distance'))
#         thresholds.append(item.get('threshold')),
#         verification.append(item.get('verified')),
#         model_names.append(item.get('model')),
#         durations.append(item.get('duration'))

#     if voting_method in votings:
#         result = vote(distances, thresholds, verification, voting_method)
#         vote_toc = time.time()
#         duration = round((vote_toc-vote_tic)+ sum(durations), 2)
#         voting_result = {
#             'test': test,
#             'train': train,
#             'manual_annotation': manual_ann,
#             'model_names': model_names,
#             'distance_metric': distance_metric,
#             'distances': distances,
#             'thresholds': thresholds,
#             'verified_by_model': verification,
#             'voting_method': voting_method,
#             'voting_result': result,
#             'duration': duration
#         }
#         return voting_result
#     else:
#         raise ValueError("Invalid voting method passed to vote function: {}".format(voting_method))


def get_vote(distances, thresholds, verification, voting_method):
    if voting_method == "if any true":
        if True in verification:
            return True
        else:
            return False

    elif voting_method == "if all true":
        if all(verification):
            return True
        else:
            return False

    elif voting_method == "if tie = true":
        if verification.count(True) >= verification.count(False):
            return True
        else:
            return False

    elif voting_method == "if tie = false":
        if verification.count(True) > verification.count(False):
            return True
        else:
            return False

    elif voting_method == "based on threshold":
        if verification.count(True) > verification.count(False):
            return True
        elif verification.count(True) == verification.count(False):
            avg_distance = np.mean(distances)
            avg_threshold = np.mean(thresholds)

            return avg_distance < avg_threshold
        else:
            return False
    else:
        raise ValueError(
            "Invalid voting method passed to get_vote function: {}".format(
                voting_method
            )
        )
