import React, { useState } from "react";
import { Header } from "../../components/header/Header";
import { DateInput } from "../../components/date-input/DateInput";
import { ButtonMain } from "../../components/button/ButtonMain";
import { AppRoute } from "../../const";

import "./MainPage.css";
import { Carousel } from "../../components/carousel/Carousel";
import { useParams } from "react-router-dom";

function MainPage(): JSX.Element {
  const { organization } = useParams();
  return (
    <>
      <Header />
      <div className="main__container">
        <div>
          <DateInput />
        </div>
        <div>
          <ButtonMain
            height="44px"
            width="211px"
            linkButton={AppRoute.CreateActivity}
          >
            Создать активность
          </ButtonMain>
        </div>
      </div>
      <Carousel organization={organization} />
    </>
  );
}

export default MainPage;
