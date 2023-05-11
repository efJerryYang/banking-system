<template>
    <div></div>
</template>
  
<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const router = useRouter()
const store = useStore()

onMounted(async () => {
    await store.dispatch('logout')
    router.push('/login')
})
</script>
  