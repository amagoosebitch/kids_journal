import React from "react";
import { Input } from "@chakra-ui/react";

export const InputPhone = ({ ...props }) => {
  const RE_PHONE = /\D/g;

  const getInputNumbersValue = (value: string) => {
    return value.replace(RE_PHONE, "");
  };

  const handelPhoneInput = (event: React.ChangeEvent<HTMLInputElement>) => {
    const input = event.target;
    let inputNumbersValue = getInputNumbersValue(input.value);
    let formattedInputValue = "";
    const selectionStart = input.selectionStart;

    if (!inputNumbersValue) {
      return (input.value = "");
    }

    if (input.value.length !== selectionStart) {
      return;
    }

    if (["7", "8", "9"].indexOf(inputNumbersValue[0]) > -1) {
      if (inputNumbersValue[0] === "9") {
        inputNumbersValue = "7" + inputNumbersValue;
      }

      formattedInputValue = "+7";

      if (inputNumbersValue.length > 1) {
        formattedInputValue += " " + inputNumbersValue.substring(1, 4);
      }

      if (inputNumbersValue.length >= 5) {
        formattedInputValue += " " + inputNumbersValue.substring(4, 7);
      }

      if (inputNumbersValue.length >= 8) {
        formattedInputValue += "-" + inputNumbersValue.substring(7, 9);
      }

      if (inputNumbersValue.length >= 10) {
        formattedInputValue += "-" + inputNumbersValue.substring(9, 11);
      }
    } else {
      formattedInputValue = "+" + inputNumbersValue.substring(0, 16);
    }
    input.value = formattedInputValue;
  };
  return (
    <Input
      type="tel"
      maxLength={18}
      onInput={handelPhoneInput}
      placeholder="Введите номер телефона"
      onChange={props.onChange}
      style={{
        background: "white",
      }}
    />
  );
};
