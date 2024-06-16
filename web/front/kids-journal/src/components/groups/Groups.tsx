import React, { useEffect, useState } from "react";
import { AppRoute } from "../../const";
import { ButtonMain } from "../button/ButtonMain";
import "./Groups.css";
import { Link } from "react-router-dom";
import {useAppDispatch, useAppSelector} from "../../hooks/useAppDispatch";
import {getAllData} from "../../features/groupsSlice";
import {LoaderScreen} from "../../pages/loading-screen/LoaderScreen";

export type GroupProps = {
  organization: string | undefined;
};

export const Groups = ({ organization }: GroupProps) => {
  const [value, setValue] = useState("");
  const dispatch = useAppDispatch();
  const data = useAppSelector((state) => {
    return state.groups;
  });

  useEffect(() => {
    dispatch(getAllData())
  }, [])


  // const [firstGroups, setFirstGroups] = useState(groupInfo);
  // useEffect(() => {
  //
  //   fetch(`${ApiRoute}/organizations/${testOrganization}/groups`, {
  //     method: "GET",
  //     headers: { Accept: "application/json" },
  //   })
  //     .then((response) => {
  //       if (response.status === 200 || response.status === 201) {
  //         return response;
  //       }
  //       throw new Error();
  //     })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setFirstGroups(data);
  //     });
  // }, []);

  const filteredGroups = data.groups.filter((group) => {
    return group.name.toLowerCase().includes(value.toLowerCase());
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
            height="40px"
            width="176px"
            linkButton={`/${organization}${AppRoute.CreateGroups}`}
          >
            <svg
              width="14"
              height="14"
              viewBox="0 0 14 14"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M1 7L13 7"
                stroke="white"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <path
                d="M7 1L7 13"
                stroke="white"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
            Создать группу
          </ButtonMain>
        </div>
      </div>

      <div className="groups">
        <table className="groups__table">
          <thead className="groups-title">
            <tr>
              <td className="groups-title_label">Группа</td>
              <td className="groups-title_age">Возраст</td>
              <td className="groups-title_teach">Воспитатель</td>
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
                <td className="groups-item_teach">{group.group_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
};
