import React, { FormEvent, useState } from "react";
import { Header } from "../../components/header/Header";
import { ButtonMain } from "../../components/button/ButtonMain";
import { useParams } from "react-router-dom";
import { Input, Select, Textarea } from "@chakra-ui/react";
import { infoGroups, subjectInfo } from "../../const";
import "./CreateSubject.css";

type CreateSubjectPageProps = {};

const optionsAge = [
  { age: "0-3", value: 1 },
  { age: "3-6", value: 2 },
  { age: "6-9", value: 3 },
];

function CreateSubjectPage({}: CreateSubjectPageProps): JSX.Element {
  const { organization } = useParams();

  const subjects = subjectInfo.filter((obj) => {
    return obj.organization === organization;
  });

  const [valueName, setName] = useState(subjects[0]?.name);
  const [valueTopic, setValueTopic] = useState("");
  const [valueAge, setValueAge] = useState("");
  const [valueDescription, setValueDescription] = useState("");

  const addSubject = {
    organizationCur: organization,
    name: valueName,
    topic: [
      {
        name: valueTopic,
        age: valueAge,
        description: valueDescription,
      },
    ],
  };

  const [isIndividual, setIsIndividual] = useState(false);

  function onSubmitForm() {
    isIndividual
      ? subjectInfo
          .filter((obj) => {
            return (
              obj.organization === addSubject.organizationCur &&
              obj.name === addSubject.name
            );
          })
          .map((obj) => obj.topic.push(addSubject.topic[0]))
      : subjectInfo.push(addSubject);
    alert("GOOD!!!");
  }

  return (
    <div>
      <Header />
      <form className="creat-subject__container">
        <div className="creat__text">Создание нового предмета</div>
        <div className="subject-creat__form">
          <div className="subject-creat">
            <input
              type="checkbox"
              checked={isIndividual}
              onChange={() => setIsIndividual(!isIndividual)}
            />
            Нет нужного предмета
            <div className="subject-creat__form-items">
              {isIndividual ? (
                <Input
                  type="text"
                  placeholder="Введите название предмета"
                  onChange={(event: React.FormEvent<HTMLInputElement>) =>
                    setName(event.currentTarget.value)
                  }
                  style={{
                    background: "white",
                  }}
                />
              ) : (
                <Select
                  style={{
                    background: "white",
                  }}
                  onChange={(event: React.FormEvent<HTMLSelectElement>) =>
                    setName(event.currentTarget.value)
                  }
                >
                  {subjects.map((subject, index) => (
                    <option value={index}>{subject.name}</option>
                  ))}
                </Select>
              )}
            </div>
            <div className="subject-creat__form-items">
              <Input
                type="text"
                placeholder="Введите название темы"
                onChange={(event: React.FormEvent<HTMLInputElement>) =>
                  setValueTopic(event.currentTarget.value)
                }
                style={{
                  background: "white",
                }}
              />
            </div>
            <div className="subject-creat__form-items">
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
            <div className="subject-creat__form-items">
              <Textarea
                placeholder="Введите описание темы"
                onChange={(event: React.FormEvent<HTMLTextAreaElement>) =>
                  setValueDescription(event.currentTarget.value)
                }
                style={{
                  background: "white",
                }}
              />
            </div>
            <div className="creat-subject__form-button">
              <ButtonMain
                typeButton="submit"
                className="creat-subject__button"
                height="44px"
                width="211px"
                linkButton={""}
                onClick={onSubmitForm}
              >
                Создать предмет/тему
              </ButtonMain>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}

export default CreateSubjectPage;
