from typing import Any

from .model import Model


def query_result_mapper(model_cls: Model, results: Any):
    if isinstance(results, list):
        objects = []
        for row in results:
            object = model_cls()
            for col, value in zip(model_cls.get_columns(), row):
                setattr(object, col, value)
            objects.append(object)

        return objects
    else:
        object = model_cls()
        for col, value in zip(model_cls.get_columns(), results):
            setattr(object, col, value)

        return object
