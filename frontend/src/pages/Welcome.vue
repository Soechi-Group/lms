<template>
	<!-- <div
		v-if="user_type === 'system user'"
		class="sm:h-screen w-full flex flex-col items-center justify-center p-4"
	>
		<img :src="GreetingDesktopImg" class="hidden sm:block w-full rounded-2xl" />

		<img :src="GreetingMobileImg" class="block sm:hidden w-full rounded-2xl" />
	</div> -->

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
		v-if="
			String(crew_rank).toLowerCase() === 'master' &&
			user_type !== 'system user'
		"
		class="p-6 space-y-6 bg-gray-50"
	>
		<!-- Header -->
		<div class="flex justify-between items-center p-6">
			<h1 class="text-2xl font-bold text-gray-800">
				Vessel Training Compliance - {{ crew_vessel }}
			</h1>
		</div>

		<!-- KPI Cards -->
		<div class="grid grid-cols-1 md:grid-cols-4 gap-4 px-6">
			<div class="bg-white rounded-xl p-6 border-l-4 border-blue-500 shadow">
				<p class="text-gray-500 text-sm">Overall Compliance</p>
				<p class="text-3xl font-bold mt-2">{{ overallCompliance }}%</p>
			</div>

			<div class="bg-white rounded-xl p-6 border-l-4 border-red-500 shadow">
				<p class="text-gray-500 text-sm">Courses At Risk</p>
				<p class="text-3xl font-bold mt-2">{{ courseAtRisk }}</p>
			</div>

			<div class="bg-white rounded-xl p-6 border-l-4 border-yellow-500 shadow">
				<p class="text-gray-500 text-sm">Crew with Overdue Training</p>
				<p class="text-3xl font-bold mt-2">{{ totalOverdue }}</p>
			</div>

			<div class="bg-white rounded-xl p-6 border-l-4 border-blue-400 shadow">
				<p class="text-gray-500 text-sm">Pending Non-Mandatory</p>
				<p class="text-3xl font-bold mt-2">
					{{ pendingNonMandatory?.total_enrollments || 0 }}
				</p>
			</div>
		</div>

		<!-- Middle Section -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
			<!-- Compliance by Course -->
			<div class="bg-white rounded-xl shadow p-6">
				<h2 class="text-lg font-semibold mb-4">Compliance by Course</h2>

				<div class="space-y-3">
					<div
						v-for="course in complianceByCourse.data?.courses || []"
						:key="course.course"
						class="flex justify-between border-b pb-2"
					>
						<a :href="`/lms/courses/${course.course}`" target="__blank"
							><span>{{ course.course_title }}</span></a
						>
						<span
							:class="{
								'text-red-600': course.compliance_percentage < 50,
								'text-gray-800': course.compliance_percentage >= 50,
							}"
							class="font-semibold"
						>
							{{ course.compliance_percentage }}%
						</span>
					</div>

					<!-- Empty State -->
					<div
						v-if="!complianceByCourse.data?.courses?.length"
						class="text-gray-500 text-sm text-center py-6"
					>
						No compliance data available.
					</div>
				</div>
			</div>

			<!-- Reminder Escalation Status -->
			<div class="bg-white rounded-xl shadow p-6">
				<h2 class="text-lg font-semibold mb-4">Reminder Escalation Status</h2>

				<!-- <div class="space-y-4">
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
				</div> -->
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
						<tr
							v-if="
								!mandatoryProgramsByVessel.data?.crew_training_status?.length
							"
						>
							<td colspan="5" class="p-4 text-center text-gray-400">
								No training data available
							</td>
						</tr>
						<tr
							v-for="crew in mandatoryProgramsByVessel.data
								?.crew_training_status || []"
							:key="crew.crew_name"
							class="border-t"
						>
							<td class="p-3">{{ crew.crew_name }}</td>

							<td class="p-3">{{ crew.mandatory_percentage }}%</td>

							<td
								class="p-3 font-semibold"
								:class="{
									'text-green-600': crew.status === 'Compliant',
									'text-red-600': crew.status === 'At Risk',
									'text-yellow-600': crew.status === 'Non-Compliant',
								}"
							>
								{{ crew.status }}
							</td>

							<td class="p-3">{{ crew.alerts }}</td>

							<td class="p-3">
								<button
									v-if="crew.status === 'At Risk'"
									class="bg-red-500 text-white px-3 py-1 rounded"
								>
									Send Reminder
								</button>

								<button
									v-else
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

	<div v-if="is_dashboard_manager" class="p-6 space-y-6 bg-gray-50">
		<!-- HEADER -->
		<div class="flex justify-between items-center mb-6">
			<h1 class="text-2xl font-bold text-gray-800">
				Fleet Training Management
			</h1>

			<div class="flex gap-3">
				<select
					v-model="selectedVessel"
					class="border rounded-lg px-4 py-2 bg-white"
				>
					<option disabled value="">Select Vessel</option>
					<option
						v-for="vessel in getVesselList.data || []"
						:key="vessel.value"
						:value="vessel.value"
					>
						{{ vessel.label }}
					</option>
				</select>

				<button
					@click="handleGenerateReport"
					class="bg-blue-600 text-white px-5 py-2 rounded-lg shadow hover:bg-blue-700"
				>
					Generate Report
				</button>
			</div>
		</div>

		<!-- KPI CARDS -->
		<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
			<!-- Fleet Compliance -->
			<div class="bg-white rounded-xl p-6 border-l-4 border-blue-500 shadow">
				<p class="text-gray-500 text-sm">Fleet Compliance</p>
				<p class="text-3xl font-bold mt-2">
					{{ fleetManagementSummary.fleet_compliance }}%
				</p>
			</div>

			<!-- Vessels >95% -->
			<div class="bg-white rounded-xl p-6 border-l-4 border-green-500 shadow">
				<p class="text-gray-500 text-sm">Vessels &gt;95% Compliant</p>
				<p class="text-3xl font-bold mt-2">
					{{ fleetManagementSummary.vessels_above_95 }} / {{ vessels.length }}
				</p>
			</div>

			<!-- Total Overdue -->
			<div class="bg-white rounded-xl p-6 border-l-4 border-orange-400 shadow">
				<p class="text-gray-500 text-sm">Total Overdue</p>
				<p class="text-3xl font-bold mt-2">
					{{ fleetManagementSummary.total_overdue }}
				</p>
			</div>

			<!-- Avg Non Mandatory -->
			<div class="bg-white rounded-xl p-6 border-l-4 border-blue-400 shadow">
				<p class="text-gray-500 text-sm">Avg. Non-Mandatory / User</p>
				<p class="text-3xl font-bold mt-2">
					{{ fleetManagementSummary.avg_non_mandatory_per_user }}
				</p>
			</div>
		</div>

		<!-- MIDDLE SECTION -->
		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
			<!-- Top Non-Compliant Courses -->
			<div class="bg-white rounded-xl shadow p-6">
				<h2 class="text-lg font-semibold mb-4">Top Non-Compliant Courses</h2>

				<!-- Empty -->
				<div v-if="!topNonCompliantCourses.length" class="text-gray-400">
					No courses found
				</div>

				<!-- List -->
				<ul v-else class="space-y-4">
					<li
						v-for="course in topNonCompliantCourses"
						:key="course.course"
						class="flex justify-between items-center"
					>
						<a :href="`/lms/courses/${course.course}`" target="__blank">
							<span class="font-medium">
								{{ course.course_title }}
							</span>
						</a>

						<span
							class="font-semibold"
							:class="getComplianceColor(course.compliance_percentage)"
						>
							{{ course.compliance_percentage }}% Compliance
						</span>
					</li>
				</ul>
			</div>

			<!-- Vessel Comparison -->
			<div class="bg-white rounded-xl shadow p-6">
				<h2 class="text-lg font-semibold mb-4">Vessel Comparison</h2>

				<table class="w-full text-sm">
					<thead>
						<tr class="bg-gray-100 text-left">
							<th class="p-2">Vessel</th>
							<th class="p-2">Compliance</th>
							<th class="p-2">Status</th>
						</tr>
					</thead>

					<tbody>
						<tr v-for="vessel in vessels" :key="vessel.vessel" class="border-b">
							<td class="p-2">
								{{ vessel.vessel }}
							</td>

							<td class="p-2 font-semibold">
								{{ vessel.compliance_percentage }}%
							</td>

							<td
								class="p-2 font-semibold"
								:class="statusClass(vessel.compliance_percentage)"
							>
								{{ getStatus(vessel.compliance_percentage) }}
							</td>
						</tr>

						<tr v-if="!vessels.length">
							<td colspan="3" class="p-4 text-center text-gray-400">
								No data available
							</td>
						</tr>
					</tbody>
				</table>
			</div>

			<!-- Reminder Configuration -->
			<div class="bg-white rounded-xl shadow p-6">
				<h2 class="text-lg font-semibold mb-4">Reminder Configuration</h2>

				<!-- <ul class="space-y-4 text-sm">
					<li class="flex justify-between">
						<span class="bg-blue-100 text-blue-600 px-2 py-1 rounded"
							>Stage 1</span
						>
						<span>Due - 30 days</span>
						<span>In-App & Email</span>
					</li>
					<li class="flex justify-between">
						<span class="bg-yellow-100 text-yellow-600 px-2 py-1 rounded"
							>Stage 2</span
						>
						<span>Due - 14 days</span>
						<span>Formal Email</span>
					</li>
					<li class="flex justify-between">
						<span class="bg-red-100 text-red-600 px-2 py-1 rounded"
							>Stage 3</span
						>
						<span>Due - 7 days</span>
						<span>SMS + Master Alert</span>
					</li>
					<li class="flex justify-between">
						<span class="bg-red-500 text-white px-2 py-1 rounded">Stage 4</span>
						<span>Overdue</span>
						<span>Office Escalation</span>
					</li>
				</ul>

				<button
					class="mt-6 w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
				>
					Configure Workflow
				</button> -->
			</div>
		</div>

		<!-- RECENT ESCALATIONS -->
		<div class="bg-white rounded-xl shadow p-6">
			<div class="flex justify-between items-center mb-4">
				<h2 class="text-lg font-semibold">Recent Escalations</h2>
				<!-- <button
					class="text-blue-600 border border-blue-600 px-3 py-1 rounded text-sm"
				>
					View All
				</button> -->
			</div>

			<!-- <table class="w-full text-sm">
				<thead>
					<tr class="bg-gray-100 text-left">
						<th class="p-3">Crew Member</th>
						<th class="p-3">Course</th>
						<th class="p-3">Vessel</th>
						<th class="p-3">Escalation Stage</th>
						<th class="p-3">Due Date</th>
						<th class="p-3">Action</th>
					</tr>
				</thead>
				<tbody>
					<tr class="border-t">
						<td class="p-3">Mike Jones</td>
						<td class="p-3">Fire Safety</td>
						<td class="p-3">Pacific Explorer</td>
						<td class="p-3">
							<span class="bg-red-100 text-red-600 px-2 py-1 rounded text-xs"
								>Stage 3</span
							>
						</td>
						<td class="p-3 text-red-500">15-Oct-2023</td>
						<td class="p-3">
							<button
								class="border border-blue-500 text-blue-500 px-3 py-1 rounded"
							>
								Contact Master
							</button>
						</td>
					</tr>

					<tr class="border-t">
						<td class="p-3">Jane Smith</td>
						<td class="p-3">Environmental Regs</td>
						<td class="p-3">Atlantic Carrier</td>
						<td class="p-3">
							<span
								class="bg-yellow-100 text-yellow-600 px-2 py-1 rounded text-xs"
								>Stage 2</span
							>
						</td>
						<td class="p-3">20-Oct-2023</td>
						<td class="p-3">
							<button
								class="border border-blue-500 text-blue-500 px-3 py-1 rounded"
							>
								Monitor
							</button>
						</td>
					</tr>

					<tr class="border-t">
						<td class="p-3">Robert Brown</td>
						<td class="p-3">Security Training</td>
						<td class="p-3">Indian Voyager</td>
						<td class="p-3">
							<span class="bg-red-500 text-white px-2 py-1 rounded text-xs"
								>Stage 4</span
							>
						</td>
						<td class="p-3 text-red-500">10-Oct-2023</td>
						<td class="p-3">
							<button class="bg-red-500 text-white px-3 py-1 rounded">
								Escalate to HR
							</button>
						</td>
					</tr>
				</tbody>
			</table> -->
		</div>
	</div>
</template>

<script setup>
import GreetingDesktopImg from '@/assets/greeting_desktop.png'
import GreetingMobileImg from '@/assets/greeting_mobile.png'
import { computed, ref } from 'vue'
import { createResource, call, toast } from 'frappe-ui'
import { usersStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const { userResource } = usersStore()

const router = useRouter()
const selectedVessel = ref('')
const topNonCompliantCourses = ref([])

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

const crew_vessel = computed(() => {
	return userResource.data?.vessel || ''
})

const user_type = computed(() => {
	return String(userResource.data?.user_type || 'Guest').toLowerCase()
})

const is_dashboard_manager = computed(() => {
	return userResource.data?.is_dashboard_manager || false
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

const getPendingNonMandatorySummary = createResource({
	url: 'lms.lms.utils.get_pending_non_mandatory_summary',
	auto: true,
	makeParams() {
		return {
			crew_vessel: crew_vessel.value,
		}
	},
	onSuccess(data) {
		console.log('Pending Non Mandatory Summary Data:', data)
	},
})

const pendingNonMandatory = computed(() => {
	return getPendingNonMandatorySummary.data?.pending_non_mandatory || ''
})

const getStatus = (percentage) => {
	if (percentage >= 95) return 'Excellent'
	if (percentage >= 80) return 'Good'
	if (percentage >= 60) return 'Needs Attention'
	return 'Critical'
}

const statusClass = (percentage) => {
	if (percentage >= 95) return 'text-green-600'
	if (percentage >= 80) return 'text-green-500'
	if (percentage >= 60) return 'text-orange-500'
	return 'text-red-600'
}

const getComplianceColor = (percentage) => {
	if (percentage < 50) {
		return 'text-red-500'
	}
	if (percentage < 80) {
		return 'text-orange-500'
	}
	return 'text-green-600'
}

const getFleetManagementSummary = createResource({
	url: 'lms.lms.utils.get_fleet_management_summary',
	auto: true,
	onSuccess(data) {
		console.log('Fleet Management Summary Data:', data)
	},
})

const fleetManagementSummary = computed(() => {
	return getFleetManagementSummary.data
})

const getVesselComparison = createResource({
	url: 'lms.lms.utils.get_vessel_comparison',
	auto: true,
	onSuccess(data) {
		console.log('Vessel Comparison Data:', data)
	},
})

const vessels = computed(() => {
	return getVesselComparison.data?.vessels || []
})

const handleGenerateReport = async () => {
	if (!selectedVessel.value) {
		toast.warning('Please select vessel first')
		return
	}

	try {
		console.log('Calling API with vessel:', selectedVessel.value)

		const data = await call('lms.lms.utils.get_top_non_compliant_courses', {
			vessel: selectedVessel.value,
		})

		console.log('Top Non Compliant Courses Data:', data)

		topNonCompliantCourses.value = data
	} catch (err) {
		console.error(err)
		toast.error(err.message || err)
	}
}

const getVesselList = createResource({
	url: 'lms.lms.utils.get_vessel_dropdown',
	auto: true,
	onSuccess(data) {
		console.log('Vessel List Data:', data)
	},
})

const complianceByCourse = createResource({
	url: 'lms.lms.utils.get_compliance_by_course',
	auto: true,
	makeParams() {
		return {
			crew_vessel: crew_vessel.value,
		}
	},
	onSuccess(data) {
		console.log('Compliance By Course Data:', data)
	},
})

const mandatoryProgramsByVessel = createResource({
	url: 'lms.lms.utils.get_crew_training_status_table',
	auto: true,
	makeParams() {
		return {
			crew_vessel: crew_vessel.value,
		}
	},
	onSuccess(data) {
		console.log('Mandatory Programs By Vessel Data:', data)
	},
})

const vesselSummary = computed(() => {
	return (
		mandatoryProgramsByVessel.data?.summary || {
			total_crew: 0,
			compliant: 0,
			at_risk: 0,
			non_compliant: 0,
			overdue: 0,
		}
	)
})

const courseAtRisk = computed(() => {
	return vesselSummary.value.at_risk || 0
})

const totalOverdue = computed(() => {
	return vesselSummary.value.overdue || 0
})

const overallCompliance = computed(() => {
	if (!mandatoryProgramsByVessel.data?.crew_training_status?.length) return 0

	const total = mandatoryProgramsByVessel.data.crew_training_status.length
	const compliant = vesselSummary.value.compliant

	return Math.round((compliant / total) * 100)
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
