
def create_index(client, index_name):
    mapping = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "content": {
                    "type": "text",
                    "analyzer": "standard"
                },
                "timestamp": {
                    "type": "date"
                }
            }
        }
    }
    if not client.indices.exists(index=index_name):
        response = client.indices.create(index=index_name, body=mapping)
        return response
    else:
        return {"message": "Index already exists"}
