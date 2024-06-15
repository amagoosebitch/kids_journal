import React, { useState } from "react";
import { Header } from "../../components/header/Header";
import { DateInput } from "../../components/date-input/DateInput";
import { ButtonMain } from "../../components/button/ButtonMain";
import { AppRoute } from "../../const";

import "./MainPage.css";
import { Carousel } from "../../components/carousel/Carousel";
import { useParams } from "react-router-dom";
import { store } from "../../store";
import { fetchGroupsAction } from "../../store/api-actions";

function MainPage(): JSX.Element {
  const { organization } = useParams();

  const [currentDate, setCurrentDate] = useState(new Date());

  function getDate(obj: Date) {
    setCurrentDate(obj);
  }

  return (
    <>
      <Header />
      <div className="main__container">
        <div className="main__container-data">
          <DateInput getDate={getDate} organization={organization} />
        </div>
        <div className="main__container-button">
          <ButtonMain
            height="44px"
            width="171px"
            linkButton={`/${organization}${AppRoute.CreateActivity}`}
          >
            <svg
              width="14"
              height="14"
              viewBox="0 0 14 14"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M1 7L13 7"
                stroke="white"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <path
                d="M7 1L7 13"
                stroke="white"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
            Добавить урок
          </ButtonMain>
        </div>
      </div>
      <Carousel currentDate={currentDate} organization={organization} />
    </>
  );
}

export default MainPage;
