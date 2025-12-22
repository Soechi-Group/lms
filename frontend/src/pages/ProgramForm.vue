<template>
	<header
		class="sticky top-0 z-10 flex flex-col md:flex-row md:items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
	>
		<Breadcrumbs :items="breadbrumbs" />
		<Button variant="solid" @click="saveProgram()">
			{{ __('Save') }}
		</Button>
	</header>
	<div v-if="program.doc" class="pt-5 px-5 w-3/4 mx-auto space-y-10">
		<FormControl v-model="program.doc.title" :label="__('Title')" />

		<!-- Courses -->
		<div>
			<div class="flex items-center justify-between mb-2">
				<div class="text-lg text-ink-gray-9 font-semibold">
					{{ __('Program Courses') }}
				</div>
				<Button
					@click="
						() => {
							currentForm = 'course'
							showDialog = true
						}
					"
				>
					<template #prefix>
						<Plus class="w-4 h-4" />
					</template>
					{{ __('Add') }}
				</Button>
			</div>

			<ListView
				:columns="courseColumns"
				:rows="program.doc.program_courses"
				row-key="name"
				:options="{
					showTooltip: false,
				}"
			>
				<ListHeader
					class="mb-2 grid items-center space-x-4 rounded bg-surface-gray-2 p-2"
				>
					<ListHeaderItem :item="item" v-for="item in courseColumns" />
				</ListHeader>
				<ListRows>
					<Draggable
						:list="program.doc.program_courses"
						item-key="name"
						group="items"
						@end="updateOrder"
						class="cursor-move"
					>
						<template #item="{ element: row }">
							<ListRow :row="row" />
						</template>
					</Draggable>
				</ListRows>
				<ListSelectBanner>
					<template #actions="{ unselectAll, selections }">
						<div class="flex gap-2">
							<Button
								variant="ghost"
								@click="remove(selections, unselectAll, 'program_courses')"
							>
								<Trash2 class="h-4 w-4 stroke-1.5" />
							</Button>
						</div>
					</template>
				</ListSelectBanner>
			</ListView>
		</div>

		<!-- Crew Rank -->
		<div>
			<div class="flex items-center justify-between mb-2">
				<div class="text-lg text-ink-gray-9 font-semibold">
					{{ __('Crew Ranks') }}
				</div>
				<Button
					@click="
						() => {
							currentForm = 'lms_crew_rank'
							showDialog = true
						}
					"
				>
					<template #prefix>
						<Plus class="w-4 h-4" />
					</template>
					{{ __('Add Crew Rank') }}
				</Button>
			</div>

			<ListView
				:columns="crewRankColumns"
				:rows="program.doc.crew_ranks"
				row-key="name"
				:options="{
					showTooltip: false,
				}"
			>
				<ListHeader
					class="mb-2 grid items-center space-x-4 rounded bg-surface-gray-2 p-2"
				>
					<ListHeaderItem :item="item" v-for="item in crewRankColumns" />
				</ListHeader>
				<ListRows>
					<ListRow :row="row" v-for="row in program.doc.crew_ranks" />
				</ListRows>
				<ListSelectBanner>
					<template #actions="{ unselectAll, selections }">
						<div class="flex gap-2">
							<Button
								variant="ghost"
								@click="remove(selections, unselectAll, 'crew_ranks')"
							>
								<Trash2 class="h-4 w-4 stroke-1.5" />
							</Button>
						</div>
					</template>
				</ListSelectBanner>
			</ListView>
		</div>

		<!-- Members -->
		<!-- <div>
			<div class="flex items-center justify-between mb-2">
				<div class="text-lg text-ink-gray-9 font-semibold">
					{{ __('Program Members') }}
				</div>
				<Button
					@click="
						() => {
							currentForm = 'member'
							showDialog = true
						}
					"
				>
					<template #prefix>
						<Plus class="w-4 h-4" />
					</template>
					{{ __('Add') }}
				</Button>
			</div>

			<ListView
				:columns="memberColumns"
				:rows="program.doc.program_members"
				row-key="name"
				:options="{
					showTooltip: false,
				}"
			>
				<ListHeader
					class="mb-2 grid items-center space-x-4 rounded bg-surface-gray-2 p-2"
				>
					<ListHeaderItem :item="item" v-for="item in memberColumns" />
				</ListHeader>
				<ListRows>
					<ListRow :row="row" v-for="row in program.doc.program_members" />
				</ListRows>
				<ListSelectBanner>
					<template #actions="{ unselectAll, selections }">
						<div class="flex gap-2">
							<Button
								variant="ghost"
								@click="remove(selections, unselectAll, 'program_members')"
							>
								<Trash2 class="h-4 w-4 stroke-1.5" />
							</Button>
						</div>
					</template>
				</ListSelectBanner>
			</ListView>
		</div> -->
	</div>

	<Dialog
		v-model="showDialog"
		:options="{
			title:
				currentForm == 'course'
					? __('New Program Course')
					: currentForm == 'lms_crew_rank'
						? __('New Crew Rank')
						: __('New Program Member'),
			actions: [
				{
					label: __('Add'),
					variant: 'solid',
					onClick: () =>
						currentForm == 'course'
							? addProgramCourse(close)
							: currentForm == 'lms_crew_rank'
								? addProgramCrewRank(close)
								: addProgramMember(close),
				},
			],
		}"
	>
		<template #body-content>
			<Link
				v-if="currentForm == 'course'"
				v-model="course"
				doctype="LMS Course"
				:filters="{
					disable_self_learning: 1,
				}"
				:label="__('Program Course')"
				:description="
					__(
						'Only courses for which self learning is disabled can be added to program.',
					)
				"
			/>

			<!-- <Link
				v-if="currentForm == 'member'"
				v-model="member"
				doctype="Crew Rank"
				:label="__('Crew Rank')"
				:onCreate="(value, close) => openSettings('Members', close)"
			/> -->

			<Link
				v-if="currentForm == 'lms_crew_rank'"
				v-model="crew_rank"
				doctype="Crew Rank"
				:label="__('Crew Rank')"
			>
				<template #item-label="{ option }">
					{{ option.label }}
				</template>
			</Link>
		</template>
	</Dialog>
</template>
<script setup>
import {
	Breadcrumbs,
	Button,
	call,
	createDocumentResource,
	Dialog,
	FormControl,
	ListView,
	ListRows,
	ListRow,
	ListHeader,
	ListHeaderItem,
	ListSelectBanner,
	usePageMeta,
	toast,
} from 'frappe-ui'
import { computed, ref, watch } from 'vue'
import { Plus, Trash2 } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { sessionStore } from '@/stores/session'
import { openSettings } from '@/utils'
import Draggable from 'vuedraggable'
import Link from '@/components/Controls/Link.vue'

const { brand } = sessionStore()
const showDialog = ref(false)
const currentForm = ref(null)
const course = ref(null)
const member = ref(null)
const crew_rank = ref(null)
const router = useRouter()

const props = defineProps({
	programName: {
		type: String,
		required: true,
	},
})

const rankCache = ref({})

const program = createDocumentResource({
	doctype: 'LMS Program',
	name: props.programName,
	auto: true,
	cache: ['program', props.programName],
})

watch(
	() => program.doc?.program_members,
	async (members) => {
		if (!members) return

		const missingRanks = [
			...new Set(
				members
					.filter((m) => m.crew_rank && !rankCache.value[m.crew_rank])
					.map((m) => m.crew_rank),
			),
		]

		if (missingRanks.length) {
			try {
				const res = await call('frappe.client.get_list', {
					doctype: 'Crew Rank',
					filters: [['name', 'in', missingRanks]],
					fields: ['name', 'rank_name'],
				})

				res.forEach((r) => {
					rankCache.value[r.name] = r.rank_name
				})
			} catch (err) {
				console.error('Failed to fetch ranks', err)
			}
		}

		members.forEach((m) => {
			if (m.crew_rank) {
				m.crew_rank_name = rankCache.value[m.crew_rank] || m.crew_rank
			}
		})
	},
	{ deep: true, immediate: true },
)

const addProgramCourse = () => {
	program.setValue.submit(
		{
			program_courses: [
				...program.doc.program_courses,
				{ course: course.value },
			],
		},
		{
			onSuccess(data) {
				showDialog.value = false
				course.value = null
				toast.success(__('Course added to program'))
				program.reload()
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		},
	)
}

const addProgramCrewRank = () => {
	if (!crew_rank.value) {
		toast.error(__('Please select a crew rank'))
		return
	}

	const alreadyAdded = (program.doc.crew_ranks || []).some(
		(r) => r.crew_rank === crew_rank.value || r.name === crew_rank.value,
	)

	if (alreadyAdded) {
		toast.error(__('Crew rank already added to program'))
		return
	}

	program.setValue.submit(
		{
			crew_ranks: [...program.doc.crew_ranks, { crew_rank: crew_rank.value }],
		},
		{
			onSuccess: async (data) => {
				const addedRank = crew_rank.value
				showDialog.value = false
				crew_rank.value = null
				toast.success(__('Crew rank added to program'))

				// fetch users for the added rank and add to program_members
				try {
					const member_list = await call('lms.lms.api.get_users_by_ranks', {
						rank: addedRank,
					})

					if (member_list && member_list.length) {
						const existing = new Set(
							(program.doc.program_members || []).map((m) => m.member),
						)

						const newMembers = member_list
							.filter((u) => !existing.has(u.name))
							.map((u) => ({
								member: u.name,
								crew_rank: u.crew_rank,
								full_name: u.full_name,
							}))

						if (newMembers.length) {
							program.setValue.submit(
								{
									program_members: [
										...(program.doc.program_members || []),
										...newMembers,
									],
								},
								{
									onSuccess() {
										toast.success(__('Members added to program'))
										program.reload()
									},
									onError(err) {
										toast.error(err.messages?.[0] || err)
									},
								},
							)
							return
						}
					}
					// fallback reload if no new members
					program.reload()
				} catch (err) {
					console.error('Failed to fetch members for rank', err)
					program.reload()
				}
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		},
	)
}

const addProgramMember = async () => {
	try {
		const member_list = await call('lms.lms.api.get_users_by_ranks', {
			rank: member.value,
		})

		if (!member_list.length) {
			toast.error(__('No users found for this rank'))
			return
		}

		const updatedMembers = [
			...program.doc.program_members,
			...member_list.map((u) => ({
				member: u.name,
				crew_rank: u.crew_rank,
				full_name: u.full_name,
			})),
		]

		program.setValue.submit(
			{
				program_members: updatedMembers,
			},
			{
				onSuccess(data) {
					showDialog.value = false
					member.value = null
					toast.success(__('Member(s) added to program'))
					program.reload()
				},
				onError(err) {
					toast.error(err.messages?.[0] || err)
				},
			},
		)
	} catch (err) {
		console.error(err)
		toast.error(__('Failed to fetch members'))
	}
}

const remove = (selections, unselectAll, doctype) => {
	selections = Array.from(selections)

	// If removing crew_ranks, also remove program_members belonging to those ranks
	if (doctype === 'crew_ranks') {
		const remainingCrewRanks = (program.doc.crew_ranks || []).filter(
			(row) => !selections.includes(row.name),
		)

		// Determine which rank identifiers were removed. Some rows may store rank id in `crew_rank` or use `name`.
		const removedRanks = (program.doc.crew_ranks || [])
			.filter((row) => selections.includes(row.name))
			.map((r) => r.crew_rank || r.name)

		const remainingMembers = (program.doc.program_members || []).filter(
			(m) => !removedRanks.includes(m.crew_rank),
		)

		program.setValue.submit(
			{
				crew_ranks: remainingCrewRanks,
				program_members: remainingMembers,
			},
			{
				onSuccess(data) {
					unselectAll()
					toast.success(__('Items removed successfully'))
					program.reload()
				},
				onError(err) {
					toast.error(err.messages?.[0] || err)
				},
			},
		)

		return
	}

	program.setValue.submit(
		{
			[doctype]: program.doc[doctype].filter(
				(row) => !selections.includes(row.name),
			),
		},
		{
			onSuccess(data) {
				unselectAll()
				toast.success(__('Items removed successfully'))
				program.reload()
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		},
	)
}

const updateOrder = (e) => {
	let sourceIdx = e.from.dataset.idx
	let targetIdx = e.to.dataset.idx
	let courses = program.doc.program_courses
	courses.splice(targetIdx, 0, courses.splice(sourceIdx, 1)[0])

	courses.forEach((course, index) => {
		course.idx = index + 1
	})

	program.setValue.submit(
		{
			program_courses: courses,
		},
		{
			onSuccess(data) {
				toast.success(__('Course moved successfully'))
				program.reload()
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		},
	)
}

const saveProgram = () => {
	call('frappe.model.rename_doc.update_document_title', {
		doctype: 'LMS Program',
		docname: program.doc.name,
		name: program.doc.title,
	})
		.then((data) => {
			toast.success(__('Program saved successfully'), 'message', 3000)
			router.push({ name: 'ProgramForm', params: { programName: data } })
		})
		.catch((err) => {
			toast.error(err.messages?.[0] || err)
		})
}

const courseColumns = computed(() => {
	return [
		{
			label: 'Title',
			key: 'course_title',
			width: 3,
		},
		{
			label: 'ID',
			key: 'course',
			width: 3,
		},
	]
})

const crewRankColumns = computed(() => {
	return [
		{
			label: 'Crew Rank',
			key: 'crew_name',
			width: 6,
			align: 'left',
		},
	]
})

const memberColumns = computed(() => {
	return [
		{
			label: 'Member',
			key: 'member',
			width: 3,
			align: 'left',
		},
		{
			label: 'Crew Rank',
			key: 'crew_rank_name',
			width: 3,
			align: 'left',
		},
		{
			label: 'Full Name',
			key: 'full_name',
			width: 3,
			align: 'left',
		},
		{
			label: 'Progress (%)',
			key: 'progress',
			width: 3,
			align: 'right',
		},
	]
})

const breadbrumbs = computed(() => {
	return [
		{
			label: 'Programs',
			route: { name: 'Programs' },
		},
		{
			label: props.programName === 'new' ? 'New Program' : props.programName,
		},
	]
})

usePageMeta(() => {
	return {
		title: program.doc?.title,
		icon: brand.favicon,
	}
})
</script>
