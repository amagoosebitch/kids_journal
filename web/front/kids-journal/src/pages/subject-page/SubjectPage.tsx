import { Header } from "../../components/header/Header";
import React, { useState } from "react";
import { ButtonMain } from "../../components/button/ButtonMain";
import { AppRoute, subjectInfo } from "../../const";
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

export const SubjectPage = () => {
  const { organization } = useParams();
  const [value, setValue] = useState("");

  const filteredSubject = subjectInfo.filter((curSub) => {
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
          {filteredSubject
            .filter((subject) => {
              return subject.organization === organization;
            })
            .map((subject) => (
              <AccordionItem>
                <h2>
                  <AccordionButton>
                    <Box as="span" flex="1" textAlign="left">
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
                      {subject.topic.map((currentTopic) => (
                        <tr className="subject-item">
                          <td className="subject-item_name">
                            {currentTopic.name}
                          </td>
                          <td className="subject-item_age">
                            {currentTopic.age}
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
