import React, { useEffect, useState } from "react";
import {AppRoute, ApiRoute, infoGroups, testOrganization} from "../../const";
import { ButtonMain } from "../button/ButtonMain";
import "./ProgressList.css";
import { Link, useNavigate, useParams } from "react-router-dom";
import { AuthMiddleware } from "../../middlewares";
import { employeeInfo } from "../employees/Employees";

export type ProgressListProps = {
  organization: string | undefined;
  group: string | undefined;
  lesson: string | undefined;
};

export const groupInfo = [
  {
    group_id: "",
    organization_id: "",
    name: "",
    age_range: "",
  },
];

export const ProgressList = ({
  organization,
  group,
  lesson,
}: ProgressListProps) => {
  const [firstProgress, setFirstProgress] = useState(groupInfo);
  useEffect(() => {
    fetch(`${ApiRoute}/organizations/${testOrganization}/groups`, {
      method: "GET",
      headers: { Accept: "application/json" },
    })
      .then((response) => {
        if (response.status === 200 || response.status === 201) {
          return response;
        }
        throw new Error();
      })
      .then((response) => response.json())
      .then((data) => {
        setFirstProgress(data);
      });
  }, []);

  const [value, setValue] = useState("");
  const filteredGroups = firstProgress.filter((group) => {
    return group.name.toLowerCase().includes(value.toLowerCase());
  });

  const handleGrade = () => {

  }

  return (
    <>
      <div className="progress__container">
        <div className="progress_title">Оценка прогресса</div>
        <div>
          <ButtonMain
            height="40px"
            width="193px"
            onClick={handleGrade}
            linkButton={``}
          >
            Сохранить изменения
          </ButtonMain>
        </div>
      </div>

      <div className="progress">
        <table className="progress__table">
          <thead className="progress-title">
            <tr>
              <td className="progress-title_label">Имя</td>
              <td className="progress-title_age">Возраст</td>
              <td className="progress-title_grade">Оценка</td>
            </tr>
          </thead>
          <tbody>
            {filteredGroups.map((group, index) => (
              <tr className="progress-item">
                <td className="progress-item_label">
                  <Link to={`/${organization}/${group.name}`}>
                    {group.name}
                  </Link>
                </td>
                <td className="progress-item_age">{group.age_range}</td>
                <td className="progress-item_grade">
                  <input
                    type="number"
                    min={0}
                    max={5}
                    id="grade"
                    name="grade"
                    className="progress-item_grade-input"
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
};
