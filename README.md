# big-fiubrother-interpolator
Big Fiubrother Face Video Interpolator

### Prerequisites

- docker

### Configuration

Before running, proper configuration should be considered. Inside the folder *config/* create a yaml file with the desired settings. By default, the application will try to load *config/development.yml*.

### Install

```
docker build -t opencv .
```

### Run

```
docker run -it opencv --network="host"
```