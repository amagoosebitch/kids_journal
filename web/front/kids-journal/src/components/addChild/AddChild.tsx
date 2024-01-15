import React, { useState } from "react";
import { Button, CloseButton, Grid, GridItem, Input } from "@chakra-ui/react";
import { ButtonMain } from "../button/ButtonMain";

const options = [
  { label: "Садик №1", value: 1 },
  { label: "Садик Вишенка", value: 2 },
];

const optionsAge = [
  { age: "0-3", value: 1 },
  { age: "3-6", value: 2 },
  { age: "6-9", value: 3 },
];

export const AddChild = () => {
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
    <>
      <div className="creat__text">Создание новой группы</div>
      <div className="creat__form">
        <div>
          <div>
            <select
              className="creat__form-select"
              placeholder="Выберете организацию"
              onChange={(event: React.FormEvent<HTMLSelectElement>) =>
                setValue(event.currentTarget.value)
              }
            >
              {options.map((option) => (
                <option value={option.value}>{option.label}</option>
              ))}
            </select>
          </div>
          <div>
            <select
              className="creat__form-select"
              placeholder="Выберете возраст детей"
              onChange={(event: React.FormEvent<HTMLSelectElement>) =>
                setValueAge(event.currentTarget.value)
              }
            >
              {optionsAge.map((option) => (
                <option value={option.value}>{option.age}</option>
              ))}
            </select>
          </div>
          <div>
            <input
              type="text"
              placeholder="Введите название группы"
              className="creat__form-select"
              onChange={(event: React.FormEvent<HTMLInputElement>) =>
                setNameInput(event.currentTarget.value)
              }
            />
          </div>
          <div>
            <ButtonMain
              className="creat__form-button"
              height="44px"
              width="211px"
              linkButton={""}
              onClick={() => createGroup()}
            >
              Создать группу
            </ButtonMain>
          </div>
        </div>

        <div className="add_children">
          <div className="childrenScroll">
            {children.map((child, index) => (
              <div className="add_children-item">
                <Grid
                  templateRows="repeat(2, 1fr)"
                  templateColumns="repeat(7, 1fr)"
                  gap={3}
                  key={index}
                >
                  <GridItem rowSpan={2} colSpan={1} className="Close-Button">
                    <CloseButton onClick={() => removeChild(index)} />
                  </GridItem>
                  <GridItem colSpan={2} w="100%" h="10">
                    <Input
                      placeholder="Имя ребенка"
                      size="md"
                      name="firstNameChild"
                      onChange={(e) => onChangeChild(e, index)}
                      value={child.firstNameChild}
                    />
                  </GridItem>
                  <GridItem colSpan={2} w="100%" h="10">
                    <Input
                      placeholder="Фамилия ребенка"
                      size="md"
                      name="surnameChild"
                      onChange={(e) => onChangeChild(e, index)}
                      value={child.surnameChild}
                    />
                  </GridItem>
                  <GridItem colSpan={2} w="100%" h="10">
                    <Input
                      placeholder="Select Date"
                      size="md"
                      type="date"
                      name="dataChild"
                      onChange={(e) => onChangeChild(e, index)}
                      value={child.dataChild}
                    />
                  </GridItem>
                  <GridItem colSpan={2} w="100%" h="10">
                    <Input
                      placeholder="Имя родителя"
                      size="md"
                      name="firstNameParent"
                      onChange={(e) => onChangeChild(e, index)}
                      value={child.firstNameParent}
                    />
                  </GridItem>
                  <GridItem colSpan={2} w="100%" h="10">
                    <Input
                      placeholder="Фамилия родителя"
                      size="md"
                      name="surnameParent"
                      onChange={(e) => onChangeChild(e, index)}
                      value={child.surnameParent}
                    />
                  </GridItem>
                  <GridItem colSpan={2} w="100%" h="10">
                    <Input
                      placeholder="Номер телефона родителя"
                      size="md"
                      type="tel"
                      name="telParent"
                      onChange={(e) => onChangeChild(e, index)}
                      value={child.telParent}
                    />
                  </GridItem>
                </Grid>
              </div>
            ))}
          </div>
          <div className="button-addChild">
            <Button colorScheme="orange" variant="outline" onClick={addChild}>
              + Ребенок
            </Button>
          </div>
        </div>
      </div>
    </>
  );
};
