import os
from typing import TYPE_CHECKING, Optional

import lightgbm

from ray.air._internal.checkpointing import save_preprocessor_to_dir
from ray.air.checkpoint import Checkpoint
from ray.air.constants import MODEL_KEY

if TYPE_CHECKING:
    from ray.data.preprocessor import Preprocessor


def to_air_checkpoint(
    path: str,
    booster: lightgbm.Booster,
    preprocessor: Optional["Preprocessor"] = None,
) -> Checkpoint:
    """Convert a pretrained model to AIR checkpoint for serve or inference.

    Args:
        path: The directory path where model and preprocessor steps are stored to.
        booster: A pretrained lightgbm model.
        preprocessor: A fitted preprocessor. The preprocessing logic will
            be applied to serve/inference.
    Returns:
        A Ray Air checkpoint.
    """
    booster.save_model(os.path.join(path, MODEL_KEY))

    if preprocessor:
        save_preprocessor_to_dir(preprocessor, path)

    checkpoint = Checkpoint.from_directory(path)

    return checkpoint
