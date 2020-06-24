from secret_keys import LF_API_KEY, LF_API_SECRET, MONGODB_CONNECTION
import pymongo
myclient = pymongo.MongoClient(MONGODB_CONNECTION)
guilds = myclient.overall.guilds

class AllGuildSettingsModel():
    def __init__(self):
        pass

    def get_guild_settings(self, id):
        print(id)
        return guilds.find_one({'id': f'{id}'})

    def set_guild_settings(self, id, **kwargs):
        new_settings = self.get_guild_settings(id)

        print(new_settings)
        print(kwargs)
        for key in kwargs.keys():
            new_settings[key] = kwargs[key]

        try:
            myquery = { 'id': f'{id}' }
            newvalues = { '$set':  new_settings }
            guilds.update_one(myquery, newvalues)
        except Exception as e:
            print(e)