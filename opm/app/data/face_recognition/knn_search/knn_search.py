import os
import pickle
import json
import numpy as np
from pathlib import Path
from loguru import logger
from ....settings.settings import settings


class KnnSearch:
    distance_threshold = 0.6

    def __init__(self):
        pass

    def load_models(self):
        logger.debug("Loading KNN model")
        model_dir = self.ensure_model_dir()
        knn_model_path = model_dir / settings.local_knn_model
        index_map_path = model_dir / settings.local_index_map
        # Check if knn model file exists and then attempt to load it
        if os.path.exists(knn_model_path):
            try:
                with open(knn_model_path, 'rb') as f:
                    loaded_knn_model = pickle.load(f)
            except Exception as e:
                logger.debug(f"Error loading KNN model: {e}")
                loaded_knn_model = None
        else:
            logger.debug(f"KNN model file not found: {knn_model_path}")
            loaded_knn_model = None

        # Check if index map file exists and then attempt to load it
        if os.path.exists(index_map_path):
            try:
                with open(index_map_path, 'r') as f:
                    index_map = json.load(f)
            except Exception as e:
                logger.debug(f"Error loading index map: {e}")
                index_map = None
        else:
            logger.debug(f"Index map file not found: {index_map_path}")
            index_map = None

        self.knn_model = loaded_knn_model
        if index_map is not None:
            self.index_vs_id_dict = {int(k): v for k, v in index_map.items()}
        else:
            self.index_vs_id_dict = {}

    def search(self, embeddings):
        if self.knn_model is None:
            return None
        unknown_person_embedding = embeddings.reshape(
            1, -1)
        distances, indices = self.knn_model.kneighbors(
            unknown_person_embedding)
        min_distance_index = np.argmin(distances, axis=1)
        min_distance_value = distances[0, min_distance_index]
        if min_distance_value > self.distance_threshold:
            return None
        index = indices[0, min_distance_index]
        matched_person_id = self.index_vs_id_dict[index[0]]
        return matched_person_id

    def ensure_model_dir(self) -> Path:
        model_dir = Path.home() / settings.app_directory / settings.knn_directory
        if not model_dir.exists():
            model_dir.mkdir(parents=True)
        return model_dir
