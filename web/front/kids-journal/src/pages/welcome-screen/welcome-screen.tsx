import React, {useEffect, useState} from "react";

import { ButtonMain } from "../../components/button/ButtonMain";
import {ApiRoute, AppRoute, LoginUrl} from "../../const";
import Cookies from 'js-cookie';
import "./welcome-screem.css";
import {useNavigate, useSearchParams} from "react-router-dom";
import { jwtDecode } from 'jwt-decode'
import {groupInfo} from "../../components/groups/Groups";

type WelcomeScreenProps = {};

export const cookieType = {
  phone_number: "",
  role:"",
  user_id:"805667021",
}

function WelcomeScreen({}: WelcomeScreenProps): JSX.Element {
  const handleButtonClick = (event: React.MouseEvent) => {
    console.log("[button click event]", event);
  };
  const [searchParams, setSearchParams] = useSearchParams();
  const [orgNames, setOrgNames] = useState(['']);
  const navigate = useNavigate();
  let cookie = searchParams.get("cookie");
  let decoded = cookieType
  let phone_number = '';
  if (cookie !== null) {
    Cookies.set('Authorization', cookie)
    decoded = jwtDecode(cookie)
    phone_number = decoded.phone_number;
  }


  useEffect(() => {
    if (phone_number === '') {return}
    fetch(`${ApiRoute}/employee/${phone_number}/organizations`,
        {method: 'GET', headers: {'Accept': 'application/json',}}).then(response => {
        if (response.status === 200 || response.status === 201) {
            return response;
        }
        throw new Error();
    }).then(response => response.json()).then(data => {setOrgNames(data)})
        .then( () => {
          if (orgNames.length >= 1 && orgNames[0].length >= 1) {
            console.log(`/${orgNames[0]}${AppRoute.Main}`)
            navigate(`/${orgNames[0]}${AppRoute.Main}`);
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
          <ButtonMain
            linkButton={LoginUrl}
            height="44px"
            width="316px"
          >
            Войти
          </ButtonMain>
        </div>
        <div className="home-button">
          <ButtonMain linkButton={AppRoute.SignUp} height="44px" width="316px">
            Зарегистрироваться
          </ButtonMain>
        </div>
      </div>
    </div>
  );
}

export default WelcomeScreen;
