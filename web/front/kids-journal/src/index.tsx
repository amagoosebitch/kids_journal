import App from "./components/app/App";
import React from "react";
import ReactDOM from "react-dom/client";
import "./style/index.css";
import reportWebVitals from "./reportWebVitals";
import { ChakraProvider } from "@chakra-ui/react";
import { Provider } from "react-redux";
import { store } from "./store";
import ErrorMessage from "./components/error/ErrorMessage";
import { ApiProvider } from "@reduxjs/toolkit/dist/query/react";
import {fetchGroupsAction} from "./store/api-actions";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement,
);

root.render(
  <Provider store={store}>
      <ChakraProvider>
        <ErrorMessage />
        <App />
      </ChakraProvider>
  </Provider>,
);

reportWebVitals();
