import React, { useState } from "react";
import { ButtonMain } from "../button/ButtonMain";
import {AppRoute, infoEmployees} from "../../const";
import { Link } from "react-router-dom";

import "./Employees.css";

export type EmployeesProps = {
  organization: string | undefined;
};

export const Employees = ({ organization }: EmployeesProps) => {
  const currentEmployees = infoEmployees.filter((employee) => {
    return organization ? employee.organization.includes(organization) : null
  })

  const [employees, setEmployees] = useState(currentEmployees);

  return (
    <>
      <div className="employees_title">
        <div className="employees_label">Сотрудники</div>
        <div>
          <ButtonMain
            height="44px"
            width="211px"
            linkButton={AppRoute.CreateEmployees}
          >
            Добавить сотрудника
          </ButtonMain>
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
