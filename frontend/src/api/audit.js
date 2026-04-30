// src/api/audit.js
import client from './client'

export const getGlobalAuditLog = async () => {
  const res = await client.get('/api/audit/global')
  return res.data
}
