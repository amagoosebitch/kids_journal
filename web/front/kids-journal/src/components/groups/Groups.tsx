import React, {useEffect, useState} from "react";
import { AppRoute, ApiRoute, infoGroups } from "../../const";
import { ButtonMain } from "../button/ButtonMain";
import "./Groups.css";
import { Link } from "react-router-dom";

export type GroupProps = {
  organization: string | undefined;
};

export const groupInfo = [{
    group_id: '',
    organization_id: '',
    name: '',
    age_range: ''
}]

export const Groups = ({ organization }: GroupProps) => {
    const [firstGroups, setFirstGroups] = useState(groupInfo);
    useEffect(() => {fetch(`${ApiRoute}/organizations/${organization}/groups`,
          {method: 'GET', headers: {'Accept': 'application/json',}}).then(response => {
          if (response.status === 200 || response.status === 201) {
              return response;
          }
          throw new Error();
      }).then(response => response.json()).then(data => {setFirstGroups(data)});
      }, [])


  const [value, setValue] = useState("");
  const filteredGroups = firstGroups.filter((group) => {
    return group.name.toLowerCase().includes(value.toLowerCase());
  });

  console.log(filteredGroups)

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
                  <Link to={`/${organization}/${group.name}`}>
                    {group.name}
                  </Link>
                </td>
                <td className="groups-item_age">{group.age_range}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
};
