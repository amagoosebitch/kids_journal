import "./CreateGroups.css";
import React, { ChangeEventHandler, useState } from "react";
import {
  Button,
  CloseButton,
  Grid,
  GridItem,
  Input,
  Select,
} from "@chakra-ui/react";
import { ButtonMain } from "../button/ButtonMain";
import {ApiRoute, AppRoute} from "../../const";

const optionsAge = [
  { age: "0-3", value: 1 },
  { age: "3-6", value: 2 },
  { age: "6-9", value: 3 },
];

type CreateGroupsProps = {
  organization: string | undefined;
};

export const CreateGroups = ({ organization }: CreateGroupsProps) => {
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
    const headers = new Headers();
    headers.append("Content-Type", "application/json");
    const body = JSON.stringify({
      organization_id: organization,
      age_range: optionsAge[Number(valueAge) - 1].age,
      name: valueName,
      group_id: valueName,
    });

    const requestOptions = {
      method: "POST",
      headers: headers,
      body: body,
    };

    fetch(ApiRoute + "/groups", requestOptions);
  };

  return (
    <form className="create-group-main__container">
      <div className="create-group__text">Общая информация</div>
      <div className="create-group__form">
        <div className="create-group">
          <div className="create-group__form-items">
            <div className="create-group__form-items_name">
              Выберите возраст детей
            </div>
            <div>
              <Select
                placeholder="Выберите возраст детей"
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
          </div>
          <div className="create-group__form-items">
            <div className="create-group__form-items_name">
              Введите название группы
            </div>
            <div>
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
          </div>
          <div className="create-group__form-items">
            <div className="create-group__form-items_name">
              Выберите преподавателя
            </div>
            <div>
              <Select
                placeholder="Выберите преподавателя"
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
          </div>
          <div className="create-group__form-button">
            <ButtonMain
              className="create-group__button"
              height="40px"
              width="160px"
              linkButton={`/${organization}/${valueName}${AppRoute.AddChild}`}
              onClick={() => createGroup()}
            >
              Продолжить
              <svg
                width="18"
                height="10"
                viewBox="0 0 18 10"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M12.7073 9L16.0002 5.70711C16.3907 5.31658 16.3907 4.68342 16.0002 4.29289L12.7073 1M15.7073 5L1.70728 5"
                  stroke="white"
                  stroke-width="1.5"
                  stroke-linecap="round"
                />
              </svg>
            </ButtonMain>
          </div>
        </div>
      </div>
    </form>
  );
};
