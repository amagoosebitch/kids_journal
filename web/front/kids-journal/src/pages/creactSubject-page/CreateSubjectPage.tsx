import React, { useState } from "react";
import { Header } from "../../components/header/Header";
import { AddEmployees } from "../../components/addEmployees/AddEmployees";
import { ButtonMain } from "../../components/button/ButtonMain";
import { useParams } from "react-router-dom";
import { Input, Select, Textarea } from "@chakra-ui/react";
import { infoGroups } from "../../const";

type CreateSubjectPageProps = {};

const optionsAge = [
  { age: "0-3", value: 1 },
  { age: "3-6", value: 2 },
  { age: "6-9", value: 3 },
];

function CreateSubjectPage({}: CreateSubjectPageProps): JSX.Element {
  const { organization } = useParams();

  const [value, setValue] = useState("");
  const [valueName, setName] = useState("");
  const [valueTopic, setValueTopic] = useState("");
  const [valueAge, setValueAge] = useState("");
  const [valueDescription, setValueDescription] = useState("");

  const addEmployees = () => {
    const result = {
      organizationCur: organization,
      group: value,
      name: valueName,
      topic: {
        name: valueTopic,
        age: valueAge,
        description: valueDescription,
      },
    };
    console.log(result);
  };

  return (
    <div>
      <Header />
      <div className="creat__text">Создание нового предмета</div>
      <div className="creat__form">
        <div>
          <div>
            <Select
              placeholder="Выберете группу"
              onChange={(event: React.FormEvent<HTMLSelectElement>) =>
                setValue(event.currentTarget.value)
              }
            >
              {infoGroups
                .filter((group) => {
                  return group.organization === organization;
                })
                .map((group, index) => (
                  <option value={index}>{group.carouselLabel}</option>
                ))}
            </Select>
          </div>
          <div>
            <Input
              type="text"
              placeholder="Введите название предмета"
              onChange={(event: React.FormEvent<HTMLInputElement>) =>
                setName(event.currentTarget.value)
              }
            />
          </div>
          <div>
            <Input
              type="text"
              placeholder="Введите название темы"
              onChange={(event: React.FormEvent<HTMLInputElement>) =>
                setValueTopic(event.currentTarget.value)
              }
            />
          </div>
          <div>
            <Select
              placeholder="Выберете возраст детей"
              onChange={(event: React.FormEvent<HTMLSelectElement>) =>
                setValueAge(event.currentTarget.value)
              }
            >
              {optionsAge.map((option) => (
                <option value={option.value}>{option.age}</option>
              ))}
            </Select>
          </div>
          <div>
            <Textarea
                placeholder='Введите описание темы'
              onChange={(event: React.FormEvent<HTMLTextAreaElement>) =>
                setValueDescription(event.currentTarget.value)
              }
            />
          </div>
          <div>
            <ButtonMain
              className="creat__form-button"
              height="44px"
              width="211px"
              linkButton={""}
              onClick={() => addEmployees()}
            >
              Создать предмет/тему
            </ButtonMain>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CreateSubjectPage;
