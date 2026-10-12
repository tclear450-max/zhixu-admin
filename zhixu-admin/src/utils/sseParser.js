// Preserve SSE frame state across arbitrary network chunk boundaries.
export function createSseParser (onEvent) {
  let pending = ''
  let event = ''
  let data = []
  function line (value) {
    if (value.endsWith('\r')) value = value.slice(0, -1)
    if (value === '') {
      if (data.length) onEvent(event || 'message', data.join('\n'))
      event = ''
      data = []
    } else if (!value.startsWith(':')) {
      const colon = value.indexOf(':')
      const field = colon < 0 ? value : value.slice(0, colon)
      let payload = colon < 0 ? '' : value.slice(colon + 1)
      if (payload.startsWith(' ')) payload = payload.slice(1)
      if (field === 'event') event = payload
      if (field === 'data') data.push(payload)
    }
  }
  return (chunk, finish = false) => {
    pending += chunk
    let index
    while ((index = pending.indexOf('\n')) >= 0) {
      line(pending.slice(0, index))
      pending = pending.slice(index + 1)
    }
    if (finish && pending) { line(pending); pending = '' }
  }
}
