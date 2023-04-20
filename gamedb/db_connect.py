import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

GAME_DB = 'gamedb'

client = None

MONGO_ID = '_id'


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Also set global client variable.
    """
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = os.environ.get("GAME_MONGO_PW")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://gcallah:{password}'
                                    + '@cluster0.eqxbbqd.mongodb.net/'
                                    + '?retryWrites=true&w=majority')
            # PA recommends these settings:
            # + 'connectTimeoutMS=30000&'
            # + 'socketTimeoutMS=None
            # + '&connect=false'
            # + 'maxPoolsize=1')
            # but they don't seem necessary
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()


def insert_one(collection, doc, db=GAME_DB):
    """
    Insert a single doc into collection.
    """
    connect_db()
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def fetch_one(collection, filt, db=GAME_DB):
    """
    Find with a filter and return on the first doc found.
    """
    connect_db()
    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        return doc


def del_one(collection, filt, db=GAME_DB):
    """
    Find with a filter and return on the first doc found.
    """
    connect_db()
    result = client[db][collection].delete_one(filt)
    return result.deleted_count


def fetch_all(collection, db=GAME_DB):
    connect_db()
    ret = []
    for doc in client[db][collection].find():
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=GAME_DB):
    connect_db()
    ret = {}
    for doc in client[db][collection].find():
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret


def append_to_list(collection, filt_nm, filt_val,
                   list_nm, new_list_item, db=GAME_DB):
    """
    Retrieve documents with a filter and then append
    new item to the field specified.
    """
    connect_db()
    return client[db][collection].update_one(
        {filt_nm: filt_val},
        {'$push': {list_nm: new_list_item}},
        upsert=True
    )
