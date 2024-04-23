import React, {useEffect, useState} from "react";

import { ButtonMain } from "../../components/button/ButtonMain";
import {ApiRoute, AppRoute, LoginUrl} from "../../const";
import Cookies from 'js-cookie';
import "./welcome-screem.css";
import {useNavigate, useSearchParams} from "react-router-dom";
import { jwtDecode } from 'jwt-decode'
import {groupInfo} from "../../components/groups/Groups";
import {AuthMiddleware} from "../../middlewares";

type WelcomeScreenProps = {};

export const cookieType = {
  phone_number: "",
  role:"",
  user_id:"",
}

function WelcomeScreen({}: WelcomeScreenProps): JSX.Element {
  const handleButtonClick = (event: React.MouseEvent) => {
    console.log("[button click event]", event);
  };
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  let cookie = searchParams.get("cookie");
  if (cookie !== null) {
    Cookies.set('Authorization', cookie)
  }
  let phone_number = AuthMiddleware(navigate);

  useEffect(() => {
    if (!phone_number) {return}
    fetch(`${ApiRoute}/employee/${phone_number}/organizations`,
        {method: 'GET', headers: {'Accept': 'application/json',}}).then(response => {
        if (response.status === 200 || response.status === 201) {
            return response;
        }
        throw new Error();
    }).then(response => response.json())
        .then( (data) => {
          console.log(data)
          if (data.length >= 1 && data[0].length >= 1) {
            navigate(`/${data[0]}${AppRoute.Main}`);
          }
        });
    }, [])

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

  console.log(new Date().getMonth());
  return (
    <div className="home">
      <div className="home-text">
        <div className="text-title">Kids Journal</div>
        <div className="text-description">
          Сервис для автоматизации работы детских садиков с методикой Монтессори
        </div>
      </div>
    <div className="home-buttons">
        <div className="home-button">
          <ButtonMain linkButton={LoginUrl} height="50px" width="288px" background={"#54A9EB"}>
            Войти через Telegram
          </ButtonMain>
        </div>
      </div>
    </div>
  );
}

export default WelcomeScreen;
