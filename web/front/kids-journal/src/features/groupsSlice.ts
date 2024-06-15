import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { ApiRoute, testOrganization } from "../const";
import { AgeRanges, group, GROUPS } from "../types/group";

export const getAllData = createAsyncThunk(
  "groupsSlice",
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(
        `${ApiRoute}/organizations/${testOrganization}/groups`,
      );
      return response.json();
    } catch (error) {
      return rejectWithValue(error);
    }
  },
);

export const postAllData = createAsyncThunk(
  "postGroupSlice",
  async function (data, { rejectWithValue, dispatch }) {
    try {
      const response = await fetch(ApiRoute + "/groups", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      dispatch(postGroup({data}))

      return response.json();
    } catch (error) {
      return rejectWithValue(error);
    }
  },
);

export const groupsSlice = createSlice({
  name: "groupsSlice",
  initialState: {
    groups: GROUPS,
    loading: false,
    error: false,
    isSuccess: "",
  },
  reducers: {
    postGroup(state, action) {
      state.groups.push({
        group_id: action.payload.group_id,
        organization_id: action.payload.organization_id,
        name: action.payload.name,
        age_range: action.payload.age_range,
      });
    },
  },
  extraReducers: (builder) => {
    builder.addCase(getAllData.pending, (state) => {
      state.loading = true;
    });
    builder.addCase(getAllData.fulfilled, (state, action) => {
      state.loading = false;
      state.groups = action.payload;
    });
    builder.addCase(getAllData.rejected, (state, action) => {
      state.loading = false;
      state.error = true;
    });

    builder.addCase(postAllData.pending, (state) => {
      state.loading = true;
    });
    builder.addCase(postAllData.fulfilled, (state, action) => {
      state.loading = false;
      state.groups.push(action.payload);
    });
    builder.addCase(postAllData.rejected, (state, action) => {
      state.loading = false;
      state.error = true;
    });
  },
});

export const { postGroup } = groupsSlice.actions;
export default groupsSlice.reducer;
