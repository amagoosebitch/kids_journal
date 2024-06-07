import React, { useEffect, useState } from "react";
import { Header } from "../../components/header/Header";
import { Link, useParams } from "react-router-dom";
import "./ChildProfile.css";
import { ApiRoute } from "../../const";
import { child } from "../../components/groupInfo/GroupInfo";

type ChildProfileProps = {};

function ChildProfile({}: ChildProfileProps): JSX.Element {
  const [children, setChildren] = useState([child]);
  const { organization, group, childName } = useParams();
    console.log(organization, group, childName)

  return (
    <>
      <Header />
      <div className="child_profile-container">
        <header className="child__info">
          <div className="child__info-img"></div>
          <div className="child__info_block">
              <header className="child__info_block-header">
                  <div className="child_name">{childName}</div>
                  <div className="child_group">Группа «{group}»</div>
              </header>
              <main className="child__info_block-main">
                  <div className="child_age">Возраст: {childName}</div>
                  <div className="child_parents">
                      <div className="child_parents-title">Родители</div>
                      <div className="child_parent">
                          <div>Мама: {childName}</div>
                          <div>Номер телефона: {childName}</div>
                      </div>
                      <div className="child_parent">
                          <div>Папа: {childName}</div>
                          <div>Номер телефона: {childName}</div>
                      </div>
                  </div>
                  <div className="child_teacher">
                      <div className="child_teacher-title">Воспитатель</div>
                      <div className="child_teacher-info">
                          <div>{childName}</div>
                          <div>Номер телефона: {childName}</div>
                      </div>
                  </div>
              </main>
          </div>
        </header>
        <section className="child__progress">
          <div className="child__progress-title">Прогресс ребенка</div>
          <table className="child__progress_table">
            <thead className="child__progress_table-title">
              <tr>
                <td className="child__progress_table_topic">Тема</td>
                <td className="child__progress_table_subject">Предмет</td>
                <td className="child__progress_table_number">Оценка</td>
              </tr>
            </thead>
            <tbody>
              <tr className="children-item">
                <td className="children-item_name">{childName}</td>
                <td className="children-item_age">{childName}</td>
                <td className="children-item_number">{childName}</td>
              </tr>
              <tr className="children-item">
                <td className="children-item_name">{childName}</td>
                <td className="children-item_age">{childName}</td>
                <td className="children-item_number">{childName}</td>
              </tr>
              <tr className="children-item">
                <td className="children-item_name">{childName}</td>
                <td className="children-item_age">{childName}</td>
                <td className="children-item_number">{childName}</td>
              </tr>
              <tr className="children-item">
                <td className="children-item_name">{childName}</td>
                <td className="children-item_age">{childName}</td>
                <td className="children-item_number">{childName}</td>
              </tr>
              <tr className="children-item">
                <td className="children-item_name">{childName}</td>
                <td className="children-item_age">{childName}</td>
                <td className="children-item_number">{childName}</td>
              </tr>
            </tbody>
          </table>
        </section>
      </div>
    </>
  );
}

export default ChildProfile;
