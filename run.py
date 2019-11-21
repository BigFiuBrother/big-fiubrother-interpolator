#!/usr/bin/env python3

import queue
import signal
import multiprocessing
from big_fiubrother_core import (
    SignalHandler,
    StoppableThread,
    PublishToRabbitMQ,
    ConsumeFromRabbitMQ,
    setup
)
from big_fiubrother_interpolator import (
    FetchVideoData,
    StoreVideoInFileSystem,
    InterpolateVideo,
    ReadInterpolatedVideo,
    StoreInterpolatedVideoInDB
)


def fetch_video(configuration, interprocess_queue):
    consumer_to_fetch_data_queue = queue.Queue()
    fetch_data_to_store_video_queue = queue.Queue()

    consumer = StoppableThread(
        ConsumeFromRabbitMQ(configuration=configuration['consumer'],
                            output_queue=consumer_to_fetch_data_queue))

    video_data_retriever = StoppableThread(
        FetchVideoData(configuration=configuration,
                       input_queue=consumer_to_fetch_data_queue,
                       output_queue=fetch_data_to_store_video_queue))

    file_system_video_storage = StoppableThread(
        StoreVideoInFileSystem(configuration=configuration,
                               input_queue=fetch_data_to_store_video_queue,
                               output_queue=interprocess_queue))

    signal_handler = SignalHandler(callback=consumer.stop)

    file_system_video_storage.start()
    video_data_retriever.start()
    consumer.run()

    # Signal STOP received!
    video_data_retriever.stop()
    file_system_video_storage.stop()

    video_data_retriever.wait()
    file_system_video_storage.wait()


def interpolate_video(configuration, input_queue, output_queue):
    video_interpolator = StoppableThread(
        InterpolateVideo(configuration=configuration,
                         input_queue=input_queue,
                         output_queue=output_queue))

    signal_handler = SignalHandler(callback=video_interpolator.stop)

    video_interpolator.run()


def publish_video(configuration, interprocess_queue):
    reader_to_storage_queue = queue.Queue()
    reader_to_publisher_queue = queue.Queue()

    video_reader = StoppableThread(
        ReadInterpolatedVideo(input_queue=interprocess_queue,
                              publisher_queue=reader_to_publisher_queue,
                              storage_queue=reader_to_storage_queue
                              ))

    db_storage = StoppableThread(
        StoreInterpolatedVideoInDB(configuration=configuration,
                                   input_queue=reader_to_storage_queue))

    publisher = StoppableThread(
        PublishToRabbitMQ(configuration=configuration['publisher'],
                          input_queue=reader_to_publisher_queue))

    signal_handler = SignalHandler(
        processes=[video_reader, db_storage, publisher])

    publisher.start()
    db_storage.start()
    video_reader.start()

    video_reader.wait()
    db_storage.wait()
    publisher.wait()


if __name__ == "__main__":
    configuration = setup(
        application_name='Big Fiubrother Interpolation Application')

    print('[*] Configuring big-fiubrother-interpolator')

    fetch_to_interpolate_queue = multiprocessing.Queue()
    interpolate_to_publish_queue = multiprocessing.Queue()

    fetch_process = multiprocessing.Process(
        target=fetch_video,
        args=(configuration, fetch_to_interpolate_queue))

    interpolate_process = multiprocessing.Process(
        target=interpolate_video,
        args=(configuration,
              fetch_to_interpolate_queue,
              interpolate_to_publish_queue))

    store_process = multiprocessing.Process(
        target=publish_video,
        args=(configuration, interpolate_to_publish_queue))

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    print('[*] Configuration finished. Starting big-fiubrother-interpolator!')

    fetch_process.start()
    interpolate_process.start()
    store_process.start()

    fetch_process.join()
    interpolate_process.join()
    store_process.join()

    print('[*] big-fiubrother-interpolator stopped!')
