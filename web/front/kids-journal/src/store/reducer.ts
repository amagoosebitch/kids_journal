import {createReducer, createSlice} from "@reduxjs/toolkit";
import {
  addingGroup,
  fetchTodo,
  loadGroups,
  setDataLoadingStatus,
  setError,
} from "./action";
import { GROUPS, groups } from "../types/group";

type initialStateType = {
  groups: groups;
  isDataLoading: boolean;
  error: boolean | string | null;
};

const initialState: initialStateType = {
  groups: GROUPS,
  isDataLoading: false,
  error: false,
};

const reducer = createReducer(initialState, (builder) => {
  builder
    .addCase(loadGroups, (state, action) => {
      state.groups = action.payload;
    })
    .addCase(setDataLoadingStatus, (state, action) => {
      state.isDataLoading = action.payload;
    })
    .addCase(setError, (state, action) => {
      state.error = action.payload;
    })
});

export { reducer };
