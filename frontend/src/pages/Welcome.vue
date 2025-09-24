<template>
	<div
		class="sm:h-screen w-full flex flex-col items-center justify-center px-2"
	>
		<!-- tampil di desktop -->
		<img :src="GreetingDesktopImg" class="hidden sm:block w-full rounded-2xl" />

		<!-- tampil di mobile -->
		<img :src="GreetingMobileImg" class="block sm:hidden w-full rounded-2xl" />
	</div>
</template>

<script setup>
import GreetingDesktopImg from '@/assets/greeting_desktop.png'
import GreetingMobileImg from '@/assets/greeting_mobile.png'
</script>
