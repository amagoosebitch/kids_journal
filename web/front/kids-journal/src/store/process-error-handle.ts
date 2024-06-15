import { store } from "./index";
import { setError } from "./action";
import { clearErrorAction } from "./api-actions";

export const processErrorHandle = (message: string): void => {
  store.dispatch(setError(message));
  store.dispatch(clearErrorAction());
};
