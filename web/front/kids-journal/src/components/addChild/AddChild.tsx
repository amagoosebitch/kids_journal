import React, { useState } from "react";
import {
  Button,
  CloseButton,
  Grid,
  GridItem,
  Input,
  FormControl,
} from "@chakra-ui/react";
import { useParams } from "react-router-dom";
import "./AddChild.css";
import { ButtonMain } from "../button/ButtonMain";
import { ApiRoute } from "../../const";
import { InputPhone } from "../input-phone/InputPhone";

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

type addChildrenProps = {
  organization: string | undefined;
  groupId: string | undefined;
};

export const AddChild = ({ organization, groupId }: addChildrenProps) => {
  const [isButton, setIsButton] = useState(false);

  const childTemplate = {
    firstNameChild: "",
    surnameChild: "",
    dataChild: Date(),
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

    const headers = new Headers();
    headers.append("Content-Type", "application/json");

    for (let i = 0; i < children.length; i++) {
      let child = children[i];
      let body_parent_1 = JSON.stringify({
        first_name: child.firstNameParent,
        last_name: child.surnameParent,
        name: child.firstNameParent + " " + child.surnameParent,
        parent_id: child.firstNameParent + " " + child.surnameParent,
        phone_number: child.telParent,
      });

      let requestOptions1 = {
        method: "POST",
        headers: headers,
        body: body_parent_1,
      };

      fetch(ApiRoute + "/parents", requestOptions1);

      let body_parent_2 = JSON.stringify({
        first_name: child.firstNameParentTWO,
        last_name: child.surnameParentTWO,
        name: child.firstNameParentTWO + " " + child.surnameParentTWO,
        parent_id: child.firstNameParentTWO + " " + child.surnameParentTWO,
        phone_number: child.telParentTWO,
      });

      let requestOptions2 = {
        method: "POST",
        headers: headers,
        body: body_parent_2,
      };

      fetch(ApiRoute + "/parents", requestOptions2);

      let body_child = JSON.stringify({
        first_name: child.firstNameChild,
        last_name: child.surnameChild,
        name: child.firstNameChild + " " + child.surnameChild,
        child_id: child.firstNameChild + " " + child.surnameChild,
        birth_date: new Date(child.dataChild),
        parent_1_id: child.firstNameParent + " " + child.surnameParent,
        parent_2_id: child.firstNameParentTWO + " " + child.surnameParentTWO,
      });

      let requestOptions3 = {
        method: "POST",
        headers: headers,
        body: body_child,
      };

      fetch(ApiRoute + `/${groupId}/child`, requestOptions3);
    }
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
                        isRequired
                        placeholder="Имя ребенка"
                        size="md"
                        name="firstNameChild"
                        onChange={(e) => onChangeChild(e, index)}
                        value={child.firstNameChild}
                      />
                    </GridItem>
                    <GridItem colSpan={2} w="100%" h="10">
                      <Input
                        isRequired
                        placeholder="Фамилия ребенка"
                        size="md"
                        name="surnameChild"
                        onChange={(e) => onChangeChild(e, index)}
                        value={child.surnameChild}
                      />
                    </GridItem>
                    <GridItem colSpan={2} w="100%" h="10">
                      <Input
                        isRequired
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
                        isRequired
                        placeholder="Имя родителя"
                        size="md"
                        name="firstNameParent"
                        onChange={(e) => onChangeChild(e, index)}
                        value={child.firstNameParent}
                      />
                    </GridItem>
                    <GridItem colSpan={2} w="100%" h="10">
                      <FormControl isRequired>
                        <Input
                          placeholder="Фамилия родителя"
                          size="md"
                          name="surnameParent"
                          onChange={(e) => onChangeChild(e, index)}
                          value={child.surnameParent}
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem colSpan={2} w="100%" h="10">
                      <InputPhone
                        isRequired
                        placeholder="Номер телефона родителя"
                        size="md"
                        type="tel"
                        name="telParent"
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                          onChangeChild(e, index)
                        }
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
                      <InputPhone
                        placeholder="Номер телефона родителя"
                        size="md"
                        type="tel"
                        name="telParentTWO"
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                          onChangeChild(e, index)
                        }
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
              linkButton={`/${organization}/${groupId}`}
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
