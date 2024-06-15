import { configureStore } from "@reduxjs/toolkit";
import {createAPI} from "../services/api";
import groupsSlice from "../features/groupsSlice";

export const api = createAPI();

// export const store = configureStore({
//   reducer,
//   middleware: (getDefaultMiddleware) => getDefaultMiddleware({
//       thunk: {
//           extraArgument: api,
//       }
//   }),
// });

export const store = configureStore({
    reducer: {
        groups: groupsSlice,
    }
})
