import React, { useState } from "react";
import { AppRoute, infoGroups } from "../../const";
import { ButtonMain } from "../button/ButtonMain";
import "./Groups.css";
import { Link } from "react-router-dom";

export type GroupProps = {
  organization: string | undefined;
};

export const Groups = ({ organization }: GroupProps) => {
  const currentGroup = infoGroups.filter((group) => {
    return organization ? group.organization.includes(organization) : null;
  });

  const [groups, setGroups] = useState(currentGroup);

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
          <ButtonMain
            height="44px"
            width="211px"
            linkButton={`/${organization}${AppRoute.CreateGroups}`}
          >
            Создать группу
          </ButtonMain>
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
                  <Link to={`/${organization}/${group.carouselLabel}`}>
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
