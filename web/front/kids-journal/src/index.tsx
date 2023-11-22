import App from "./components/app/App";
import React from "react";
import ReactDOM from "react-dom/client";
import "./style/index.css";
import reportWebVitals from "./reportWebVitals";
import { ChakraProvider, Wrap, WrapItem } from "@chakra-ui/react";
import { Avatar, AvatarBadge, AvatarGroup } from "@chakra-ui/react";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement,
);

root.render(
  <ChakraProvider>
    <App />
  </ChakraProvider>,
);

reportWebVitals();
