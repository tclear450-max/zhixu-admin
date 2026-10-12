import assert from 'node:assert/strict'
import fs from 'node:fs'
const source = fs.readFileSync(new URL('../zhixu-admin/src/utils/sseParser.js', import.meta.url), 'utf8')
const { createSseParser } = await import('data:text/javascript;base64,' + Buffer.from(source).toString('base64'))
const stream = 'event:token\r\ndata:知\r\n\r\nevent:token\ndata:  \n\nevent:token\ndata:\ndata:\n\nevent:citations\ndata:[{"documentName":"手册"}]\n\nevent:meta\ndata:{"conversationId":1}\n\n'
const expected = [['token', '知'], ['token', ' '], ['token', '\n'], ['citations', '[{"documentName":"手册"}]'], ['meta', '{"conversationId":1}']]
for (let boundary = 0; boundary <= stream.length; boundary++) {
  const result = []
  const parse = createSseParser((event, data) => result.push([event, data]))
  parse(stream.slice(0, boundary))
  parse(stream.slice(boundary), true)
  assert.deepEqual(result, expected, 'split at ' + boundary)
}
const result = []
const parse = createSseParser((event, data) => result.push([event, data]))
for (const ch of stream) parse(ch)
assert.deepEqual(result, expected)
console.log('PASS SSE parser at every character boundary, CRLF, whitespace, multiline data, citations and metadata')
