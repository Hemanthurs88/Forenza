// src/api/cases.js
import client from './client'

export const listCases = async () => {
  const res = await client.get('/api/cases')
  return res.data
}

export const createCase = async (caseData) => {
  const res = await client.post('/api/cases', caseData)
  return res.data
}

export const getCaseHistory = async (caseId) => {
  const res = await client.get(`/api/cases/${caseId}/history`)
  return res.data
}
