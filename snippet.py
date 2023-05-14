# I wrote this code in about 4 hours, without *direct* help of ChatGPT
# i.e. only asked e.g. how to load hdf5 using h5py and similar stuff.
# I beleive ChatGPT could generate a _somewhat_ similar code in few prompts.
# also I missed deleteing tracks that's already in the given list (user history).

from typing import List, Tuple
import h5py
import pandas as pd

# Note: id of the first track is 0, unlike db which starts with 1.


def load_data():
    with h5py.File('similarity_matrix.h5', 'r') as f:
        print("Loading HDF5 File...")
        similarity_matrix = f['scores'][()].tolist()

    print("Loading CSV File...")
    df = pd.read_csv('tracks_data.csv')

    return similarity_matrix, df


similarity_matrix, df = load_data()


def get_recommendation_ids_list(track_id_list: List[int]) -> List[int]:
    recommend_set = set()
    for trackId in track_id_list:
        recommend_set.update(get_similarity_array(trackId))

    return list(recommend_set)


def get_similarity_array(track_id: int):
    return similarity_matrix[track_id]


def get_tracks_details(recommend_id_list: List[int]):
    tracks_details = []
    for trackId in recommend_id_list:
        tracks_details.append(get_track_object(trackId))
    return tracks_details


def get_track_object(track_id: int):
    df_track = df.iloc[track_id]
    return {'id': track_id,
            'title':  df_track['track_name'],
            'genre': df_track['genre'],
            'duration': int(df_track['len']),
            'releaseDate': int(df_track['release_date']),
            'artist': {'name': df_track['artist_name']}
            }


# Uncomment me.
# ids that you want to get recommendations for
# id_list = [1, 2, 3]
# print("Recommendation for ids: ", id_list)
# recommended_ids_list = get_recommendation_ids_list(id_list)

# print("Recommended ids: ", recommended_ids_list)
# recommended_tracks = get_tracks_details(recommended_ids_list)

# print("Recommended tracks: ", recommended_tracks)
