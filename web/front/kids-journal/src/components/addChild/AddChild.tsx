import React, { useState } from "react";
import { Button, CloseButton, Grid, GridItem, Input } from "@chakra-ui/react";
import { useParams } from "react-router-dom";
import "./AddChild.css";
import { ButtonMain } from "../button/ButtonMain";

type Child = {
  firstNameChild: string;
  surnameChild: string;
  dataChild: string;
  firstNameParent: string;
  surnameParent: string;
  telParent: string;
  firstNameParentTWO: string;
  surnameParentTWO: string;
  telParentTWO: string;
};

export const AddChild = () => {
  const { organization, groupId } = useParams();

  const [isButton, setIsButton] = useState(false);

  const childTemplate = {
    firstNameChild: "",
    surnameChild: "",
    dataChild: "",
    firstNameParent: "",
    surnameParent: "",
    telParent: "",
    firstNameParentTWO: "",
    surnameParentTWO: "",
    telParentTWO: "",
  };

  const [children, setChildren] = useState([childTemplate]);
  const addChild = () => {
    isButton ? setChildren([...children, childTemplate]) : setIsButton(true);
  };

  const onChangeChild = (
    e: React.FormEvent<HTMLInputElement>,
    index: number,
  ) => {
    const updatedChildren = children.map((child, i) =>
      index == i
        ? Object.assign(child, {
            [e.currentTarget.name]: e.currentTarget.value,
          })
        : child,
    );
    setChildren(updatedChildren);
  };

  const removeChild = (index: number) => {
    const filteredChildren = [...children];
    filteredChildren.splice(index, 1);
    setChildren(filteredChildren);
  };

  const [value, setValue] = useState("");
  const [valueAge, setValueAge] = useState("");
  const [valueName, setNameInput] = useState("");

  const addToGroup = () => {
    console.log(children);
  };

  return (
    <>
      <div className="creat__text">Добавление детей в группу</div>
      <div className="creat__form">
        <div className="add_children">
          <div className="childrenScroll">
            {isButton &&
              children?.map((child, index) => (
                <div className="add_children-item">
                  <Grid
                    templateRows="repeat(3, 1fr)"
                    templateColumns="repeat(7, 1fr)"
                    gap={3}
                    key={index + 1}
                  >
                    <GridItem rowSpan={3} colSpan={1} className="Close-Button">
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

                    <GridItem colSpan={2} w="100%" h="10">
                      <Input
                        placeholder="Имя родителя"
                        size="md"
                        name="firstNameParentTWO"
                        onChange={(e) => onChangeChild(e, index)}
                        value={child.firstNameParentTWO}
                      />
                    </GridItem>
                    <GridItem colSpan={2} w="100%" h="10">
                      <Input
                        placeholder="Фамилия родителя"
                        size="md"
                        name="surnameParentTWO"
                        onChange={(e) => onChangeChild(e, index)}
                        value={child.surnameParentTWO}
                      />
                    </GridItem>
                    <GridItem colSpan={2} w="100%" h="10">
                      <Input
                        placeholder="Номер телефона родителя"
                        size="md"
                        type="tel"
                        name="telParentTWO"
                        onChange={(e) => onChangeChild(e, index)}
                        value={child.telParentTWO}
                      />
                    </GridItem>
                  </Grid>
                </div>
              ))}
          </div>
          <div className="button-addChild">
            <Button
              className="button-addChild"
              colorScheme="orange"
              variant="outline"
              onClick={addChild}
            >
              + Ребенок
            </Button>
          </div>

          <div className="add_children-in-group__button">
            <ButtonMain
              height="44px"
              width="211px"
              linkButton={""}
              onClick={() => addToGroup()}
            >
              Добавить детей в группу
            </ButtonMain>
          </div>
        </div>
      </div>
    </>
  );
};
