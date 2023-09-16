<script lang="ts">
	import type { Channel } from 'src/js/interfaces';
	import MenuCategory from 'src/components/channels/MenuCategory.svelte';

	export let channels: Channel[] = [];
	export let selectedChannelId: string | null = null;
	export let selectedGuildId: string | null = null;

	let channelsByCategoryId: any = {}; // {categoryId: channels}
	let categoryId_msgCount: any = []; // {categoryId: msgCount}

	// interface Channel with channels array
	interface ChannelTree extends Channel {
		threads: Channel[];
	}

	/*function getCategoriesFromChannels(allChannels: Channel[]) {
		let threads: Channel[] = allChannels.filter(channel => channel.type === "GuildPublicThread" || channel.type === "GuildPrivateThread")
		let channels: ChannelTree[] = allChannels.filter(channel => channel.type !== "GuildPublicThread" && channel.type !== "GuildPrivateThread") // Only add to list if channel has a category

		// create channel for threads without channel
		channels.push({
			_id: '0',
			type: 'GuildTextChat',
			categoryId: '0',
			category: 'Lost threads / forums',
			name: 'Lost threads / forums',
			topic: null,
			threads: [],
			msg_count: 0,
			guildId: selectedGuildId as string,
		})

		// add channels array to all channels
		channels.forEach(channel => {
			channel.threads = []
		})
		

		// add threads to channels
		threads.forEach(thread => {
			let channel = channels.find(channel => channel._id === thread.categoryId)
			if (!channel) {
				channel = channels.find(channel => channel._id === '0')
			}
			// @ts-ignore
			channel.threads.push(thread)

			// increase msg count
			channel.msg_count += thread.msg_count
		})

		// sort threads by message count
		channels.forEach(channel => {
			channel.threads.sort((a, b) => b.msg_count - a.msg_count)
		})


		// categorise channels by category
		let channelsByCategoryId: Record<string, ChannelTree[]> = {}
		channels.forEach(channel => {
			if (channel.categoryId === null) {
				channel.categoryId = '1'  // made-up category for channels without category (we can't use null as key)
			}
			if (!channelsByCategoryId[channel.categoryId]) {
				channelsByCategoryId[channel.categoryId] = []
			}
			channelsByCategoryId[channel.categoryId].push(channel)
		})

		// sort channels by message count in each category
		Object.values(channelsByCategoryId).forEach((channels: ChannelTree[]) => {
			channels.sort((a, b) => b.msg_count - a.msg_count)
		})

		// remove lost threads category if it contains no threads
		if (channelsByCategoryId['0'][0].threads.length === 0) {
			delete channelsByCategoryId['0']
		}

		return channelsByCategoryId
	}*/

	function getCategoriesFromChannels(allChannels: Channel[]): Record<string, ChannelTree[]> {
		let threads: Channel[] = allChannels.filter(
			(channel) => channel.type === 'GuildPublicThread' || channel.type === 'GuildPrivateThread' || channel.type === 'GuildNewsThread'
		);
		let channels: ChannelTree[] = allChannels.filter(
			(channel) => channel.type !== 'GuildPublicThread' && channel.type !== 'GuildPrivateThread' && channel.type !== 'GuildNewsThread'
		);

		// Create channel for threads without channel
		channels.push({
			_id: '0',
			type: 'GuildTextChat',
			categoryId: '0',
			category: 'Lost threads / forums',
			name: 'Lost threads / forums',
			topic: null,
			threads: [],
			msg_count: 0,
			guildId: selectedGuildId as string,
			position: '999999', // A high value to ensure it's last
			categoryPosition: '999999' // A high value to ensure it's last
		});

		// Create "Forum" type channels based on threads' parentType and parentPosition
		threads.forEach((thread) => {
			if (
				thread.parentType === 'GuildForum' &&
				!channels.some((channel) => channel._id === thread.categoryId)
			) {
				console.log('Creating forum channel for thread', thread);

				channels.push({
					_id: thread.categoryId,
					type: 'GuildForum',
					categoryId: thread.parentCategoryId,
					category: thread.parentCategoryName,
					name: thread.category,
					topic: null,
					threads: [],
					msg_count: 0,
					guildId: selectedGuildId as string,
					position: thread.parentPosition,
					categoryPosition: thread.parentCategoryPosition // A high value to ensure it's last
				});
			}
		});

		// Initialize threads array for all channels
		channels.forEach((channel) => {
			channel.threads = [];
		});

		// Add threads to channels
		threads.forEach((thread) => {
			let channel = channels.find((channel) => channel._id === thread.categoryId);
			if (!channel) {
				channel = channels.find((channel) => channel._id === '0');
			}
			channel.threads.push(thread);
			channel.msg_count += thread.msg_count;
		});

		// Sort threads by their channel ID
		channels.forEach((channel) => {
			channel.threads.sort((a, b) => a._id.localeCompare(b._id));
		});

		// Categorize channels by category
		let channelsByCategoryId: Record<string, ChannelTree[]> = {};
		channels.forEach((channel) => {
			if (channel.categoryId === null) {
				channel.categoryId = '999'; // Made-up category for channels without category
			}
			if (!channelsByCategoryId[channel.categoryId]) {
				channelsByCategoryId[channel.categoryId] = [];
			}
			channelsByCategoryId[channel.categoryId].push(channel);
			console.log('channel: ', channel.categoryId);
		});

		// Sort channels by their type and position within each category
		Object.values(channelsByCategoryId).forEach((channels: ChannelTree[]) => {
			channels.sort((a, b) => {
				if (a.type === 'GuildVoiceChat' && b.type !== 'GuildVoiceChat') {
					return 1; // a is a voice channel, b is not, so a should come after b
				} else if (a.type !== 'GuildVoiceChat' && b.type === 'GuildVoiceChat') {
					return -1; // a is not a voice channel, b is, so a should come before b
				} else {
					return parseInt(a.position) - parseInt(b.position); // Both are of the same type, sort by position
				}
			});
		});

		// Sort categories by their position
		const sortedCategories = Object.entries(channelsByCategoryId).sort((a, b) => {
			const categoryA = a[1][0];
			const categoryB = b[1][0];
			return parseInt(categoryA.categoryPosition) - parseInt(categoryB.categoryPosition);
		});

		// Convert sorted categories back to an object
		const orderedCategories: Record<string, ChannelTree[]> = {};
		for (const [categoryId, channels] of sortedCategories) {
			orderedCategories[categoryId] = channels;
		}

		// Remove lost threads category if it contains no threads
		if (orderedCategories['0'][0].threads.length === 0) {
			delete orderedCategories['0'];
		}
		console.log(channelsByCategoryId);
		console.log(orderedCategories);

		return orderedCategories;
	}

	function processChannels(channels: Channel[]) {
		channelsByCategoryId = getCategoriesFromChannels(channels);
		// console.log(channels);

		// count message count in each category
		categoryId_msgCount = Object.values(channelsByCategoryId).map((channels: ChannelTree[]) => {
			return {
				categoryId: channels[0].categoryId,
				msg_count: channels.reduce((acc, channel) => acc + channel.msg_count, 0)
			};
		});

		// sort category ids by message count
		categoryId_msgCount.sort((a, b) => b.msg_count - a.msg_count);

		// put category id `1` always at the start of channel list
		let categoryId1_msgCount = categoryId_msgCount.find((obj) => obj.categoryId === '999');
		if (categoryId1_msgCount) {
			categoryId_msgCount = categoryId_msgCount.filter((obj) => obj.categoryId !== '999');
			categoryId_msgCount.unshift(categoryId1_msgCount);
		}

		categoryId_msgCount.sort((a, b) => {
			const categoryA = channelsByCategoryId[a.categoryId][0];
			const categoryB = channelsByCategoryId[b.categoryId][0];
			return parseInt(categoryA.categoryPosition) - parseInt(categoryB.categoryPosition);
		});
	}

	$: processChannels(channels);
</script>

{#each categoryId_msgCount as obj}
	{@const channels = channelsByCategoryId[obj.categoryId]}
	<MenuCategory {channels} guildId={selectedGuildId} {selectedChannelId} />
{/each}
