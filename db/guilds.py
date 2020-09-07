from db import db

guilds_collection = db.get_guilds_collection()


async def db_set_prefix(guild_id, prefix):
    guild_document = await guilds_collection.find_one({"_id": str(guild_id)})

    if guild_document is None:
        await db_create_new_guild(guild_id, prefix=prefix)
        return
    else:
        myquery = {"_id": str(guild_id)}
        newvalues = guild_document
        newvalues["prefix"] = str(prefix)

        await guilds_collection.update_one(myquery, {"$set": newvalues})
        return


async def db_get_prefix(guild_id):
    guild_document = await guilds_collection.find_one({"_id": str(guild_id)})
    if guild_document is None:
        return None

    prefix = guild_document["prefix"]
    return prefix


async def db_set_moderator_role_id(guild_id, moderator_role_id):
    guild_document = await guilds_collection.find_one({"_id": str(guild_id)})

    if guild_document is None:
        await db_create_new_guild(guild_id, moderator_role_id=moderator_role_id)
        return
    else:
        myquery = {"_id": str(guild_id)}
        newvalues = guild_document
        newvalues["moderatorRoleId"] = str(moderator_role_id)

        await guilds_collection.update_one(myquery, {"$set": newvalues})
        return


async def db_get_moderator_role_id(guild_id):
    guild_document = await guilds_collection.find_one({"_id": str(guild_id)})
    if guild_document is None:
        return None

    moderator_role_id = guild_document["moderatorRoleId"]
    return moderator_role_id


async def db_set_welcome(
            guild_id, *,
            welcome_channel_id=None,
            welcome_title=None,
            welcome_content=None,
            welcome_image_url=None
        ):
    guild_document = await guilds_collection.find_one({"_id": str(guild_id)})

    if guild_document is None:
        await db_create_new_guild(
            guild_id,
            welcome_channel_id=welcome_channel_id,
            welcome_title=welcome_title,
            welcome_content=welcome_content,
            welcome_image_url=welcome_image_url
            )
        return
    else:
        myquery = {"_id": str(guild_id)}
        newvalues = guild_document
        if welcome_channel_id is not None:
            newvalues["welcomeChannelId"] = str(welcome_channel_id)

        if welcome_title is not None:
            newvalues["welcomeTitle"] = welcome_title

        if welcome_content is not None:
            newvalues["welcomeContent"] = welcome_content

        if welcome_image_url is not None:
            newvalues["welcomeImageUrl"] = welcome_image_url

        await guilds_collection.update_one(myquery, {"$set": newvalues})
        return


async def db_get_welcome(guild_id):
    guild_document = await guilds_collection.find_one({"_id": str(guild_id)})
    if guild_document is None:
        return None

    welcome_info = {}

    if "welcomeChannelId" in guild_document and guild_document["welcomeChannelId"] != "None":
        welcome_info["channel_id"] = int(guild_document["welcomeChannelId"])
    else:
        welcome_info["channel_id"] = None

    if "welcomeTitle" in guild_document and guild_document["welcomeTitle"] != "None":
        welcome_info["title"] = guild_document["welcomeTitle"]
    else:
        welcome_info["title"] = None

    if "welcomeContent" in guild_document and guild_document["welcomeContent"] != "None":
        welcome_info["content"] = guild_document["welcomeContent"]
    else:
        welcome_info["content"] = None

    if "welcomeImageUrl" in guild_document and guild_document["welcomeImageUrl"] != "None":
        welcome_info["image_url"] = guild_document["welcomeImageUrl"]
    else:
        welcome_info["image_url"] = None

    return welcome_info


async def db_create_new_guild(
            guild_id, *,
            prefix=None,
            moderator_role_id=None,
            welcome_channel_id=None,
            welcome_title=None,
            welcome_content=None,
            welcome_image_url=None
        ):
    newvalues = {
        "_id":                  str(guild_id),
        "prefix":               prefix,
        "moderatorRoleId":      str(moderator_role_id),
        "welcomeChannelId":     str(welcome_channel_id),
        "welcomeTitle":         str(welcome_title),
        "welcomeContent":       str(welcome_content),
        "welcomeImageUrl":      str(welcome_image_url)
    }
    await guilds_collection.insert_one(newvalues)
    return
