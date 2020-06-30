# README.md

This project is still in the early stages, but started based on a desire to have a searchable datastore of D&D 5e monsters that contain some additional metadata that doesn't appear in the originating SRD document. In particular, I wanted to have the means of generating a series of encounters based on "zones of influence" starting from a central high CR creature and expanding out based on environment and environmental effects.

## Requirements

Note: some of the steps below imply use of a Debian Linux variant. Originally, implemented on a modern Ubuntu.

- Python 2.7
- Docker

## Install Docker

On a Debian variant:

```
sudo apt-get install docker.io --install-suggests
```

Verify docker install

```
sudo docker run --rm -ti ubuntu:latest /bin/bash
```

### ElasticSearch

Download elasticsearch docker

```
sudo docker pull docker.elastic.co/elasticsearch/elasticsearch:6.2.3
```

Start your new docker container

```
sudo docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --name elastic docker.elastic.co/elasticsearch/elasticsearch:6.2.3
```

### Kibana

Download kibana docker

```
sudo docker pull docker.elastic.co/kibana/kibana:6.2.3
```

Run kibana docker

```
sudo docker run --rm --link elastic:elastic-url -e "ELASTICSEARCH_URL=http://elastic-url:9200"  -p 5601:5601 --name kibana docker.elastic.co/kibana/kibana:6.2.3
```

## Load Data Into ElasticSearch

Remove license from json file

- TBD - notes to do this OR provide script

Index content of json file

```
cat <5e-SRD-Monsters.json> | jq -c '.[] | {"index": {"_index": "monsters", "_type": "monster", "_id": .name}}, .' | curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/_bulk --data-binary @-
```

