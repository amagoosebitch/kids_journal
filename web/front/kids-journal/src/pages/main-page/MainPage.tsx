import React, { useState } from "react";
import { Header } from "../../components/header/Header";
import { DateInput} from "../../components/date-input/DateInput";
import { Button } from "../../components/button/Button";
import { AppRoute } from "../../const";

import "./MainPage.css";
import { Carousel } from "../../components/carousel/Carousel";


function MainPage(): JSX.Element {
  return (
    <>
      <Header />
      <div className="main__container">
        <div>
          <DateInput/>
        </div>
        <div>
          <Button
              height="44px"
              width="211px"
              linkButton={AppRoute.CreateActivity}
          >
              Создать активность
          </Button>
        </div>
      </div>
      <Carousel/>
    </>
  );
}

export default MainPage;
