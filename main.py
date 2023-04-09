import tensorflow as tf
import numpy as np
import torch
def serialize_example(feature0, feature1, feature2):
    """
    Creates a tf.Example message ready to be written to a file.
    """
    # Create a dictionary mapping the feature name to the tf.Example-compatible
    # data type.
    feature = {
        'feature0': tf.train.Feature(bytes_list=tf.train.BytesList(value=[feature0])),
        'feature1': tf.train.Feature(bytes_list=tf.train.BytesList(value=[feature1])),
        'feature2': tf.train.Feature(bytes_list=tf.train.BytesList(value=[feature2]))
    }

    # Create a Features message using tf.train.Example.

    example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
    return example_proto.SerializeToString()



smiles = [b'C1=CC2=C(C(=C1)[O-])NC(=CC2=O)C(=O)O']
caption = [b'just caption']
cid = [b'168495123']
m = serialize_example(smiles[0], caption[0], cid[0])
tf_string = tf.py_function(
    serialize_example,
    (np.array(smiles[0]), np.array(caption[0]), np.array(cid[0])),
    tf.string
)
a = tf.reshape(tf_string, ())
print(321)

