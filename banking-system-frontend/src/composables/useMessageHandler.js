import { ref } from 'vue'

export default function useMessageHandler() {
  const message = ref('')
  const messageType = ref('')
  const showMessage = ref(false)

  function displayMessage(text, type = 'error') {
    message.value = text
    messageType.value = type
    showMessage.value = true
  }

  function clearMessage() {
    showMessage.value = false
  }

  return {
    message,
    messageType,
    showMessage,
    displayMessage,
    clearMessage
  }
}
