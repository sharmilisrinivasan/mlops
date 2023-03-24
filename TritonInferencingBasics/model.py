import triton_python_backend_utils as pb_utils

import numpy as np

#  ----------------------- Imports from Detection -----------------------
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
#  ------------------------------------------------------------------------


class TritonPythonModel:

    def initialize(self, args):
        """
        `initialize` is called only once when the model is initially loaded
        """

        # ------------ Add any model initialization code here -------------
        nltk.data.path.append('/mnt/data/model_repository/sentiment-nltk-service/1/resources/nltk')
        self.model = SentimentIntensityAnalyzer()
        # -----------------------------------------------------------------

        print('Initialized...')

    def execute(self, requests):
        """
        `execute` is called for every inference request
        """

        responses = []

        for request in requests:

            in_text = pb_utils.get_input_tensor_by_name(request, "TEXT")
            in_text = in_text.as_numpy()[0][0].decode("utf-8")

            # -------------- Add your inference code here -------------
            try:
                score = (self.model.polarity_scores(in_text).
                         get("compound", 0.0))
                status = "Success"
            except Exception as exception:
                score = 0.0
                status = f"Failure: {exception}"
            # ------------------------------------------- -------------

            response_score = pb_utils.Tensor(
                "SCORE", np.array([score], dtype=object))
            response_status = pb_utils.Tensor(
                "STATUS", np.array([status],
                                          dtype=object))

            inference_response = pb_utils.InferenceResponse(
                output_tensors=[response_score,
                                response_status])
            responses.append(inference_response)
        return responses

    def finalize(self):
        """
        `finalize` is called only once when the model is being unloaded.
        """
        print('Cleaning up...')
