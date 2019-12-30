FROM ubuntu:18.04
ENV OPENCV_VERSION 4.2.0
ENV nproc 4

# Install all dependencies for OpenCV
RUN apt-get -y update && \
    apt-get -y install \
        python3 \
        python3-dev \
        python3-pip \
        git \
        wget \
        unzip \
        cmake \
        build-essential \
        pkg-config \
        libatlas-base-dev \
        gfortran \
        libgtk2.0-dev \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libv4l-dev \
        libx264-dev \
        ffmpeg \
        && \
    # Python dependencies
    pip3 install numpy \
    && \
    # Get OpenCV
    wget https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip -O opencv.zip && \
    unzip -q opencv.zip && \
    mv /opencv-$OPENCV_VERSION /opencv && \
    rm opencv.zip \
    && \
    # Build
    mkdir /opencv/build && cd /opencv/build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D BUILD_PYTHON_SUPPORT=ON \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D BUILD_EXAMPLES=OFF \
      -D PYTHON_DEFAULT_EXECUTABLE=/usr/bin/python3 \
      -D BUILD_opencv_python3=ON \
      -D BUILD_opencv_python2=OFF \
      -D WITH_IPP=OFF \
      -D WITH_FFMPEG=ON \
      -D WITH_V4L=ON .. \
    && \
    # Install
    cd /opencv/build && \
    make -j$(nproc) && \
    make install && \
    ldconfig \
    && \
    # Clean
    apt-get -y remove \
        python3-dev \
        libatlas-base-dev \
        gfortran \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libv4l-dev \
    && \
    apt-get clean && \
    rm -rf /opencv /var/lib/apt/lists/*

# Copy application to container
COPY . big-fiubrother-interpolator

# Set working directory
WORKDIR /big-fiubrother-interpolator

# Install dependencies for application
RUN pip3 install .

# Define default command.
CMD ["./run.py"]