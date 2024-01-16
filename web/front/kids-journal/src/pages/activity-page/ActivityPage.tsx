import React from "react";
import "./ActivityPage.css";
import { Header } from "../../components/header/Header";
import { useParams } from "react-router-dom";
import { ButtonMain } from "../../components/button/ButtonMain";
import {AppRoute} from "../../const";

type ActivityPageProps = {};

function ActivityPage({}: ActivityPageProps): JSX.Element {
  const { organization } = useParams();
  return (
    <div>
      <Header />
      <div className="activity_container">
        <ButtonMain
          isDisable
          className="activity_item"
          height="30vh"
          linkButton=""
          width="380px"
        >
          Наблюдения
        </ButtonMain>
        <ButtonMain
          className="activity_item active_activity"
          height="30vh"
          linkButton={`/${organization}${AppRoute.Subject}`}
          width="400px"
        >
          Предметы
        </ButtonMain>
        <ButtonMain
          isDisable
          className="activity_item"
          height="30vh"
          linkButton=''
          width="380px"
        >
          Диагностика
        </ButtonMain>
      </div>
    </div>
  );
}

export default ActivityPage;
