import React, { useState } from "react";
import { Button } from "../button/Button";
import { AppRoute, infoEmployees } from "../../const";
import { Link } from "react-router-dom";

import "./Employees.css";

export const Employees = () => {
  const [employees, setEmployees] = useState(infoEmployees);

  return (
    <>
      <div className="employees_title">
        <div className="employees_label">Сотрудники</div>
        <div>
          <Button
            height="44px"
            width="211px"
            linkButton={AppRoute.CreateGroups}
          >
            Добавить сотрудника
          </Button>
        </div>
      </div>

      <div className="employees">
        <table className="employees__table">
          <thead className="employees-title">
            <tr>
              <td className="employees-title_name">Имя</td>
              <td className="employees-title_role_id">Роль</td>
              <td className="employees-phone_number">Контакт</td>
            </tr>
          </thead>
          <tbody>
            {employees.map((employe) => (
              <tr className="employees-item">
                <td className="employees-item_name">{employe.name}</td>
                <td className="employees-item_role_id">{employe.role_id}</td>
                <td className="employees-item_phone_number">
                  {employe.phone_number}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
};
