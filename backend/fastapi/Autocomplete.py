from pprint import pprint


def autocomplete_categories(db, guild_id: str, partial_category: str, limit: int):
	"""
	Searches for categories.
	limited to {limit} results * 10
	"""
	collection_channels = db["channels"]

	# ignore "GuildPublicThread" or "GuildPrivateThread", because their category is channel name
	query = {
		"category": {
			"$regex": partial_category,
			"$options": "i"
		},
		"guildId": guild_id,
		"type": {
			"$nin": [
				"GuildPublicThread",
				"GuildPrivateThread"
			]
		}
	}

	cursor = collection_channels.aggregate([
		{
			"$match": query
		},
		{
			"$group": {
				"_id": "$category",
				"total_msg_count": { "$sum": "$msg_count" },
				"doc": { "$first": "$$ROOT" },
			}
		},
		{
			"$limit": limit
		},
		{
			"$sort": {
				"total_msg_count": -1,
				"category": 1
			}
		}
	])

	category_names = []
	for category in cursor:
		category_names.append({
			"key": category['doc']['category'],
			"description": "",
			"description2": str(category['total_msg_count']) + " messages (without threads)",   # TODO: messages in threads are not counted
		})

	return category_names

def autocomplete_channels(db, guild_id: str, partial_channel: str, limit: int):
	"""
	Searches for channels.
	limited to {limit} results
	"""
	collection_channels = db["channels"]

	query = {
		"name": {
			"$regex": partial_channel, "$options": "i"
		},
		"guildId": guild_id
	}
	cursor = collection_channels.find(query, {
		"name": 1,
		"category": 1,
		"msg_count": 1
	}).limit(limit).sort([
		("msg_count", -1),
		("name", 1)
	])
	channel_names = []
	for channel in cursor:
		channel_names.append({
			"key": channel['name'],
			"description": channel['category'],
			"description2": str(channel['msg_count']) + " messages",
		})

	return channel_names

def autocomplete_reactions(db, guild_id: str, partial_reaction: str, limit: int):
	"""
	Searches for reactions.
	limited to {limit} results
	"""
	collection_emojis = db["emojis"]

	query = {
		"name": {
			"$regex": partial_reaction,
			"$options": "i"
		},
		"guildIds": guild_id
	}
	cursor = collection_emojis.find(query, {
		"name": 1,
		"image": 1,
		"usage_count": 1
	}).limit(limit).sort([
		("usage_count", -1),
		("name", 1)
	])
	reaction_names = []
	for reaction in cursor:
		reaction_names.append({
			"key": reaction['name'],
			"description": "",
			"description2": str(reaction['usage_count']) + "x",
			"icon": reaction['image']

		})

	return reaction_names


def autocomplete_filenames(db, guild_id: str, partial_filename: str, limit: int):
	"""
	Searches for filenames.
	limited to {limit} results
	"""
	collection_assets = db["assets"]

	query = {
		"filenameWithoutHash": {
			"$regex": partial_filename,
			"$options": "i"
		}
	}
	cursor = collection_assets.aggregate([
		{"$match": query},
		{
			"$group": {
				"_id": "$filenameWithoutHash",
				"doc": { "$first": "$$ROOT" }
			}
		},
		{"$limit": limit},
		{"$sort": {"_id": 1}}
	])


	filenames = []
	for db_result in cursor:
		filenames.append({
			"key": db_result['doc']['filenameWithoutHash'],
			"description": db_result['doc']["type"]
		})

	return filenames


def autocomplete_users(db, guild_id: str, partial_user_name: str, limit: int):
	"""
	Searches for users by name.
	limited to {limit} results
	only shows users that have messages in the guild {guild_id}
	"""
	collection_authors = db["authors"]

	query = {
		"guildIds": guild_id,
		"names": {
			"$regex": partial_user_name, "$options": "i"
		}
	}
	cursor = collection_authors.find(query, {
		"names": 1,
		"nicknames": 1,
		"msg_count": 1,
		"avatar": 1
	}).limit(limit).sort([
		("msg_count", -1),
		("names", 1)
	])
	authors= []
	for author in cursor:
		print(author)
		authors.append({
			"key": author['names'][0],
			"description": ", ".join(author['nicknames']),
			"description2": str(author['msg_count']) + " messages",
			"icon": author['avatar']
		})
	return authors