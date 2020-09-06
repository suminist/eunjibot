from db import db

users_collection = db.get_users_collection()


async def db_set_lf_username(user_id, lf_username):
    user_document = await users_collection.find_one({"_id": str(user_id)})

    if user_document is None:
        await db_create_new_user(
            user_id,
            lf_username=lf_username
            )
        return

    myquery = {"_id": str(user_id)}
    newvalues = {"$set": {"lfUsername": lf_username}}
    users_collection.update_one(myquery, newvalues)


async def db_get_lf_username(user_id):
    user_document = await users_collection.find_one({"_id": str(user_id)})
    if user_document is None:
        return None

    if "lfUsername" in user_document:
        lf_username = user_document['lfUsername']
        return lf_username


async def db_create_new_user(
            user_id, *,
            lf_username
        ):
    newvalues = {
        "_id":                  str(user_id),
        "lfUsername":           lf_username
    }
    await users_collection.insert_one(newvalues)
    return
