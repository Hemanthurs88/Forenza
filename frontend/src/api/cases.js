import client from './client'

const API_URL = '/api/cases'

export const listCases = async () => {
  const response = await client.get(API_URL)
  return response.data
}

export const createCase = async (caseData) => {
  const response = await client.post(API_URL, caseData)
  return response.data
}

export const getCase = async (caseId) => {
  const response = await client.get(`${API_URL}/${caseId}`)
  return response.data
}
