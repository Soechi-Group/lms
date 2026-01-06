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
				2 Courses Overdue!
			</span>
		</div>

		<!-- STATS -->
		<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
			<!-- Mandatory Progress -->
			<div class="bg-white rounded-xl shadow p-4">
				<p class="text-sm text-gray-500">Mandatory Progress</p>
				<p class="text-3xl font-bold mt-2">65%</p>

				<div class="w-full bg-gray-200 rounded-full h-2 mt-3">
					<div class="bg-green-500 h-2 rounded-full" style="width: 65%"></div>
				</div>
			</div>

			<!-- Overdue -->
			<div class="bg-white rounded-xl shadow p-4 border-l-4 border-red-500">
				<p class="text-sm text-gray-500">Overdue Courses</p>
				<p class="text-3xl font-bold mt-2">2</p>
			</div>

			<!-- In Progress -->
			<div class="bg-white rounded-xl shadow p-4 border-l-4 border-orange-400">
				<p class="text-sm text-gray-500">In Progress</p>
				<p class="text-3xl font-bold mt-2">2</p>
			</div>

			<!-- Completed -->
			<div class="bg-white rounded-xl shadow p-4 border-l-4 border-green-500">
				<p class="text-sm text-gray-500">Completed</p>
				<p class="text-3xl font-bold mt-2">12</p>
			</div>
		</div>

		<!-- CONTENT -->
		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
			<!-- Mandatory Training -->
			<div class="bg-white rounded-xl shadow p-5 lg:col-span-2">
				<h3 class="font-semibold text-lg mb-4">Mandatory Training</h3>

				<ul class="space-y-4">
					<li
						v-for="program in programs.data"
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
				<!-- <ul class="space-y-4">
					<li class="flex items-center justify-between">
						<div class="flex items-center gap-3">
							<span class="w-3 h-3 rounded-full bg-red-500"></span>
							<span class="font-medium">Fire Safety Refresher</span>
						</div>

						<div class="flex items-center gap-2">
							<span
								class="px-3 py-1 text-xs font-semibold text-white bg-red-500 rounded"
							>
								Overdue
							</span>
							<button class="px-3 py-1 text-sm text-white bg-blue-500 rounded">
								Resume
							</button>
						</div>
					</li>

					<li class="flex items-center justify-between">
						<div class="flex items-center gap-3">
							<span class="w-3 h-3 rounded-full bg-red-500"></span>
							<span class="font-medium">New Environmental Regulations</span>
						</div>

						<div class="flex items-center gap-2">
							<span
								class="px-3 py-1 text-xs font-semibold text-white bg-red-500 rounded"
							>
								Overdue
							</span>
							<button class="px-3 py-1 text-sm text-white bg-blue-500 rounded">
								Start
							</button>
						</div>
					</li>

					<li class="flex items-center justify-between">
						<div class="flex items-center gap-3">
							<span class="w-3 h-3 rounded-full bg-orange-400"></span>
							<div>
								<p class="font-medium">Advanced First Aid</p>
								<p class="text-xs text-gray-500">Due: 30-Nov-2023</p>
							</div>
						</div>

						<button class="px-3 py-1 text-sm text-white bg-blue-500 rounded">
							Resume
						</button>
					</li>

					<li class="flex items-center justify-between">
						<div class="flex items-center gap-3">
							<span class="w-3 h-3 rounded-full bg-blue-500"></span>
							<div>
								<p class="font-medium">Vessel Security Training</p>
								<p class="text-xs text-gray-500">Due: 15-Dec-2023</p>
							</div>
						</div>

						<button
							class="px-3 py-1 text-sm border border-blue-500 text-blue-500 rounded"
						>
							View
						</button>
					</li>
				</ul> -->
			</div>

			<!-- Non Mandatory -->
			<div class="bg-white rounded-xl shadow p-5">
				<h3 class="font-semibold text-lg mb-4">Non-Mandatory Training</h3>

				<ul class="space-y-4">
					<li class="flex justify-between items-center">
						Leadership at Sea
						<button
							class="px-3 py-1 text-sm border border-blue-500 text-blue-500 rounded"
						>
							Enroll
						</button>
					</li>

					<li class="flex justify-between items-center">
						Efficient Cargo Handling
						<button
							class="px-3 py-1 text-sm border border-blue-500 text-blue-500 rounded"
						>
							Enroll
						</button>
					</li>

					<li class="flex justify-between items-center">
						Basic Engine Room Troubleshooting
						<button
							class="px-3 py-1 text-sm border border-blue-500 text-blue-500 rounded"
						>
							Enroll
						</button>
					</li>
				</ul>

				<div class="mt-6 text-center">
					<button class="px-4 py-2 text-sm border rounded text-gray-700">
						Browse Full Library
					</button>
				</div>
			</div>
		</div>

		<!-- RECENT ACTIVITY -->
		<div class="bg-white rounded-xl shadow p-5">
			<h3 class="font-semibold text-lg mb-4">Recent Activity</h3>

			<ul class="space-y-2 text-sm">
				<li class="text-green-600">
					✔ Today: Completed "Conflict Resolution"
				</li>
				<li class="text-orange-500">
					⚠ Yesterday: Reminder sent for "Fire Safety Refresher"
				</li>
				<li class="text-blue-500">
					▶ Last Week: Started "Advanced First Aid"
				</li>
			</ul>
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

const programs = createResource({
	url: 'lms.lms.utils.get_mandatory_program_courses_by_user',
	auto: true,
	makeParams() {
		return {
			crew_rank: crew_rank.value,
		}
	},
	onSuccess(data) {
		console.log('Crew Rank Data:', data)
	},
})
</script>
