<template>
	<div
		v-if="user_type === 'system user'"
		class="sm:h-screen w-full flex flex-col items-center justify-center p-4"
	>
		<img :src="GreetingDesktopImg" class="hidden sm:block w-full rounded-2xl" />

		<img :src="GreetingMobileImg" class="block sm:hidden w-full rounded-2xl" />
	</div>
	<div
		v-if="String(crew_rank).toLowerCase() !== 'master'"
		class="p-6 space-y-6 bg-gray-50"
	>
		<!-- HEADER -->
		<div class="flex items-center justify-between">
			<h2 class="text-2xl font-semibold text-gray-800">
				My Training Dashboard
			</h2>

			<span
				class="px-4 py-2 text-sm font-semibold text-white bg-red-500 rounded-lg"
			>
				{{ summary.data.overdue }} Courses Overdue!
			</span>
		</div>

		<!-- STATS -->
		<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
			<!-- Mandatory Progress -->
			<div class="bg-white rounded-xl shadow p-4">
				<p class="text-sm text-gray-500">Mandatory Progress</p>
				<p class="text-3xl font-bold mt-2">
					{{ summary.data?.percentage ?? 0 }}%
				</p>

				<div class="w-full bg-gray-200 rounded-full h-2 mt-3">
					<div
						class="bg-green-500 h-2 rounded-full"
						:style="{ width: `${summary.data?.percentage || 0}%` }"
					></div>
				</div>
			</div>

			<!-- Overdue -->
			<div class="bg-white rounded-xl shadow p-4 border-l-4 border-red-500">
				<p class="text-sm text-gray-500">Overdue Courses</p>
				<p class="text-3xl font-bold mt-2">{{ summary.data.overdue }}</p>
			</div>

			<!-- In Progress -->
			<div class="bg-white rounded-xl shadow p-4 border-l-4 border-orange-400">
				<p class="text-sm text-gray-500">In Progress</p>
				<p class="text-3xl font-bold mt-2">{{ summary.data.in_progress }}</p>
			</div>

			<!-- Completed -->
			<div class="bg-white rounded-xl shadow p-4 border-l-4 border-green-500">
				<p class="text-sm text-gray-500">Completed</p>
				<p class="text-3xl font-bold mt-2">{{ summary.data.completed }}</p>
			</div>
		</div>

		<!-- CONTENT -->
		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
			<!-- Mandatory Training -->
			<div class="bg-white rounded-xl shadow p-5 lg:col-span-2">
				<h3 class="font-semibold text-lg mb-4">Mandatory Training</h3>

				<ul class="space-y-4">
					<li
						v-for="program in mandatory.data"
						:key="program.name"
						class="flex items-center justify-between"
					>
						<div class="flex items-center gap-3">
							<span
								:class="[
									'w-3 h-3 rounded-full',
									program.is_completed
										? 'bg-blue-500'
										: program.is_overdue
											? 'bg-red-500'
											: program.is_enrolled
												? 'bg-yellow-500'
												: 'bg-yellow-500',
								]"
							></span>
							<div>
								<span class="font-medium">{{ program.title }}</span>
								<p class="text-xs text-gray-500">
									Due: {{ formatDate(program.due_date) }}
								</p>
							</div>
						</div>

						<div v-if="!program.is_enrolled" class="flex items-center gap-2">
							<span
								v-if="program.is_overdue"
								class="px-3 py-1 text-xs font-semibold text-white bg-red-500 rounded"
							>
								Overdue
							</span>
							<button
								v-if="!program.is_completed"
								class="px-3 py-1 text-sm text-white bg-blue-500 rounded"
								@click="handleStart(program)"
							>
								Start
							</button>
						</div>
						<div v-if="program.is_enrolled" class="flex items-center gap-2">
							<span
								v-if="program.is_overdue"
								class="px-3 py-1 text-xs font-semibold text-white bg-red-500 rounded"
							>
								Overdue
							</span>
							<button
								v-if="program.is_completed"
								class="px-3 py-1 text-sm border border-blue-500 text-blue-500 rounded"
								@click="handleResume(program)"
							>
								View
							</button>
							<button
								v-if="!program.is_completed"
								class="px-3 py-1 text-sm text-white bg-blue-500 rounded"
								@click="handleResume(program)"
							>
								Resume
							</button>
						</div>
					</li>
				</ul>
			</div>

			<!-- Non Mandatory -->
			<div class="bg-white rounded-xl shadow p-5">
				<h3 class="font-semibold text-lg mb-4">Non-Mandatory Training</h3>

				<ul class="space-y-4">
					<li
						v-for="program in nonMandatory.data"
						:key="program.name"
						class="flex justify-between items-center"
					>
						{{ program.title }}
						<button
							class="px-3 py-1 text-sm border border-blue-500 text-blue-500 rounded"
							@click="handleEnroll(program)"
						>
							Enroll
						</button>
					</li>
				</ul>

				<div v-if="nonMandatory.data.length > 0" class="mt-6 text-center">
					<a
						href="/lms/programs"
						class="px-4 py-2 text-sm border rounded text-gray-700"
					>
						Browse Full Library
					</a>
				</div>
				<div v-else class="mt-20 text-center text-gray-500">
					No courses available.
				</div>
			</div>
		</div>

		<!-- RECENT ACTIVITY -->
		<div class="bg-white rounded-xl shadow p-5">
			<h3 class="font-semibold text-lg mb-4">Recent Activity</h3>

			<ul v-if="recentActivities.length" class="space-y-2 text-sm">
				<li
					v-for="(activity, index) in recentActivities"
					:key="index"
					:class="activity.color"
				>
					{{ activity.icon }} {{ activity.label }}
				</li>
			</ul>

			<div v-else class="text-gray-500 text-sm">No recent activity.</div>
		</div>
	</div>

	<div
		v-if="String(crew_rank).toLowerCase() === 'master'"
		class="p-6 space-y-6 bg-gray-50"
	>
		<!-- Header -->
		<div class="flex justify-between items-center p-6">
			<h1 class="text-2xl font-bold text-gray-800">
				Vessel Training Compliance - Pacific Explorer
			</h1>
			<button
				class="bg-blue-600 text-white px-5 py-2 rounded-lg shadow hover:bg-blue-700"
			>
				Generate Report
			</button>
		</div>

		<!-- KPI Cards -->
		<div class="grid grid-cols-1 md:grid-cols-4 gap-4 px-6">
			<div class="bg-white rounded-xl p-6 border-l-4 border-blue-500 shadow">
				<p class="text-gray-500 text-sm">Overall Compliance</p>
				<p class="text-3xl font-bold mt-2">78%</p>
			</div>

			<div class="bg-white rounded-xl p-6 border-l-4 border-red-500 shadow">
				<p class="text-gray-500 text-sm">Courses At Risk</p>
				<p class="text-3xl font-bold mt-2">5</p>
			</div>

			<div class="bg-white rounded-xl p-6 border-l-4 border-yellow-500 shadow">
				<p class="text-gray-500 text-sm">Crew with Overdue Training</p>
				<p class="text-3xl font-bold mt-2">3</p>
			</div>

			<div class="bg-white rounded-xl p-6 border-l-4 border-blue-400 shadow">
				<p class="text-gray-500 text-sm">Pending Non-Mandatory</p>
				<p class="text-3xl font-bold mt-2">15</p>
			</div>
		</div>

		<!-- Middle Section -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
			<!-- Compliance by Course -->
			<div class="bg-white rounded-xl shadow p-6">
				<h2 class="text-lg font-semibold mb-4">Compliance by Course</h2>

				<div class="space-y-3">
					<div class="flex justify-between border-b pb-2">
						<span>Course A: Safety Procedures</span>
						<span class="font-semibold">100%</span>
					</div>
					<div class="flex justify-between border-b pb-2">
						<span>Course B: Emergency Response</span>
						<span class="font-semibold">95%</span>
					</div>
					<div class="flex justify-between border-b pb-2 text-red-600">
						<span>Course C: Environmental Regulations</span>
						<span class="font-semibold">45%</span>
					</div>
					<div class="flex justify-between">
						<span>Course D: Navigation Safety</span>
						<span class="font-semibold">88%</span>
					</div>
				</div>
			</div>

			<!-- Reminder Escalation Status -->
			<div class="bg-white rounded-xl shadow p-6">
				<h2 class="text-lg font-semibold mb-4">Reminder Escalation Status</h2>

				<div class="space-y-4">
					<div class="border-b pb-3">
						<span class="bg-red-100 text-red-600 text-xs px-2 py-1 rounded"
							>Stage 3</span
						>
						<p class="font-medium mt-1">Fire Safety - Mike Jones</p>
						<p class="text-sm text-gray-500">Manager Alert Sent (SMS)</p>
					</div>

					<div class="border-b pb-3">
						<span
							class="bg-yellow-100 text-yellow-600 text-xs px-2 py-1 rounded"
							>Stage 2</span
						>
						<p class="font-medium mt-1">Environmental Regs - Jane Smith</p>
						<p class="text-sm text-gray-500">Formal Reminder Sent</p>
					</div>

					<div>
						<span class="bg-blue-100 text-blue-600 text-xs px-2 py-1 rounded"
							>Stage 1</span
						>
						<p class="font-medium mt-1">Security Training - 5 crew members</p>
						<p class="text-sm text-gray-500">Initial Notification Sent</p>
					</div>
				</div>
			</div>
		</div>

		<!-- Crew Training Status Table -->
		<div class="px-6 pb-8">
			<div class="bg-white rounded-xl shadow p-6">
				<h2 class="text-lg font-semibold mb-4">Crew Training Status</h2>

				<table class="w-full border-collapse">
					<thead>
						<tr class="bg-gray-100 text-left">
							<th class="p-3 text-sm">Name</th>
							<th class="p-3 text-sm">Mandatory %</th>
							<th class="p-3 text-sm">Status</th>
							<th class="p-3 text-sm">Alerts</th>
							<th class="p-3 text-sm">Action</th>
						</tr>
					</thead>
					<tbody>
						<tr class="border-t">
							<td class="p-3">John Doe</td>
							<td class="p-3">100%</td>
							<td class="p-3 text-green-600">Compliant</td>
							<td class="p-3">None</td>
							<td class="p-3">
								<button
									class="border border-blue-500 text-blue-500 px-3 py-1 rounded"
								>
									View
								</button>
							</td>
						</tr>

						<tr class="border-t">
							<td class="p-3">Jane Smith</td>
							<td class="p-3">45%</td>
							<td class="p-3 text-red-600">At Risk</td>
							<td class="p-3">2 Overdue</td>
							<td class="p-3">
								<button class="bg-red-500 text-white px-3 py-1 rounded">
									Send Reminder
								</button>
							</td>
						</tr>

						<tr class="border-t">
							<td class="p-3">Mike Jones</td>
							<td class="p-3">60%</td>
							<td class="p-3 text-red-600">Non-Compliant</td>
							<td class="p-3">1 Overdue</td>
							<td class="p-3">
								<button class="bg-red-500 text-white px-3 py-1 rounded">
									Send Reminder
								</button>
							</td>
						</tr>

						<tr class="border-t">
							<td class="p-3">Anna Kyle</td>
							<td class="p-3">95%</td>
							<td class="p-3 text-green-600">Compliant</td>
							<td class="p-3">Due Soon (1)</td>
							<td class="p-3">
								<button
									class="border border-blue-500 text-blue-500 px-3 py-1 rounded"
								>
									View
								</button>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	</div>
</template>

<script setup>
import GreetingDesktopImg from '@/assets/greeting_desktop.png'
import GreetingMobileImg from '@/assets/greeting_mobile.png'
import { computed } from 'vue'
import { createResource, call, toast } from 'frappe-ui'
import { usersStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const { userResource } = usersStore()

const router = useRouter()

const getRelativeDayLabel = (dateStr) => {
	if (!dateStr) return ''

	const date = new Date(dateStr)
	const today = new Date()

	const diffDays = Math.floor((today - date) / (1000 * 60 * 60 * 24))

	if (diffDays === 0) return 'Today'
	if (diffDays === 1) return 'Yesterday'
	if (diffDays <= 7) return 'Last Week'
	return date.toLocaleDateString()
}

const recentActivities = computed(() => {
	if (!activityLog.data) return []

	const activities = []

	activityLog.data.forEach((item) => {
		// ✅ Completed
		if (item.completed_at) {
			activities.push({
				type: 'completed',
				color: 'text-green-600',
				icon: '✔',
				label: `${getRelativeDayLabel(item.completed_at)}: Completed "${item.course_title}"`,
				date: item.completed_at,
			})
			return
		}

		// ▶ Started
		if (item.started_at) {
			activities.push({
				type: 'started',
				color: 'text-blue-500',
				icon: '▶',
				label: `${getRelativeDayLabel(item.started_at)}: Started "${item.course_title}"`,
				date: item.started_at,
			})
		}
	})

	// sort by latest activity
	return activities
		.sort((a, b) => new Date(b.date) - new Date(a.date))
		.slice(0, 5) // tampilkan max 5 activity
})

const formatDate = (dateStr) => {
	if (!dateStr) return '-'

	const date = new Date(dateStr)
	const day = String(date.getDate()).padStart(2, '0')
	const month = String(date.getMonth() + 1).padStart(2, '0')
	const year = date.getFullYear()

	return `${day}-${month}-${year}`
}

const crew_rank = computed(() => {
	return userResource.data?.crew_rank || 'Guest'
})

const user_type = computed(() => {
	return String(userResource.data?.user_type || 'Guest').toLowerCase()
})

const handleEnroll = (program) => {
	enrollMember(program.program, program.course)
}

const handleStart = (program) => {
	enrollMember(program.program, program.course)
}

const handleResume = (program) => {
	enrollMember(program.program, program.course)
}

const enrollMember = (program, course) => {
	call('lms.lms.utils.enroll_in_program_course', {
		program: program,
		course: course,
	})
		.then((data) => {
			if (data.current_lesson) {
				router.push({
					name: 'Lesson',
					params: {
						courseName: course,
						chapterNumber: data.current_lesson.split('-')[0],
						lessonNumber: data.current_lesson.split('-')[1],
					},
				})
			} else if (data) {
				router.push({
					name: 'Lesson',
					params: {
						courseName: course,
						chapterNumber: 1,
						lessonNumber: 1,
					},
				})
			}
		})
		.catch((err) => {
			toast.error(err.messages?.[0] || err)
		})
}

const nonMandatory = createResource({
	url: 'lms.lms.utils.get_non_mandatory_courses_by_user',
	auto: true,
	makeParams() {
		return {
			crew_rank: crew_rank.value,
		}
	},
	onSuccess(data) {
		console.log('Non Mandatory Data:', data)
	},
})

const mandatory = createResource({
	url: 'lms.lms.utils.get_mandatory_program_courses_by_user',
	auto: true,
	makeParams() {
		return {
			crew_rank: crew_rank.value,
		}
	},
	onSuccess(data) {
		console.log('Mandatory Data:', data)
	},
})

const summary = createResource({
	url: 'lms.lms.utils.get_course_summary_by_crew_rank',
	auto: true,
	makeParams() {
		return {
			crew_rank: crew_rank.value,
		}
	},
	onSuccess(data) {
		console.log('Summary Data:', data)
	},
})

const activityLog = createResource({
	url: 'lms.lms.utils.get_all_user_courses_enrollment',
	auto: true,
	onSuccess(data) {
		console.log('Activity Log Data:', data)
	},
})
</script>
