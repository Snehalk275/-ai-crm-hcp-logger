import { createSlice } from "@reduxjs/toolkit";

const interactionSlice = createSlice({
  name: "interaction",
  initialState: {
    hcpName: "",
    interactionType: "",
    topics: "",
    sentiment: "",
    followUp: "",
  },
  reducers: {
    setInteraction: (state, action) => {
      return { ...state, ...action.payload };
    },
  },
});

export const { setInteraction } = interactionSlice.actions;
export default interactionSlice.reducer;