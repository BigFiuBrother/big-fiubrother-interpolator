#!/usr/bin/env python3

import queue
import signal
import multiprocessing
from big_fiubrother_core import (
    StoppableThread,
    ConsumeFromRabbitMQ,
    runtime_context,
    run
)
from big_fiubrother_interpolator import (
    FetchVideoData,
    FetchVideoChunk,
    InterpolateVideo,
    StoreProcessedVideo,
    NotifyProcessedVideo
)


def fetch_video(configuration, interprocess_queue):
    queue_1 = queue.Queue()
    
    consumer = StoppableThread(
        ConsumeFromRabbitMQ(configuration=configuration['consumer'],
                            output_queue=queue_1))

    queue_2 = queue.Queue()

    video_data_retriever = StoppableThread(
        FetchVideoData(configuration=configuration,
                       input_queue=queue_1,
                       output_queue=queue_2))

    video_chunk_retriever = StoppableThread(
        FetchVideoChunk(configuration=configuration,
                        input_queue=queue_2,
                        output_queue=interprocess_queue))

    run(processes=[video_data_retriever, video_chunk_retriever],
        main_process=consumer)


def interpolate_video(configuration, input_queue, output_queue):
    video_interpolator = StoppableThread(
        InterpolateVideo(configuration=configuration,
                         input_queue=input_queue,
                         output_queue=output_queue))

    run(main_process=video_interpolator)


def publish_video(configuration, interprocess_queue):
    queue_1 = queue.Queue()

    storage_task = StoppableThread(
        StoreProcessedVideo(configuration=configuration,
                            input_queue=interprocess_queue,
                            output_queue=queue_1))

    notify_task = StoppableThread(
        NotifyProcessedVideo(configuration=configuration, input_queue=queue_1))

    run(processes=[storage_task, notify_task])


if __name__ == "__main__":
    with runtime_context('Big Fiubrother Interpolation Application') as configuration:
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
