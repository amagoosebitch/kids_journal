import { createAction } from "@reduxjs/toolkit";
import { groups } from "../types/group";
import {fetchGroupsAction} from "./api-actions";

export const addingGroup = createAction("group/addingGroup");

export const setError = createAction<string | null>("setError");

export const loadGroups = createAction<groups>('data/loadGroups');

export const fetchTodo = createAction<groups>('data/fetchTodo');

export const setDataLoadingStatus = createAction<boolean>("data/setDataLoadingStatus")
