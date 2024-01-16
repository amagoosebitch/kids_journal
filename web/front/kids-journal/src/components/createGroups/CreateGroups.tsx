import "./CreateGroups.css";
import React, { useState } from "react";
import {Button, CloseButton, Grid, GridItem, Input, Select} from "@chakra-ui/react";
import { ButtonMain } from "../button/ButtonMain";
import { InputPhone } from "../input-phone/InputPhone";

const options = [
  { label: "Садик №1", value: 1 },
  { label: "Садик Вишенка", value: 2 },
];

const optionsAge = [
  { age: "0-3", value: 1 },
  { age: "3-6", value: 2 },
  { age: "6-9", value: 3 },
];

export const CreateGroups = () => {
  const [value, setValue] = useState("");
  const [valueAge, setValueAge] = useState("");
  const [valueName, setNameInput] = useState("");

  const childTemplate = {
    firstNameChild: "",
    surnameChild: "",
    dataChild: "",
    firstNameParent: "",
    surnameParent: "",
    telParent: "",
  };

  const [children, setChildren] = useState([childTemplate]);
  const addChild = () => {
    setChildren([...children, childTemplate]);
  };

  const onChangeChild = (e: any, index: number) => {
    const updatedChildren = children.map((child, i) =>
      index == i
        ? Object.assign(child, { [e.target.name]: e.target.value })
        : child,
    );
    setChildren(updatedChildren);
  };

  const removeChild = (index: number) => {
    const filteredChildren = [...children];
    filteredChildren.splice(index, 1);
    setChildren(filteredChildren);
  };

  const createGroup = () => {
    const result = {
      organization_id: value,
      age: valueAge,
      groupName: valueName,
      listChildren: children,
    };
    console.log(result);
  };

  return (
    <form className="create-group-main__container">
      <div className="create-group__text">Создание новой группы</div>
      <div className="create-group__form">
        <div className="create-group">
          <div className="create-group__form-items">
            <Select
              placeholder="Выберете организацию"
              onChange={(event: React.FormEvent<HTMLSelectElement>) =>
                setValue(event.currentTarget.value)
              }
              style={{
                background: "white",
              }}
            >
              {options.map((option) => (
                <option value={option.value}>{option.label}</option>
              ))}
            </Select>
          </div>
          <div className="create-group__form-items">
            <Select
              placeholder="Выберете возраст детей"
              onChange={(event: React.FormEvent<HTMLSelectElement>) =>
                setValueAge(event.currentTarget.value)
              }
              style={{
                background: "white",
              }}
            >
              {optionsAge.map((option) => (
                <option value={option.value}>{option.age}</option>
              ))}
            </Select>
          </div>
          <div className="create-group__form-items">
            <Input
              type="text"
              placeholder="Введите название группы"
              onChange={(event: React.FormEvent<HTMLInputElement>) =>
                setNameInput(event.currentTarget.value)
              }
              style={{
                background: "white",
              }}
            />
          </div>
          <div className="create-group__form-button">
            <ButtonMain
              className="create-group__button"
              height="44px"
              width="211px"
              linkButton={""}
              onClick={() => createGroup()}
            >
              Создать группу
            </ButtonMain>
          </div>
        </div>
      </div>
    </form>
  );
};
