import tensorflow as tf
import numpy as np

batch_size = 50
filename_queue = tf.train.string_input_producer(['iris.data'])
reader = tf.TextLineReader()
key, value = reader.read(filename_queue)
record_defaults = [[0.0], [0.0], [0.0], [0.0], [""]]
decoded = tf.decode_csv(value, record_defaults=record_defaults)
col1, col2, col3, col4, col5 = tf.train.shuffle_batch(decoded, batch_size=batch_size, capacity=batch_size * 50, min_after_dequeue=batch_size)

#col1, col2, col3, col4, col5 = tf.decode_csv(value, record_defaults=record_defaults)
#features = tf.concat(0, [[col1], [col2], [col3], [col4]])

with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    for i in range(1000):
        example, label = sess.run([col1, col5])
        #print sess.run(decoded)
        print 'gooda'
        #example, label = sess.run([features, col5])
        print example, label
        print i
    coord.request_stop()
    coord.join(threads)

