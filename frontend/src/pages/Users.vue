<template>
	<header
		class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
	>
		<Breadcrumbs :items="breadcrumbs" />
		<Button v-if="!readOnlyMode" variant="solid" @click="showForm = true">
			<template #prefix>
				<Plus class="w-4 h-4" />
			</template>
			{{ __('Create') }}
		</Button>
	</header>
	<div class="py-5 mx-5">
		<div class="flex items-center justify-between mb-4">
			<div class="text-lg font-semibold text-ink-gray-7">
				{{
					users.data?.length
						? __('{0} Users').format(users.data.length)
						: __('No Users')
				}}
			</div>
			<FormControl v-model="search" type="text" placeholder="Search">
				<template #prefix>
					<FeatherIcon name="search" class="size-4 text-ink-gray-5" />
				</template>
			</FormControl>
		</div>
		<ListView
			v-if="users.data?.length"
			:columns="userColumns"
			:rows="users.data"
			row-key="full_name"
			:options="{
				showTooltip: false,
				selectable: false,
				onRowClick: (row) => {
					if (readOnlyMode) return
					assignmentID = row.name
					showAssignmentForm = true
				},
			}"
		>
		</ListView>
		<EmptyState v-else type="Users" />
		<div v-if="users.hasNextPage" class="flex justify-center my-5">
			<Button @click="users.next()">
				{{ __('Load More') }}
			</Button>
		</div>
	</div>
	<Dialog
		v-model="showForm"
		:options="{
			title: __('Create a Quiz'),
			size: 'sm',
			actions: [
				{
					label: __('Save'),
					variant: 'solid',
					onClick({ close }) {
						insertQuiz(close)
					},
				},
			],
		}"
	>
		<template #body-content>
			<FormControl v-model="title" :label="__('Title')" type="text" />
		</template>
	</Dialog>
</template>
<script setup>
import {
	Breadcrumbs,
	Button,
	createListResource,
	Dialog,
	FeatherIcon,
	FormControl,
	ListView,
	toast,
	usePageMeta,
} from 'frappe-ui'
import { useRouter } from 'vue-router'
import { computed, inject, onMounted, ref, watch } from 'vue'
import { Plus } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import EmptyState from '@/components/EmptyState.vue'

const { brand } = sessionStore()
const user = inject('$user')
const dayjs = inject('$dayjs')
const router = useRouter()
const search = ref('')
const readOnlyMode = window.read_only_mode
const userFilters = ref({})
const showForm = ref(false)
const title = ref('')

onMounted(() => {
	if (!user.data?.is_moderator && !user.data?.is_instructor) {
		router.push({ name: 'Courses' })
	} else if (!user.data?.is_moderator) {
		userFilters.value['owner'] = user.data?.name
	}
})

watch(search, () => {
	userFilters.value['full_name'] = ['like', `%${search.value}%`]
	users.update({
		filters: userFilters.value,
	})
	users.reload()
})

const users = createListResource({
	doctype: 'User',
	filters: userFilters,
	fields: ['full_name', 'email', 'crew_rank', 'vessel'],
	auto: true,
	cache: ['user', user.data?.name],
	orderBy: 'crew_rank desc',
})

const userColumns = computed(() => {
	return [
		{
			label: __('Full Name'),
			key: 'full_name',
			width: 2,
		},
		{
			label: __('Email'),
			key: 'email',
			width: 1,
		},
		{
			label: __('Rank'),
			key: 'crew_rank',
			width: 1,
		},
		{
			label: __('Vessel'),
			key: 'vessel',
			width: 1,
		},
	]
})

const breadcrumbs = computed(() => {
	return [
		{
			label: __('User Management'),
			route: {
				name: 'Users',
			},
		},
	]
})

usePageMeta(() => {
	return {
		title: __('User Management'),
		icon: brand.favicon,
	}
})
</script>
