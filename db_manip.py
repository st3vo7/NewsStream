async def do_find_one(my_collection, value1):
    document = await my_collection.find_one({"name": value1})
    return document


async def do_check_one(my_collection, value1, value2):
    document = await my_collection.find_one({"name": value1, "password": value2})
    return document


async def do_insert(my_collection, value1, value2):
    document = {"name": value1, "password": value2, "headlines": [], "timer": 600}
    result = await my_collection.insert_one(document)
    return result


async def do_insert_headlines(my_collection, name, value1, value2, value3, value4):
    document = {"headline": value1, "description": value2, "url_headline": value3, "url_img": value4}
    result = await my_collection.update_one({"name": name}, {'$push': {"headlines": document}})
    return result


async def do_delete_one(my_collection, name, headline):
    result = await my_collection.update_one({"name": name}, {'$pull': {"headlines": {"headline": headline}}})
    return result


async def do_alter_timer(my_collection, name, timer_value):
    result = await my_collection.update_one({"name": name}, {'$set': {"timer": timer_value}})
    return result


async def do_alter_password(my_collection, name, new_password):
    result = await my_collection.update_one({"name": name}, {'$set': {"password": new_password}})
    return result
