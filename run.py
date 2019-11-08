#!/usr/bin/env python3

from queue import Queue
from big_fiubrother_core import (
    SignalHandler,
    StoppableThread,
    PublishToRabbitMQ,
    ConsumeFromRabbitMQ,
    setup
)
from big_fiubrother_interpolator import (
    FetchVideoChunk,
    FetchBoundingBoxes,
    InterpolateVideo
)


if __name__ == "__main__":
    setup(application_name='Big Fiubrother Interpolation Application')

    print('[*] Configuring big-fiubrother-interpolator')

    consumer_to_video_chunk_retriever_queue = Queue()
    video__queue = Queue()
    consumer_to_interpolation_queue = Queue()
    interpolation_to_publisher_queue = Queue()

    consumer = StoppableThread(
        ConsumeFromRabbitMQ(configuration=configuration['consumer'],
                            output_queue=consumer_to_interpolation_queue))

    video_chunk_retriever = StoppableThread(
        FetchVideoChunk(configuration=configuration,
                        input_queue=consumer_to_interpolation_queue,
                        output_queue=interpolation_to_publisher_queue))

    bounding_boxes_retriever = StoppableThread(
        FetchBoundingBoxes(configuration=configuration,
                           input_queue=consumer_to_interpolation_queue,
                           output_queue=interpolation_to_publisher_queue))

    video_interpolator = StoppableThread(
        InterpolateVideo(configuration=configuration,
                         input_queue=consumer_to_interpolation_queue,
                         output_queue=interpolation_to_publisher_queue))

    publisher = StoppableThread(
        PublishToRabbitMQ(configuration=configuration['publisher'],
                          input_queue=interpolation_to_publisher_queue))

    signal_handler = SignalHandler(callback=consumer.stop)

    print('[*] Configuration finished. Starting big-fiubrother-interpolator!')

    publisher.start()
    video_interpolator.start()
    bounding_boxes_retriever.start()
    video_chunk_retriever.start()
    consumer.run()

    # STOP signal received!
    video_chunk_retriever.stop()
    bounding_boxes_retriever.stop()
    video_interpolator.stop()
    publisher.stop()
    video_chunk_retriever.wait()
    bounding_boxes_retriever.wait()
    video_interpolator.wait()
    publisher.wait()

    print('[*] big-fiubrother-interpolator stopped!')
