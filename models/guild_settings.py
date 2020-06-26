from secret_keys import LF_API_KEY, LF_API_SECRET, MONGODB_CONNECTION
import pymongo
myclient = pymongo.MongoClient(MONGODB_CONNECTION)
guilds = myclient.overall.guilds

class AllGuildSettingsModel():
    def __init__(self):
        self._default = {
            '_id' : None,
            'prefix' : '~'
        }

    def get_guild_settings(self, id):
        print(id)
        return guilds.find_one({'_id': f'{id}'})

    def set_guild_settings(self, id, **kwargs):

        new_settings = self.get_guild_settings(id)
        new_entry = False

        if new_settings == None:
            new_entry = True
            new_settings = self._default
            new_settings['_id'] = str(id)

        for key in kwargs.keys():
            new_settings[key] = kwargs[key]

        if new_entry:
            try:
                guilds.insert_one(new_settings)
            except Exception as e:
                print(e)
        else:
            try:
                myquery = { '_id': f'{id}' }
                newvalues = { '$set':  new_settings }
                guilds.update_one(myquery, newvalues)
            except Exception as e:
                print(e)