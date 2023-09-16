<script>
	import IconChannel from 'src/components/icons/IconChannel.svelte';
	import IconChannelWithThreads from 'src/components/icons/IconChannelWithThreads.svelte';
	import IconChannelNsfw from 'src/components/icons/IconChannelNsfw.svelte';
	import IconChannelWithThreadsNsfw from 'src/components/icons/IconChannelWithThreadsNsfw.svelte';
	import IconVoiceChannel from 'src/components/icons/IconVoiceChannel.svelte';
	import IconVoiceChannelNsfw from 'src/components/icons/IconVoiceChannelNsfw.svelte';
	import IconForumChannel from 'src/components/icons/IconForumChannel.svelte';
	import IconForumChannelNsfw from 'src/components/icons/IconForumChannelNsfw.svelte';
	import IconNewsChannel from 'src/components/icons/IconNewsChannel.svelte';
	import IconNewsChannelWithThreads from 'src/components/icons/IconNewsChannelWithThreads.svelte';
	import IconNewsChannelNsfw from 'src/components/icons/IconNewsChannelNsfw.svelte';
	import IconNewsChannelWithThreadsNsfw from 'src/components/icons/IconNewsChannelWithThreadsNsfw.svelte';
	import IconStageChannel from 'src/components/icons/IconStageChannel.svelte';
	import IconRulesChannel from 'src/components/icons/IconRulesChannel.svelte';
	import { copyTextToClipboard } from '../../js/helpers';
	import { contextMenuItems, isMenuHidden } from '../menu/menuStore';
	export let guildId;
	export let id;
	export let name;
	export let isSelected = false;
	export let threadCount = 0;
	export let type;
	export let nsfw;
	export let isRulesChannel;

	function onRightClick(e, id) {
		$contextMenuItems = [
			{
				"name": "Copy channel ID",
				"action": () => {
					copyTextToClipboard(BigInt(id))
				}
			},
			{
				"name": "Copy channel name",
				"action": () => {
					copyTextToClipboard(name)
				}
			}
		]
	}
</script>

<a
	href="/channels/{guildId}/{id}"
	on:contextmenu|preventDefault={(e) => onRightClick(e, id)}
>
	<div title="{name}" class="channel" class:selected={isSelected} on:click={()=>$isMenuHidden=true}>
		<div class="channel-icon">
			<!-- check for type first then check for threads or not and then nsfw or not -->
			{#if type == "GuildTextChat"} 
				{#if isRulesChannel}
					<IconRulesChannel/>
				{:else}
					{#if nsfw}
						{#if threadCount > 0}
							<IconChannelWithThreadsNsfw />
						{:else}
							<IconChannelNsfw />
						{/if}
					{:else if !nsfw}
						{#if threadCount > 0}
							<IconChannelWithThreads />
						{:else}
							<IconChannel />
						{/if}
					{/if}
				{/if}
			{:else if type == "GuildVoiceChat" && nsfw}
					<IconVoiceChannelNsfw />
			{:else if type == "GuildVoiceChat" && !nsfw}
					<IconVoiceChannel />
			{:else if type == "GuildNews" && nsfw}
				{#if threadCount > 0}
					<IconNewsChannelWithThreadsNsfw />
				{:else}
					<IconNewsChannelNsfw />
				{/if}
			{:else if type == "GuildNews" && !nsfw}
				{#if threadCount > 0}
					<IconNewsChannelWithThreads />
				{:else}
					<IconNewsChannel />
				{/if}
			{:else if type == "GuildForum" && nsfw}
				<IconForumChannelNsfw />
			{:else if type == "GuildForum" && !nsfw}
			<IconForumChannel />
			{:else if type == "GuildStageVoice"}
				<IconStageChannel />
			{:else}
				<IconChannel />
			{/if}

		<!-- {#if threadCount > 0}
			<IconChannelWithThreads />
		{:else if type == "GuildVoiceChat"}
			<IconVoiceChannel />
			{:else if type == "GuildNews"}
			<IconNewsChannel/>
			{:else}
			<IconChannel />
		{/if} -->
	</div>
		<div class="thread-name" class:selected={isSelected}>
			{name}
		</div>
	</div>
</a>

<style>
	.channel {
		display: flex;
		align-items: center;
		border-radius: 4px;
		width: calc(100% - 40x);
		padding: 4px 6px;
		margin: 1px 8px;
        gap: 5px;
	}

	.channel:hover,
	.channel.selected {
		background-color: var(--channel-bg-hover);
		color: #dbdee1;
	}

	a {
		color: var(--channel-text-read);
        text-decoration: none;
	}
	.thread-name {
		color: var(--channel-text-read);
		white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
	width: 200%;
	}

	.channel:hover .thread-name {
		color: #dbdee1;
	}

	.thread-name.selected {
		color: var(--channel-text-unread) !important;
	}

	.channel-icon {
		width: 24px;
		margin-right: 5px;
	}
</style>
