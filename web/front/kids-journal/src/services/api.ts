import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from "axios";
import { processErrorHandle } from "../store/process-error-handle";
import { StatusCodes } from "http-status-codes";

const BACKEND_URL = "https://d5de0lctsr23htkj7hlj.apigw.yandexcloud.net";
const REQUEST_TIMEOUT = 5000;

const StatusCodesMapping: Record<number, boolean> = {
  [StatusCodes.BAD_REQUEST]: true,
  [StatusCodes.UNAUTHORIZED]: true,
  [StatusCodes.NOT_FOUND]: true,
};

const shouldDisplayError = (response: AxiosResponse) =>
  !!StatusCodesMapping[response.status];

export const createAPI = () => {
  const api = axios.create({
    baseURL: BACKEND_URL,
    timeout: REQUEST_TIMEOUT,
  });

  api.interceptors.response.use(
      (response) => response,
      (error: AxiosError<{ error: string }>) => {
        if (error.response && shouldDisplayError(error.response)) {
          processErrorHandle(error.response.data.error);
        }
      },
  );

  return api;
};
