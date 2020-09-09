from db import db

feeds_collection = db.get_feeds_twitter_collection()


async def db_get_feeds(limit=100):
    cursor = feeds_collection.find()
    return await cursor.to_list(length=limit)


async def db_add_feed(user_id, channel_id):
    feed_document = await feeds_collection.find_one({"_id": str(user_id)})

    if feed_document is None:
        await db_create_new_feed(user_id, channel_ids=[str(channel_id)])
        return True

    if str(channel_id) not in feed_document["channelIds"]:
        myquery = {"_id": str(user_id)}
        newvalues = feed_document
        newvalues["channelIds"].append(str(channel_id))

        await feeds_collection.update_one(myquery, {"$set": newvalues})
        return False

    else:
        return None


async def db_delete_feed(user_id, channel_id):
    feed_document = await feeds_collection.find_one({"_id": str(user_id)})

    if feed_document is None:
        return False

    if str(channel_id) in feed_document["channelIds"]:
        myquery = {"_id": str(user_id)}
        newvalues = feed_document
        newvalues["channelIds"].remove(str(channel_id))

        if len(newvalues["channelIds"]) == 0:
            await feeds_collection.delete_one(myquery)
        else:
            await feeds_collection.update_one(myquery, {"$set": newvalues})
        return True


async def db_create_new_feed(
            id, *,
            channel_ids
        ):
    newvalues = {
        "_id":                str(id),
        "channelIds":         channel_ids
    }
    await feeds_collection.insert_one(newvalues)
    return
