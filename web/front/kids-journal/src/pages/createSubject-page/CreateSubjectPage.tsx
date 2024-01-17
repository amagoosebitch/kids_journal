import React, { FormEvent, useEffect, useState } from "react";
import { Header } from "../../components/header/Header";
import { ButtonMain } from "../../components/button/ButtonMain";
import { useParams } from "react-router-dom";
import { Input, Select, Textarea } from "@chakra-ui/react";
import { infoGroups, ApiRoute, subjectInfo } from "../../const";
import "./CreateSubject.css";

type CreateSubjectPageProps = {};

const optionsAge = [
  { age: "0-3", value: 1 },
  { age: "3-6", value: 2 },
  { age: "6-9", value: 3 },
];

export const infoSubject = [
  {
    organization_id: "",
    subject_id: "",
    name: "",
    description: "",
    age_range: "",
  },
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

  const [subjectsCur, setsubjectsCur] = useState(infoSubject);
  useEffect(() => {
    fetch(`${ApiRoute}/organizations/${organization}/subjects`, {
      method: "GET",
      headers: { Accept: "application/json" },
    })
      .then((response) => {
        if (response.status === 200 || response.status === 201) {
          return response;
        }
        throw new Error();
      })
      .then((response) => response.json())
      .then((data) => {
        setsubjectsCur(data);
      });
  }, []);

  function onSubmitForm() {
    const headers = new Headers();
    headers.append("Content-Type", "application/json");

    if (isIndividual) {
      console.log(isIndividual)
      let subject = JSON.stringify({
        organization_id: organization,
        subject_id: valueName,
        name: valueName,
      });
      console.log(subject);

      let requestOptions = {
        method: "POST",
        headers: headers,
        body: subject,
      };

      fetch(ApiRoute + `/organizations/${organization}/subjects`, requestOptions);
    }

    let presentation = JSON.stringify({
      subject_id: valueName,
      presentation_id: valueTopic,
      name: valueTopic,
      description: valueDescription,
    });
    console.log(presentation);

    let requestOptions1 = {
      method: "POST",
      headers: headers,
      body: presentation,
    };

    fetch(ApiRoute + `/subjects/${valueName}/presentations`, requestOptions1);
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
                  {subjectsCur.map((subject, index) => (
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
