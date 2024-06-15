import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { AppDispatch, State } from "../types/state";
import { AxiosInstance } from "axios";
import { groups } from "../types/group";
import { testOrganization, TIMEOUT_SHOW_ERROR } from "../const";
import { loadGroups, setDataLoadingStatus, setError } from "./action";
import { store } from "./index";

export const clearErrorAction = createAsyncThunk("setError", () => {
  setTimeout(() => store.dispatch(setError(null)), TIMEOUT_SHOW_ERROR);
});

export const fetchGroupsAction = createAsyncThunk<
  void,
  undefined,
  {
    dispatch: AppDispatch;
    state: State;
    extra: AxiosInstance;
  }
>("data/fetchGroups", async (_arg, { dispatch, extra: api }) => {
  dispatch(setDataLoadingStatus(true));
  const { data } = await api.get<groups>(
    `/organizations/${testOrganization}/groups`,
  );
  dispatch(setDataLoadingStatus(true));
  dispatch(loadGroups(data));
});

export const fetch1 = createAsyncThunk("fetchTodo", async () => {
  const data = await fetch(
    `https://d5de0lctsr23htkj7hlj.apigw.yandexcloud.net/organizations/${testOrganization}/groups`,
  );
  return data.json();
});
