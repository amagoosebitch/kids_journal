import React, { useState } from "react";

import { Button } from "../../components/button/Button";
import { AppRoute } from "../../const";
import "./welcome-screem.css";

type WelcomeScreenProps = {};

function WelcomeScreen({}: WelcomeScreenProps): JSX.Element {
  const handleButtonClick = (event: React.MouseEvent) => {
    console.log("[button click event]", event);
  };

  const [click, setClick] = useState(false);
  const [button, setButton] = useState(true);

  const showButton = () => {
    if (window.innerWidth <= 960) {
      setButton(false);
    } else {
      setButton(true);
    }
  };

  window.addEventListener("resize", showButton);

  return (
    <div className="home">
      <div className="home-text">
        <div className="text-title">Kids Journal</div>
        <div className="text-description">
          Сервис для автоматизации работы детских садиков с методикой Монтессори
        </div>
      </div>
      <div className="home-buttons">
        <div className='home-button'>
          <Button linkButton={AppRoute.SignIn} height="44px" width="316px">
            Войти
          </Button>
        </div>
        <div className='home-button'>
          <Button linkButton={AppRoute.SignUp} height="44px" width="316px">
            Зарегистрироваться
          </Button>
        </div>
      </div>
    </div>
  );
}

export default WelcomeScreen;
