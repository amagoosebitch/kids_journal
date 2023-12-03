import React, { useState } from "react";
import { AppRoute, infoGroups } from "../../const";
import { Button } from "../button/Button";
import "./Groups.css";
import { Link } from "react-router-dom";

export const Groups = () => {
  const [groups, setGroups] = useState(infoGroups);

  const [value, setValue] = useState("");
  const filteredGroups = groups.filter((group) => {
    return group.carouselLabel.toLowerCase().includes(value.toLowerCase());
  });

  return (
    <>
      <div className="groups__container">
        <div className="groups__from">
          <form className="groups_search-form">
            <input
              type="text"
              placeholder="Введите название группы"
              className="groups_search-input"
              onChange={(event: React.FormEvent<HTMLInputElement>) =>
                setValue(event.currentTarget.value)
              }
            />
          </form>
        </div>
        <div>
          <Button
            height="44px"
            width="211px"
            linkButton={AppRoute.CreateGroups}
          >
            Создать группу
          </Button>
        </div>
      </div>

      <div className="groups">
        <table className="groups__table">
          <thead className="groups-title">
            <tr>
              <td className="groups-title_label">Название группы</td>
              <td className="groups-title_age">Возраст детей</td>
            </tr>
          </thead>
          <tbody>
            {filteredGroups.map((group, index) => (
              <tr className="groups-item">
                <td className="groups-item_label">
                  <Link to={`${AppRoute.Groups}/${group.carouselLabel}`}>
                    {group.carouselLabel}
                  </Link>
                </td>
                <td className="groups-item_age">{group.carouselAge}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
};
