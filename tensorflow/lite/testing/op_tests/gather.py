# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Test configs for gather."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow.lite.testing.zip_test_utils import create_tensor_data
from tensorflow.lite.testing.zip_test_utils import make_zip_of_tests
from tensorflow.lite.testing.zip_test_utils import register_make_test_function


@register_make_test_function()
def make_gather_tests(options):
  """Make a set of tests to do gather."""

  test_parameters = [
      {
          "params_dtype": [tf.float32, tf.int32, tf.int64],
          "params_shape": [[10], [1, 2, 20]],
          "indices_dtype": [tf.int32, tf.int64],
          "indices_shape": [[3], [5]],
          "axis": [-1, 0, 1],
      },
      {
          # TODO(b/123895910): add Nd support for strings.
          "params_dtype": [tf.string],
          "params_shape": [[8]],
          "indices_dtype": [tf.int32],
          "indices_shape": [[3]],
          "axis": [0],
      }
  ]

  def build_graph(parameters):
    """Build the gather op testing graph."""
    params = tf.compat.v1.placeholder(
        dtype=parameters["params_dtype"],
        name="params",
        shape=parameters["params_shape"])
    indices = tf.compat.v1.placeholder(
        dtype=parameters["indices_dtype"],
        name="indices",
        shape=parameters["indices_shape"])
    axis = min(len(parameters["params_shape"]), parameters["axis"])
    out = tf.gather(params, indices, axis=axis)
    return [params, indices], [out]

  def build_inputs(parameters, sess, inputs, outputs):
    params = create_tensor_data(parameters["params_dtype"],
                                parameters["params_shape"])
    indices = create_tensor_data(parameters["indices_dtype"],
                                 parameters["indices_shape"], 0,
                                 parameters["params_shape"][0] - 1)
    return [params, indices], sess.run(
        outputs, feed_dict=dict(zip(inputs, [params, indices])))

  # Note that TF can't execute with index=1 and params_shape=[10].
  make_zip_of_tests(
      options,
      test_parameters,
      build_graph,
      build_inputs,
      expected_tf_failures=12)
