from db import db

guilds_collection = db.get_guilds_collection()


async def db_set_welcome_channel_id(guild_id, channel_id):
    guild_document = await guilds_collection.find_one({"_id": str(guild_id)})

    if guild_document is None:
        await db_create_new_guild(guild_id, welcome_channel_id=channel_id)
        return
    else:
        myquery = {"_id": str(guild_id)}
        newvalues = guild_document
        newvalues["welcomeChannelId"] = str(channel_id)
        await guilds_collection.update_one(myquery, {"$set": newvalues})
        return


async def db_get_welcome_channel_id(guild_id):
    guild_document = await guilds_collection.find_one({"_id": str(guild_id)})
    if guild_document is None:
        return None
    else:
        if "welcomeChannelId" in guild_document:
            channel_id = guild_document["welcomeChannelId"]
            if channel_id != "None":
                return int(channel_id)
            else:
                return None
        else:
            await db_set_welcome_channel_id(guild_id, None)
            return None


async def db_create_new_guild(guild_id, *, prefix=None, welcome_channel_id=None):
    newvalues = {
        "_id":                  str(guild_id),
        "prefix":               prefix,
        "welcomeChannelId":     str(welcome_channel_id)
    }
    await guilds_collection.insert_one(newvalues)
    return
