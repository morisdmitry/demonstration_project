class UserDAO:
    def __init__(self, db_client):
        self.client = db_client

    async def add(self, params):
        return await self.client.records.insert_one(params)

    async def update(self, field: dict, params: dict):
        return await self.client.records.update_one(field, {"$set": params})

    async def get(self, field: dict):
        return await self.client.records.find_one(field)

    async def delete(self, field: dict):
        return await self.client.records.delete_one(field)


class CacheDAO:
    def __init__(self, client):
        self.client = client

    async def add(self, key, value):
        return await self.client.set(key, value)

    async def get(self, key):
        return await self.client.get(key)
