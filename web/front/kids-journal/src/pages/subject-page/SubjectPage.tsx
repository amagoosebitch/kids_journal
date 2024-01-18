import { Header } from "../../components/header/Header";
import React, { useEffect, useState } from "react";
import { ButtonMain } from "../../components/button/ButtonMain";
import { AppRoute, ApiRoute, subjectInfo } from "../../const";
import {
  Accordion,
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Box,
} from "@chakra-ui/react";
import "./Subject.css";
import { useParams } from "react-router-dom";

export const infoSubject = [
  {
    organization_id: "",
    subject_id: "",
    name: "",
    description: "",
    age_range: "",
  },
];

export const infoTopic = [
  {
    presentation_id: "",
    name: "",
    description: "",
  },
];

type infoTopicProps = {
  organization_id: string;
  subject_id: string;
  presentation_id: string;
  name: string;
  description: string;
}[];

type allInfoTopicProps = infoTopicProps[];

export const SubjectPage = () => {
  const { organization } = useParams();
  const [value, setValue] = useState("");

  const [subjects, setSubjects] = useState(infoSubject);
  const [presentations, setPresentations] = useState(infoTopic);

  const [curSubject, setCurSubject] = useState("");

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
        setSubjects(data);
      });
  }, []);

  useEffect(() => {
    if (curSubject !== "") {
      setPresentations(infoTopic)
      fetch(`${ApiRoute}/subjects/${curSubject}/presentations`, {
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
          setPresentations(data);
        });
    }
  }, [curSubject]);


  const filteredSubject = subjects.filter((curSub) => {
    return curSub.name.toLowerCase().includes(value.toLowerCase());
  });

  return (
    <>
      <Header />
      <div className="subjects__container">
        <div className="groups__from">
          <form className="subjects_search-form">
            <input
              type="text"
              placeholder="Введите название предмета"
              className="subjects_search-input"
              onChange={(event: React.FormEvent<HTMLInputElement>) =>
                setValue(event.currentTarget.value)
              }
            />
          </form>
        </div>
        <div>
          <ButtonMain
            height="44px"
            width="211px"
            linkButton={`/${organization}${AppRoute.CreateSubject}`}
          >
            Создать предмет/тему
          </ButtonMain>
        </div>
      </div>

      <div className="subjects">
        <Accordion allowToggle>
          {filteredSubject.map((subject) => (
            <AccordionItem>
              <h2>
                <AccordionButton>
                  <Box
                    onClick={() => setCurSubject(subject.name)}
                    as="span"
                    flex="1"
                    textAlign="left"
                  >
                    {subject.name}
                  </Box>
                  <AccordionIcon />
                </AccordionButton>
              </h2>
              <AccordionPanel pb={4}>
                <table className="subject__table">
                  <thead className="subject-title">
                    <tr>
                      <td className="subject-title_name">Название темы</td>
                      <td className="subject-title_age">Возраст</td>
                      <td className="subject-description">Описание</td>
                    </tr>
                  </thead>
                  <tbody>
                    {presentations?.map((currentTopic) => (
                      <tr className="subject-item">
                        <td className="subject-item_name">
                          {currentTopic.name}
                        </td>
                        <td className="subject-item_age">
                          {subject.age_range}
                        </td>
                        <td className="subject-item_description">
                          {currentTopic.description}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </AccordionPanel>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
    </>
  );
};
