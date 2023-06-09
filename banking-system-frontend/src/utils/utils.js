// utils.js
export function generateUUID() {
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
    (c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))).toString(16)
  )
}

export function generateClientId() {
  const uuid = generateUUID()
  const userAgent = navigator.userAgent
  return `${uuid}_${userAgent}`
}

export function loadClientId() {
  let clientId = localStorage.getItem('clientId')
  if (!clientId) {
    clientId = generateClientId()
    localStorage.setItem('clientId', clientId)
  }
  return clientId
}
