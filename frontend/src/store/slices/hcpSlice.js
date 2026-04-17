import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { searchHCPs } from '../../api/interactionApi'

export const fetchHCPs = createAsyncThunk(
  'hcp/search',
  async (query) => {
    const response = await searchHCPs(query)
    return response.data.results
  }
)

const hcpSlice = createSlice({
  name: 'hcp',
  initialState: {
    results: [],
    isLoading: false,
  },
  reducers: {
    clearResults: (state) => { state.results = [] },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchHCPs.pending, (s) => { s.isLoading = true })
      .addCase(fetchHCPs.fulfilled, (s, a) => {
        s.isLoading = false
        s.results = a.payload
      })
      .addCase(fetchHCPs.rejected, (s) => { s.isLoading = false })
  },
})

export const { clearResults } = hcpSlice.actions
export default hcpSlice.reducer
