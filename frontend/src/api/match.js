import client from './client'

export const matchFace = async (sessionId) => {
  const res = await client.get(`/api/match/${sessionId}`)
  return res.data
}
